import openai
import os
from dotenv import load_dotenv, find_dotenv
from pathlib import Path

# Load environment variables for OpenAI API
load_dotenv(find_dotenv())
openai.api_key = os.getenv("OPENAI_API_KEY")

def transcribe_audio(audio_path):
    """Transcribe audio file to text using OpenAI Whisper."""
    with open(audio_path, "rb") as audio_file:
        response = openai.audio.transcriptions.create(
            model="whisper-1",
            file=audio_file
        )
    return response.text

def generate_gpt_response(prompt):
    """Generate a GPT response for the given prompt."""
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ]
    )
    return response.choices[0].message.content

import requests  # Make sure to import requests if you plan to download the audio using a URL

def save_audio_to_file(response, output_path):
    """Save the audio response to a file, checking if it's a URL or direct binary data."""
    # Check if the response contains a URL or binary data directly
    if hasattr(response, 'url'):
        # If the response contains a URL to the audio content
        audio_url = response.url
        audio_data = requests.get(audio_url).content
        with open(output_path, "wb") as audio_file:
            audio_file.write(audio_data)
    elif hasattr(response, 'audio_data'):  # Hypothetical attribute for direct binary data
        # If the response directly contains binary audio data
        with open(output_path, "wb") as audio_file:
            audio_file.write(response.audio_data)
    else:
        raise ValueError("Unexpected response format. Unable to save audio.")

def text_to_speech_openai(text, output_path):
    """Convert text to speech using OpenAI's TTS (hypothetical)."""
    try:
        response = openai.audio.speech.create(
            model="tts-1",  # Hypothetical model name for OpenAI TTS
            voice="nova",
            input=text
            # stream=True  # Enable streaming if supported # type: ignore
        )
        response.stream_to_file(output_path)
    except AttributeError as e:
        print("The TTS feature is not available in the OpenAI API.")
        print(e)
    except ValueError as e:
        print("Error saving audio.")
        print(e)

def main():
    # File paths
    input_audio_path = "audio.m4a"  # Input audio file
    output_speech_path = Path(__file__).parent / "response_openai.mp3"  # Output speech file

    # Step 1: Transcribe the input audio file to text
    print("Transcribing audio...")
    transcription_text = transcribe_audio(input_audio_path)
    print(f"Transcription: {transcription_text}")

    # Step 2: Generate GPT response
    print("Generating GPT response...")
    gpt_response = generate_gpt_response(transcription_text)
    print(f"GPT Response: {gpt_response}")

    # Step 3: Convert GPT response to speech using OpenAI's TTS (hypothetical)
    print(f"Converting GPT response to speech and saving to: {output_speech_path}")
    text_to_speech_openai(gpt_response, output_speech_path)
    # print("Speech generation completed successfully!")

if __name__ == "__main__":
    main()
