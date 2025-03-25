import os
import io
import base64
import uuid
from PIL import Image
from flask import request

UPLOAD_FOLDER = "static/uploads"

# ✅ Ensure upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

def save_uploaded_image(file):
    """ Saves an uploaded image or captured image. Returns (filename, error_message) """
    if not file:
        return None, "No file selected!"

    try:
        filename = f"{uuid.uuid4()}_{file.filename}"
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)
        return filename, None  # ✅ Success
    except Exception as e:
        return None, f"Error saving uploaded image: {str(e)}"

def preprocess_image(image_path):
    """ Preprocesses the image for the AI model """
    from torchvision import transforms
    import torch

    transform = transforms.Compose([
        transforms.Resize((224, 224)),  # ✅ Ensure correct input size
        transforms.ToTensor(),
    ])

    image = Image.open(image_path).convert("RGB")
    return transform(image).unsqueeze(0)  # ✅ Add batch dimension

