import torch
from diffusers import StableDiffusionPipeline
from flask import Flask, request, jsonify
import os
import base64
import requests

# Initialize Flask app
app = Flask(__name__)

# Load Stable Diffusion model
model_id = "CompVis/stable-diffusion-v1-4"  # You can change this to another model if needed
device = "cuda" if torch.cuda.is_available() else "cpu"  # Use GPU if available

# Create the pipeline for Stable Diffusion
pipe = StableDiffusionPipeline.from_pretrained(model_id, torch_dtype=torch.float16).to(device)

GEMINI_API_KEY = os.environ.get("Add gemini api key here")
GEMINI_API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro-vision:generateContent"

def describe_image_with_gemini(image_path):
    # Read and encode the image as base64
    with open(image_path, "rb") as img_file:
        img_base64 = base64.b64encode(img_file.read()).decode("utf-8")
    # Prepare the Gemini API payload
    payload = {
        "contents": [
            {
                "parts": [
                    {
                        "inline_data": {
                            "mime_type": "image/jpeg",
                            "data": img_base64
                        }
                    },
                    {
                        "text": "Describe the content of this image in detail."
                    }
                ]
            }
        ]
    }
    params = {"key": GEMINI_API_KEY}
    response = requests.post(GEMINI_API_URL, params=params, json=payload)
    if response.status_code == 200:
        result = response.json()
        # Extract the generated text
        return result["candidates"][0]["content"]["parts"][0]["text"]
    else:
        raise Exception(f"Gemini API error: {response.text}")

@app.route('/generate-image', methods=['POST'])
def generate_image():
    data = request.json
    prompt = data.get("prompt")

    # Generate image
    try:
        with torch.no_grad():
            image = pipe(prompt)["sample"][0]

        # Save image to a file
        image_path = "generated_image.png"
        image.save(image_path)

        return jsonify({"message": "Image generated successfully", "image_path": image_path})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/describe-image', methods=['POST'])
def describe_image_route():
    data = request.json
    image_name = data.get("image_name")
    if not image_name:
        return jsonify({"error": "Image name is required"}), 400
    image_path = os.path.join("static", "images", image_name)
    if not os.path.exists(image_path):
        return jsonify({"error": "Image not found"}), 404
    try:
        description = describe_image_with_gemini(image_path)
        return jsonify({"description": description}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Ensure the model is downloaded and ready
    os.makedirs("generated_images", exist_ok=True)
    app.run(debug=True)
