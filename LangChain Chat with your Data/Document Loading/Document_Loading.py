# -------------------------
# Document Loading for Retrieval-Augmented Generation (RAG)
# -------------------------

# This script demonstrates loading and processing documents from various sources, such as PDFs, YouTube transcripts, web pages, 
# and Notion pages. The content from these sources is broken down into smaller, manageable chunks, optimized for quick retrieval 
# and enabling a large language model (LLM) to answer queries based on specific document content.

# ## Setup: Import Libraries and Load API Keys
# The script requires environment setup for API keys and other configuration variables.
# Ensure all necessary libraries are installed, and set up API keys via environment variables.

import os
import openai
from dotenv import load_dotenv, find_dotenv
from langchain_community.document_loaders import PyPDFLoader, WebBaseLoader, NotionDirectoryLoader # type: ignore
from langchain_community.document_loaders.generic import GenericLoader # type: ignore
from langchain_community.document_loaders.parsers.audio import OpenAIWhisperParser # type: ignore
from langchain_community.document_loaders import YoutubeAudioLoader # type: ignore

# Load environment variables for OpenAI API and User-Agent (if required by web requests).
load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")
user_agent = os.getenv("USER_AGENT")

# If USER_AGENT is required, set it in headers for requests.
headers = {"User-Agent": user_agent} if user_agent else {}
print("USER_AGENT loaded successfully.\n")

# -------------------------
# Document Sources Loading
# -------------------------

# ### Load PDFs
# Use the `PyPDFLoader` to load PDFs, breaking down the content into separate pages to manage document size and enable efficient retrieval.
pdf_loader = PyPDFLoader("docs/cs229_lectures/sfbu-2024-2025-university-catalog-8-20-2024.pdf")
pages = pdf_loader.load()

# Display page count and a preview of the first page’s content.
print(f"PDF loaded with {len(pages)} pages.")
print("\nPreview of first page content:")
print(pages[1].page_content[:500])  # Display first 500 characters of the first page's content

# ### Load YouTube Transcript
# Load audio from a YouTube video, transcribing it with the Whisper API. Make sure `yt-dlp` and `pydub` are installed.
# - This method saves the audio, parses it, and stores the transcription.
# - Install `yt-dlp` and `pydub` locally with: `!pip install yt_dlp pydub`

youtube_url = "https://www.youtube.com/watch?v=kuZNIvdwnMc"
save_dir = "docs/youtube/"
youtube_loader = GenericLoader(
    YoutubeAudioLoader([youtube_url], save_dir),
    OpenAIWhisperParser()
)
docs = youtube_loader.load()

# Display a preview of the YouTube transcript.
print("\nYouTube Transcript Preview:")
print(docs[0].page_content[:500])  # Display the first 500 characters

# ### Load Webpage Content
# Use `WebBaseLoader` to load content from a specified URL. This can be useful for capturing specific content from websites.
# Pass `headers` with USER_AGENT if needed.

# Load content from a specific URL
web_loader = WebBaseLoader("https://www.sfbu.edu/student-health-insurance")
web_docs = web_loader.load()

# Process the webpage content to remove blank lines
web_content = web_docs[0].page_content  # Access the content
cleaned_content = "\n".join([line.strip() for line in web_content.splitlines() if line.strip()])

# Display the cleaned content (first 500 characters as an example)
print("\nWebpage Content Preview:")
print(cleaned_content[:500])

# ### Load Notion Page Content
# Load documents stored in Notion by specifying the Notion directory path. The content is expected to be in Markdown format.

notion_loader = NotionDirectoryLoader("docs/Notion_DB")
notion_docs = notion_loader.load()

# Display a preview of Notion document content and its metadata.
print("\nLength: ", len(notion_docs))
print("\nNotion Document Content Preview:\n")
print(notion_docs[0].page_content[:200])  # Display the first 200 characters
print("\nNotion Document Metadata:\n")
print(notion_docs[0].metadata)

# -------------------------
# End of Document Loading Script
# -------------------------

# Each document is now loaded, processed, and stored in a structure suitable for retrieval, allowing an LLM to use this content 
# for answering specific questions based on the document's details.