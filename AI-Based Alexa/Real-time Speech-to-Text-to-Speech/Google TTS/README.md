# Audio Transcription, GPT, and Text-to-Speech Integration

This project integrates OpenAI's Whisper for audio transcription, GPT-3.5 for generating responses, and Google Text-to-Speech (gTTS) for converting text to speech.

## Features

- Transcribes an audio file to text using OpenAI Whisper.
- Sends the transcribed text to OpenAI GPT-3.5 to generate a relevant response.
- Converts the GPT-generated response to speech using gTTS and saves it as an MP3 file.

## Requirements

openai==0.27.0
python-dotenv==1.0.0
gtts==2.3.1

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/audio-gpt-tts.git
   cd audio-gpt-tts

2. Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

3. Set up your OpenAI API key:
    Create a .env file in the project root directory and add your API key:
    ```
    OPENAI_API_KEY=your_api_key_here
    ```

## Usage

1. Place an audio file (e.g., audio.m4a) in the project directory or specify the path to the audio file in the code.

2. Run the Google_TTS.py script:
    ```bash
    python3 Google_TTS.py
    ```
3. The process will:

    Transcribe the audio file to text.
    Use GPT to generate a response based on the transcription.
    Convert the GPT response to speech and save it as an MP3 file (response_gtts.mp3).


---

## `project_structure.txt`

This file will describe the structure of the project directory.

```txt
Google_TTS.py/
│
├── Google_TTS.py         # Main script that handles transcription, GPT response, and TTS
├── requirements.txt      # Project dependencies
├── README.md             # Project overview and setup instructions
├── project_structure.txt # Description of project structure
├── .env                  # Environment variables (e.g., OpenAI API key)
│
├── audio.m4a             # Example audio file to transcribe (replace with your own)
│
└── response_gtts.mp3     # Converted audio from GPT response 