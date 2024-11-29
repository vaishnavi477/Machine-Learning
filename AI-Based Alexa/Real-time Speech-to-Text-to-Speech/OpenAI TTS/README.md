# AI Voice Interaction Project

## Overview

This project leverages OpenAI's Whisper model for speech-to-text transcription, GPT-3.5 for generating responses, and OpenAI's hypothetical TTS (Text-to-Speech) for converting text back into speech. The main functionality includes transcribing an audio file, generating a text-based response based on the transcription, and converting the response into an audio file.

## Features

- **Speech-to-Text**: Transcribes audio files to text using OpenAI Whisper.
- **AI Response Generation**: Uses GPT-3.5 to generate responses based on transcribed text.
- **Text-to-Speech**: Converts generated text responses into speech (hypothetical TTS from OpenAI).

## Requirements

openai==0.27.0
python-dotenv==0.21.0
requests==2.31.0

```bash
    pip install -r requirements.txt
```

## Setup
1. Clone the repository:
```bash
    git clone https://github.com/vaishnavi477/Machine-Learning/AI-Based Alexa/Real-time Speech-to-Text-to-Speech.git
    cd OpenAI TTS
```

2. Set up your OpenAI API key:
    Create a .env file in the project root and add your API key:
    ```
    OPENAI_API_KEY=your-openai-api-key-here
    ```

## Usage
Run the Openai_TTS.py script to transcribe an audio file, generate a response using GPT, and convert the response into speech:
```bash
python3 Openai_TTS.py
```

