from flask import Flask, render_template, request
import os

from langchain_openai import ChatOpenAI
from langchain.chains.combine_documents.stuff import StuffDocumentsChain
from langchain.text_splitter import CharacterTextSplitter
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from langchain_community.document_loaders import PyPDFLoader

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def process_pdf(pdf_path, question):
    # 1. Load and split the PDF
    loader = PyPDFLoader(pdf_path)
    docs = loader.load()
    print(f"[DEBUG] Loaded {len(docs)} pages from PDF")

    if not docs:
        return "No content could be extracted from the PDF."

    text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    splits = text_splitter.split_documents(docs)

    if not splits:
        return "PDF content could not be split for processing."

    # 2. Set up the LLM
    llm = ChatOpenAI(model="gpt-4o-mini-2024-07-18", temperature=0)

    # 3. Define the prompt template
    prompt = PromptTemplate.from_template("""
    Use the following context to answer the question.
    Context: {context}

    Question: {question}
    """)

    # 4. Wrap prompt and LLM into an LLMChain
    llm_chain = LLMChain(llm=llm, prompt=prompt)

    # 5. Set up the StuffDocumentsChain using the LLMChain
    chain = StuffDocumentsChain(
        llm_chain=llm_chain,
        document_variable_name="context"
    )

    # 6. Invoke the chain with input_documents and question
    result = chain.invoke({
        "input_documents": splits,
        "question": question
    })

    return result["output_text"] if isinstance(result, dict) and "output_text" in result else result

@app.route('/', methods=['GET', 'POST'])
def index():
    answer = None
    message = None

    if request.method == 'POST':
        if 'pdf' in request.files and request.files['pdf']:
            pdf = request.files['pdf']
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf.filename)
            pdf.save(pdf_path)

            print(f"[DEBUG] Saved PDF to: {pdf_path}")
            print(f"[DEBUG] File exists? {os.path.exists(pdf_path)}")

            if not pdf.filename.lower().endswith('.pdf'):
                message = 'Please upload a valid PDF file.'
                return render_template('index.html', message=message, pdf_uploaded=False)

            message = 'PDF uploaded successfully! Now ask a question below.'
            return render_template('index.html', message=message, pdf_uploaded=True, pdf_filename=pdf.filename)

        elif request.form.get('question') and request.form.get('pdf_filename'):
            question = request.form['question']
            pdf_filename = request.form['pdf_filename']
            pdf_path = os.path.join(app.config['UPLOAD_FOLDER'], pdf_filename)

            if os.path.exists(pdf_path):
                try:
                    answer = process_pdf(pdf_path, question)
                except Exception as e:
                    answer = f"Error: {str(e)}"
            else:
                answer = "PDF not found. Please upload again."

            return render_template('index.html', answer=answer, pdf_uploaded=True, pdf_filename=pdf_filename)

    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
