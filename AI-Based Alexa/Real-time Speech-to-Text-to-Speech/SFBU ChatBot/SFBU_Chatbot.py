import os
import openai
import datetime
from dotenv import load_dotenv, find_dotenv
from flask import Flask, request, jsonify, send_from_directory, send_file
from werkzeug.utils import secure_filename
from langchain_community.document_loaders import PyPDFLoader
from langchain_openai import OpenAIEmbeddings
from langchain_chroma import Chroma
from langchain_openai import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from pathlib import Path

# Load environment variables__
load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")

# Initialize Flask app
app = Flask(__name__)

# Directories
PDF_DIRECTORY = 'docs/cs229_lectures/'
PERSIST_DIRECTORY = 'docs/chroma/'

# Embedding function
embedding = OpenAIEmbeddings()

# Function to load PDFs and generate vector embeddings
def load_pdfs_and_store_embeddings(pdf_directory, persist_directory):
    pdf_files = [f for f in os.listdir(pdf_directory) if f.endswith('.pdf')]
    all_docs = []

    for pdf_file in pdf_files:
        pdf_path = os.path.join(pdf_directory, pdf_file)
        loader = PyPDFLoader(pdf_path)
        all_docs.extend(loader.load_and_split())
    
    return Chroma.from_documents(all_docs, embedding=embedding, persist_directory=persist_directory)

# Initialize vector store
vectordb = load_pdfs_and_store_embeddings(PDF_DIRECTORY, PERSIST_DIRECTORY)

# Initialize LLM
current_date = datetime.datetime.now().date()
llm_name = "gpt-3.5-turbo" if current_date >= datetime.date(2023, 9, 2) else "gpt-3.5-turbo-0125"
llm = ChatOpenAI(model=llm_name, temperature=0)

# Create retriever and memory
memory = ConversationBufferMemory(memory_key="chat_history", return_messages=True)
retriever = vectordb.as_retriever()

# Helper Functions
def transcribe_audio(audio_file):
    """Transcribe audio file to text using OpenAI Whisper."""
    response = openai.audio.transcriptions.create(model="whisper-1", file=audio_file)
    return response.text

def generate_gpt_response(prompt):
    """Generate a GPT response for the given prompt."""
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo-0125",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def text_to_speech_openai(text, output_path):
    """Convert text to speech using OpenAI's TTS."""
    try:
        response = openai.audio.speech.create(
            model="tts-1",  # Hypothetical model
            voice="nova",
            input=text
        )
        response.stream_to_file(output_path)
    except Exception as e:
        print(f"TTS processing failed: {e}")

# Routes
@app.route('/')
def index():
    """Serve the HTML file."""
    return send_from_directory('templates', 'index.html')

@app.route('/process-audio', methods=['POST'])
def process_audio():
    if 'audio' not in request.files:
        return jsonify({'error': 'No audio file provided'}), 400

    audio_file = request.files['audio']
    audio_path = "temp_audio_input.wav"
    audio_file.save(audio_path)

    try:
        transcription_text = transcribe_audio(open(audio_path, "rb"))
        docs = vectordb.similarity_search(transcription_text)
        context = "\n".join([doc.page_content for doc in docs])
        prompt = f"Use the following context to answer the question:\n\n{context}\n\nQuestion: {transcription_text}\nHelpful Answer:"
        gpt_response = generate_gpt_response(prompt)

        output_speech_path = Path("response_audio.mp3")
        text_to_speech_openai(gpt_response, output_speech_path)

        return jsonify({
            'transcription': transcription_text,
            'gptResponse': gpt_response,
            'audioUrl': str(output_speech_path)
        })
    except Exception as e:
        print(f"Error processing audio: {e}")
        return jsonify({'error': 'Processing failed'}), 500

@app.route('/response_audio.mp3')
def serve_audio():
    """Serve the generated audio file."""
    audio_file = "response_audio.mp3"
    try:
        return send_file(audio_file, as_attachment=False)
    except FileNotFoundError:
        return "Audio file not found", 404

# Run the Flask app
if __name__ == '__main__':
    app.run(debug=True)
