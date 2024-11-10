# Vectorstores and Embeddings for RAG

# Retrieval Augmented Generation (RAG) Workflow:
# 1. Load documents.
# 2. Split documents into small, semantically meaningful chunks.
# 3. Embed each chunk to create an index.
# 4. Store indexes in vector stores for efficient retrieval.
# 5. Perform similarity searches to answer questions.
# 6. Handle edge cases in similarity search.
#############################################################

import os
import openai
from dotenv import load_dotenv, find_dotenv

# Load environment variables for OpenAI API
load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")

# ## Step 1: Load PDF Documents
# Load multiple PDF documents using `PyPDFLoader`. Here, a few duplicate documents are added to simulate messy data.

from langchain_community.document_loaders import PyPDFLoader # type: ignore

pdf_loaders = [
    # Duplicate documents on purpose - messy data
    PyPDFLoader("docs/cs229_lectures/sfbu-2024-2025-university-catalog-8-20-2024_1.pdf"),
    PyPDFLoader("docs/cs229_lectures/sfbu-2024-2025-university-catalog-8-20-2024_3.pdf"),
    PyPDFLoader("docs/cs229_lectures/sfbu-2024-2025-university-catalog-8-20-2024_1.pdf"),
    PyPDFLoader("docs/cs229_lectures/sfbu-2024-2025-university-catalog-8-20-2024_2.pdf")
]

# Load all documents into `docs` list
docs = []
for loader in pdf_loaders:
    docs.extend(loader.load())

# ## Step 2: Split Documents into Chunks
# Use `RecursiveCharacterTextSplitter` to divide each document into smaller, semantically meaningful chunks for embedding.

from langchain.text_splitter import RecursiveCharacterTextSplitter # type: ignore

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size = 1500,       # Size of each chunk
    chunk_overlap = 150      # Overlap between chunks to retain context
)

splits = text_splitter.split_documents(docs)

print(f"Total number of chunks: {len(splits)}")

# ## Step 3: Embed Each Chunk
# Embed each document chunk to create vectors for similarity search.

from langchain_openai import OpenAIEmbeddings # type: ignore

embedding = OpenAIEmbeddings()

# Example sentences to check similarity
sentence1 = "i like dogs"
sentence2 = "i like canines"
sentence3 = "the weather is ugly outside"

# Embed sentences and compute similarity using dot product
embedding1 = embedding.embed_query(sentence1)
embedding2 = embedding.embed_query(sentence2)
embedding3 = embedding.embed_query(sentence3)

import numpy as np
print("Similarity between sentence1 and sentence2:", np.dot(embedding1, embedding2))
print("Similarity between sentence1 and sentence3:", np.dot(embedding1, embedding3))
print("Similarity between sentence2 and sentence3:", np.dot(embedding2, embedding3))

# ## Step 4: Store Embeddings in a Vector Store
# Set up a vector store (Chroma) to store embeddings for document retrieval.

# Install chromadb package if not already installed
# !pip install chromadb

from langchain_community.vectorstores import Chroma # type: ignore

# Set directory for persistent storage of vector database
persist_directory = 'docs/chroma/'

# Remove old database files if present to avoid conflicts
os.system('rm -rf ./docs/chroma')

# Create vector store from document chunks
vectordb = Chroma.from_documents(
    documents = splits,
    embedding = embedding,
    persist_directory = persist_directory
)

print("\nTotal documents in vector store:", vectordb._collection.count())

# ## Step 5: Perform Similarity Search
# Run a similarity search using a sample question to find relevant documents.

question = "is there an email I can ask for help"
docs = vectordb.similarity_search(question, k=3)

print("\nNumber of documents retrieved:", len(docs))
print("Content of first retrieved document:", docs[0].page_content)

# Persist vector database for future use
# vectordb.persist()

# ## Step 6: Edge Case Handling in Similarity Search
# Simulate edge cases in similarity search, such as duplicate retrievals and specificity issues.

# Case 1: Duplicate chunks from similar documents
question = "what did they say about matlab?"
docs = vectordb.similarity_search(question, k=5)
print("\nContent of first duplicate document:", docs[0])
print("\nContent of second duplicate document:", docs[1])

# Case 2: Specificity issues - retrieves documents not directly relevant to the query
question = "what did they say about regression in the third lecture?"
docs = vectordb.similarity_search(question, k=5)

print("\nMetadata of retrieved documents for specificity test:")
for doc in docs:
    print(doc.metadata)

print("\nContent of least specific document:", docs[4].page_content)