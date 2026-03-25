# from TTS.api import TTS
# import torch

# # Detect best device
# if torch.cuda.is_available():
#     device = "cuda"
# elif torch.backends.mps.is_available():
#     device = "mps"
# else:
#     device = "cpu"
    


# print(f"Using device: {device}")
# print(TTS().list_models())


# # Load model (keep gpu=False, we control device manually)
# tts = TTS(
#     model_name="tts_models/multilingual/multi-dataset/xtts_v2",
#     gpu=False
# )

# # Move model to selected device
# tts.to(device)

# # Pure Hindi text
# text = "नमस्ते, मेरा नाम गणेश है। यह हिंदी टेक्स्ट टू स्पीच का परीक्षण है।"

# # Generate audio
# tts.tts_to_file(
#     text=text,
#     language="hi",
#     speaker="Craig Gutsy",
#     file_path="hindi_output.wav"
# )


# import torch
# from transformers import VitsModel, VitsTokenizer
# import soundfile as sf

# # Detect device (CUDA > MPS > CPU)
# if torch.cuda.is_available():
#     device = "cuda"
# elif torch.backends.mps.is_available():
#     device = "mps"
# else:
#     device = "cpu"

# print(f"Using device: {device}")

# # Load model
# model_name = "facebook/mms-tts-hin"
# tokenizer = VitsTokenizer.from_pretrained(model_name)
# model = VitsModel.from_pretrained(model_name).to(device)

# # Hindi text
# text = "नमस्ते, आप कैसे हैं? यह हिंदी टेक्स्ट टू स्पीच है।"

# # Tokenize and move to device
# inputs = tokenizer(text, return_tensors="pt")
# inputs = {k: v.to(device) for k, v in inputs.items()}

# # Generate speech
# with torch.no_grad():
#     output = model(**inputs).waveform

# # Move back to CPU for saving
# audio = output.squeeze().cpu().numpy()

# # Save audio
# sf.write("hindi_output.wav", audio, 16000)

# print("Audio saved as hindi_output.wav")

import requests

API_URL = "https://api-inference.huggingface.co/models/Vai22/kumaoni-english-translator"
headers = {"Authorization": "Bearer YOUR_HF_TOKEN"}

def query(payload):
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

print(query({"inputs": "Hello"}))