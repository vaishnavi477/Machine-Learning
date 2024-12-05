# SFBU ChatBot

## Overview
The SFBU ChatBot is a Flask-based AI-powered web application that:
- Transcribes user speech into text using OpenAI Whisper.
- Searches context-relevant information from PDF files using LangChain and ChromaDB.
- Generates intelligent responses using OpenAI's GPT model.
- Converts the responses to speech and plays them back for users.

## Features
- Speech-to-Text: Transcribes audio recordings to text.
- Contextual Chat: Fetches information from lecture PDFs using embeddings.
- Text-to-Speech: Converts GPT responses to audio using OpenAI's TTS.
- Responsive UI: Built with Bootstrap, ensuring a user-friendly interface.

## Installation

### Prerequisites
- Python 3.8 or higher
- OpenAI API key
- Flask

### Steps
1. Clone the repository:
   ```bash
   git clone https://github.com/vaishnavi477/AI-Based Alexa/Real-time Speech-to-Text-to-Speech.git
   cd SFBU_ChatBot

2. Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Add your OpenAI API key in the .env file:
    ```bash
    OPENAI_API_KEY=your_openai_api_key
    ```

4. Place your lecture PDFs in the docs/cs229_lectures/ directory.

5. Run the application:
    ```bash
    python3 SFBU_ChatBot.py
    ```

6. Open your browser and visit: http://127.0.0.1:5000

## File Structure

    SFBU_ChatBot.py: Backend application logic.
    templates/index.html: Frontend for the chatbot UI.
    docs/cs229_lectures/: Directory for lecture PDFs.
    docs/chroma/: Storage for vector embeddings.
