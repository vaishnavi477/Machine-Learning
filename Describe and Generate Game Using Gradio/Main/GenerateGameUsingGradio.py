import os
import io
import requests
import base64
from PIL import Image
from dotenv import load_dotenv, find_dotenv
import gradio as gr  # type: ignore # Gradio for creating UI
import tempfile

# Load environment variables from the .env file
load_dotenv(find_dotenv())
hf_api_key = os.getenv("HF_API_KEY")
TTI_ENDPOINT = os.getenv("HF_API_TTI_BASE")
ITT_ENDPOINT = os.getenv("HF_API_ITT_BASE")
TTS_ENDPOINT = os.getenv("HF_API_TTS_BASE")

# Function to generate an image from a text prompt
def generate_image(prompt):
    headers = {
        "Authorization": f"Bearer {hf_api_key}"
    }
    payload = {
        "inputs": prompt,
        "parameters": {
            "guidance_scale": 7.5,
            "num_inference_steps": 50
        }
    }
    
    response = requests.post(TTI_ENDPOINT, headers=headers, json=payload) # type: ignore
    
    # Process response to display image
    if response.status_code == 200:
        try:
            image_data = response.content
            image = Image.open(io.BytesIO(image_data))
            return image
        except Exception as e:
            print("Error processing image data:", e)
            raise
    else:
        print(f"Error {response.status_code}: {response.text}")
        raise Exception(f"Request failed with status code {response.status_code}. Details: {response.text}")

# Function to generate a caption from an uploaded image
def generate_caption(image):
    headers = {
        "Authorization": f"Bearer {hf_api_key}"
    }
    # Convert image to base64
    buffered = io.BytesIO()
    image.save(buffered, format="PNG")
    image_base64 = base64.b64encode(buffered.getvalue()).decode("utf-8")
    
    payload = {
        "inputs": image_base64
    }
    
    response = requests.post(ITT_ENDPOINT, headers=headers, json=payload) # type: ignore
    
    # Extract and return caption from response
    if response.status_code == 200:
        result = response.json()
        if isinstance(result, list) and len(result) > 0 and 'generated_text' in result[0]:
            return result[0]['generated_text']
        else:
            raise ValueError("Unexpected response structure from image captioning API")
    else:
        print(f"Error {response.status_code}: {response.text}")
        raise Exception(f"Request failed with status code {response.status_code}. Details: {response.text}")

# Function to generate audio from a text caption
def generate_audio(text):
    headers = {
        "Authorization": f"Bearer {hf_api_key}"
    }
    payload = {
        "inputs": text
    }
    
    response = requests.post(TTS_ENDPOINT, headers=headers, json=payload) # type: ignore
    
    # Process audio response and save to a temporary file
    if response.status_code == 200:
        audio_data = response.content
        # Save the audio to a specific file path
        output_audio_file = "Audios/generated_audio.wav"
        with open(output_audio_file, "wb") as f:
            f.write(audio_data)
        return output_audio_file  # Return the file path
    else:
        print(f"Error {response.status_code}: {response.text}")
        raise Exception(f"Request failed with status code {response.status_code}. Details: {response.text}")

# Combined function for generating caption, image, and audio
def caption_and_generate(image):
    caption = generate_caption(image)
    generated_image = generate_image(caption)
    audio_output = generate_audio(caption)
    return [caption, generated_image, audio_output]

# Gradio interface for user interaction
with gr.Blocks() as demo:
    gr.Markdown("Describe and Generate game")

    # UI elements: Image input, button, and output fields
    image_input = gr.Image(label="Upload an Image", type="pil")
    btn_all = gr.Button("Generate Caption, Image, and Audio")
    caption_output = gr.Textbox(label="Generated Caption")
    image_output = gr.Image(label="Generated Image")
    audio_output = gr.Audio(label="Generated Audio")
    
    # Define button action
    btn_all.click(fn=caption_and_generate, inputs=[image_input], outputs=[caption_output, image_output, audio_output])

# Launch the app with a shareable link
demo.launch(share=True)