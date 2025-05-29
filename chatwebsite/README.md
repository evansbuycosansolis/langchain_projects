# ChatWebsite

ChatWebsite is a Flask-based web application that lets users ask questions about any public webpage. It uses **LangChain**, **OpenAI's GPT models**, and **BeautifulSoup** to extract content from URLs and provide intelligent responses.

## Features

- URL input: Users can enter any website URL.
- Ask questions: Get relevant answers from the webpage content.
- Powered by OpenAI's GPT (via LangChain's `ChatOpenAI`)
- HTML content parsing via LangChain's `WebBaseLoader`
- Text splitting for better processing using `CharacterTextSplitter`
- Lightweight frontend built with HTML and Flask

---

## Tech Stack

- Python 3.10+
- Flask
- LangChain
- OpenAI API
- Requests
- BeautifulSoup (via LangChain)

---

## Setup Instructions

### 1. Clone the repository

```bash
git clone https://github.com/evansbuycosansolis/langchain_projects.git
cd langchain_projects/chatwebsite
