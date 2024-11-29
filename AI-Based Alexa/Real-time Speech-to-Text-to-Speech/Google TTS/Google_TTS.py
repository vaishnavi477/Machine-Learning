import openai
import os
from dotenv import load_dotenv, find_dotenv
from gtts import gTTS
# from pathlib import Path

# Load environment variables for OpenAI API
load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")

def transcribe_audio_to_text(audio_file_path):
    """Transcribe audio file to text using OpenAI Whisper."""
    with open(audio_file_path, "rb") as audio_file:
        transcription = openai.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return transcription.text

def get_gpt_response(prompt):
    """Get a response to the given prompt using OpenAI GPT."""
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

def text_to_speech(text, output_path):
    """Convert text to speech using gTTS and save as an MP3 file."""
    tts = gTTS(text=text, lang="en", slow=False)
    tts.save(output_path)

def main():
    # Step 1: Transcribe the audio file
    input_audio_path = "audio.m4a"  # Replace with your audio file
    print(f"Transcribing audio from: {input_audio_path}")
    transcribed_text = transcribe_audio_to_text(input_audio_path)
    print(f"Transcription: {transcribed_text}")
    
    # Step 2: Get GPT-generated response based on the transcription
    print("Generating GPT response...")
    gpt_reply = get_gpt_response(transcribed_text)
    print(f"GPT Reply: {gpt_reply}")
    
    # Step 3: Convert GPT reply to speech
    output_speech_path = "/output/response_gtts.mp3"
    print(f"Converting GPT reply to speech and saving to: {output_speech_path}")
    text_to_speech(gpt_reply, output_speech_path)
    print("Process completed successfully!")

if __name__ == "__main__":
    main()
