# LangChain Chat with your Data: text - SFBU Customer Support System

This project demonstrates a Customer Support Chatbot built using Retrieval Augmented Generation (RAG) with OpenAI’s GPT model and a vectorstore (Chroma) for efficient document retrieval. The chatbot is designed to answer questions based on the contents of uploaded documents, such as PDFs, with a conversational interface.

## Features

- Document Loading: Load PDF documents to create a vectorstore.
- Conversational Q&A: Engage in a conversational Q&A with the chatbot.
- Retrieval-Augmented Generation (RAG): Uses similarity search to retrieve relevant document chunks to answer questions.
- Memory Support: Retains conversation history for context continuity.
- Web Interface: Uses Panel and Param for a simple web interface.
- File Upload: Upload a new PDF document dynamically for querying.

## Requirements

- Python 3.x
- OpenAI API Key (stored in `.env`)

To install the required dependencies, run:

```bash
pip install -r requirements.txt
```
#### Usage

## 1. Setup Environment Variables:

Create a .env file and add your OpenAI API key:

OPENAI_API_KEY=your_api_key

## 2. Run the Application:

```bash
python3 SFBU_Customer_Support.py
```

## 3. Interact with the Chatbot:

Once the application is running, you can interact with the chatbot through the web-based interface.
Upload PDF documents using the file input component, and submit queries to receive responses based on the document content.
