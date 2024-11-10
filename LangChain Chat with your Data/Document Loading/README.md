# Document Loading for Retrieval-Augmented Generation (RAG)

This project demonstrates the process of loading and processing documents from various sources, such as PDFs, YouTube transcripts, web pages, and Notion pages. The content from these sources is broken down into smaller, manageable chunks, optimized for quick retrieval, and used for answering queries based on specific document content.

## Project Overview

This project loads documents from multiple sources, processes them, and prepares them for use with Retrieval-Augmented Generation (RAG) models, such as OpenAI's GPT models, to answer queries based on specific document content. It supports loading content from:

- **PDFs**: Loads pages of a PDF document and extracts text for retrieval.
- **YouTube**: Transcribes YouTube video content using the OpenAI Whisper API.
- **Web Pages**: Loads HTML content from a specified URL, removing unnecessary formatting.
- **Notion Pages**: Loads content from Notion, stored in markdown format.

## Setup Instructions

### 1. Install Dependencies

Ensure that you have Python 3.7+ installed on your machine. Install the necessary libraries using `pip`:

```bash
pip install -r requirements.txt
```
### `requirements.txt`

This file lists all the dependencies needed for the project. You can generate it with `pip freeze` or manually add the libraries.

```txt
openai==0.27.0
python-dotenv==1.0.0
langchain-community==0.0.1
yt-dlp==2023.2.8
pydub==0.25.1
requests==2.28.1
```

### 2. Set Up Environment Variables

Create a .env file in the root directory of the project and add your OpenAI API key and other required environment variables. 

OPENAI_API_KEY=your_openai_api_key
USER_AGENT=your_user_agent_string

### 3. Run the Script

Once the setup is complete, you can run the document loading and processing script:

``` bash
python3 document_loader.py
```

This script loads content from PDFs, YouTube transcripts, web pages, and Notion pages, processes them, and provides preview output.


