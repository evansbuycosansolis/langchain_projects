from flask import Flask, render_template, request
import os
from dotenv import load_dotenv
from flask import Flask, render_template, request

# Load environment variables from .env
load_dotenv()

# Optional: Ensure the key exists (optional safety check)
assert "OPENAI_API_KEY" in os.environ, "OPENAI_API_KEY not found in environment."

from langchain_openai import ChatOpenAI
from langchain.chains.question_answering import load_qa_chain
from langchain.text_splitter import CharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader

app = Flask(__name__)

def process_url(url, question):
    try:
        # 1. Load the web page content using BeautifulSoup
        loader = WebBaseLoader(url)
        docs = loader.load()

        if not docs:
            return "No content could be extracted from the website."

        # 2. Split into manageable chunks
        text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=100)
        splits = text_splitter.split_documents(docs)

        if not splits:
            return "Failed to split website content for processing."

        # 3. Set up the LLM
        llm = ChatOpenAI(model="gpt-4o-mini-2024-07-18", temperature=0)

        # 4. Load QA chain and use invoke
        chain = load_qa_chain(llm, chain_type="stuff")
        result = chain.invoke({"input_documents": splits, "question": question})

        return result.get("output_text", "No answer generated.")

    except Exception as e:
        return f"Error: {str(e)}"


@app.route('/', methods=['GET', 'POST'])
def index():
    answer = None
    message = None
    url = ""
    if request.method == 'POST':
        url = request.form.get('url')
        question = request.form.get('question')
        if url and question:
            answer = process_url(url, question)
        else:
            message = "Please provide both a website URL and your question."
    return render_template('index.html', answer=answer, url=url, message=message)

if __name__ == '__main__':
    app.run(debug=True)