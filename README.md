# langchain_projects

Welcome to `langchain_projects` — a growing collection of hands-on experiments, tools, and applications built using [LangChain](https://www.langchain.com/), [OpenAI](https://openai.com), and other LLM frameworks.

This repository is focused on showcasing real-world use cases of Language Models (LLMs) integrated into Python applications.

---

## Projects

### 1. AskMyPDF

A Flask-based web app that allows you to upload a PDF and ask questions about its content using LangChain’s `StuffDocumentsChain` and OpenAI's GPT-4o models.

#### Features
- PDF upload and parsing using `PyPDFLoader`
- Contextual document Q&A using LangChain and OpenAI
- Simple HTML/Flask frontend

#### Run Locally

#### bash
#### Navigate into the project folder
cd askmypdf

#### Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate      # On Windows: .venv\Scripts\activate

#### Install dependencies
pip install -r requirements.txt

#### Run the Flask app
python app.py



### 2. ChatWebsite
ChatWebsite is a Flask-based app that lets users ask questions about the content of any public webpage. It uses LangChain's WebBaseLoader to fetch and parse website data, OpenAI's ChatOpenAI for LLM responses, and supports user interaction via a simple HTML frontend.

Features
Accepts any URL input

Extracts webpage content with BeautifulSoup via LangChain

Splits text for optimal LLM processing using CharacterTextSplitter

Generates intelligent answers using OpenAI’s GPT models

Lightweight frontend with Flask

Run Locally
####bash

#### Navigate into the project folder
cd chatwebsite

#### Create and activate virtual environment
python -m venv .venv
source .venv/bin/activate    # On Windows: .venv\Scripts\activate

#### Install dependencies
pip install -r requirements.txt

#### Run the Flask app
python app.py
