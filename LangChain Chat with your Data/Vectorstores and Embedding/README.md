# LangChain Chat with your Data: Vectorstores and Embedding

This project demonstrates how to implement a Retrieval-Augmented Generation (RAG) workflow using various document loaders, embeddings, and vector stores to answer queries based on specific content from documents like PDFs, YouTube transcriptions, etc.

## Project Overview

### Steps Covered:
1. Loading Documents: Load PDF documents and YouTube transcriptions for processing.
2. Chunking Documents: Split large documents into smaller chunks for better embedding and retrieval.
3. Embeddings: Embed the document chunks using OpenAI embeddings.
4. Vector Store: Store the embeddings in a persistent vector store (Chroma) for efficient similarity search.
5. Similarity Search: Use the vector store to perform similarity searches based on user queries.
6. Edge Case Handling: Simulate edge cases in retrieval such as duplicate content and specificity issues.

## Prerequisites

- Python 3.7+
- OpenAI API key (set up in `.env` file)
- Required libraries (listed in `requirements.txt`)

## Setup

1. Clone the Repository:

   ```bash
   git clone https://github.com/vaishnavi477/Machine-Learning/LangChain Chat with your Data.git
   cd Vectorstores and Embedding

2. Install Dependencies:
   ``` bash
   pip install -r requirements.txt
   ```
3. Set Up the OpenAI API Key:

   Create a .env file in the project root and add your OpenAI API key:
   
   OPENAI_API_KEY=your-api-key-here

5. Run the Script:

  ``` bash
   python3 Vectorstores_and_Embedding.py
  ```

 

