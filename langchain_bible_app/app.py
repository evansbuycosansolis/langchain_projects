import os
from flask import Flask, render_template, request
from dotenv import load_dotenv

from langchain_openai import ChatOpenAI
from langchain.text_splitter import CharacterTextSplitter
from langchain.prompts.prompt import PromptTemplate
from langchain_core.documents import Document
from langchain.chains.combine_documents import create_stuff_documents_chain

# Load environment variables
load_dotenv()

# Initialize Flask app
app = Flask(__name__)

# Load Bible text once at startup
with open("bible.text", "r", encoding="utf-8") as file:
    bible_text = file.read()

# Convert text to LangChain Document
doc = Document(page_content=bible_text)

# Split the document into smaller chunks
splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=100)
docs = splitter.split_documents([doc])
limited_docs = docs[:5]  # Limit to avoid token overflow

# Initialize LLM
llm = ChatOpenAI(model="gpt-4o", temperature=0)

# Prompt template
prompt_template = """Use the following context to answer the question:
Context:
{context}

Question: {question}
Helpful Answer:"""
prompt = PromptTemplate.from_template(prompt_template)

# Create the StuffDocumentsChain
chain = create_stuff_documents_chain(llm, prompt)

@app.route("/", methods=["GET", "POST"])
def index():
    answer = ""
    question = ""  # <-- Add this line

    if request.method == "POST":
        question = request.form.get("question")
        if question:
            try:
                inputs = {
                    "context": limited_docs,
                    "question": question
                }
                response = chain.invoke(inputs)
                answer = response
            except Exception as e:
                answer = f"Error: {str(e)}"

    return render_template("index.html", answer=answer, question=question)



if __name__ == "__main__":
    app.run(debug=True)