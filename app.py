from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os
import requests

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Ensure the 'static/images' directory exists for storing generated images
if not os.path.exists('static/images'):
    os.makedirs('static/images')

# Function to generate an image using Stability AI API
def generate_image(prompt):
    api_url = "https://api.stability.ai/v2beta/stable-image/generate/core"
    api_key = "sk-H7NimWcSDiGHsOLB953vgsNBkSEvY75MoHvKT96h1LmE7ufX"  # Your API key
    
    # Make the API request to Stability AI
    response = requests.post(
        api_url,
        headers={
            "authorization": f"Bearer {api_key}",
            "accept": "image/*"
        },
        files={"none": ''}, 
        data={
            "prompt": prompt,
            "output_format": "webp",
        },
    )
    
    # Check if the request was successful
    if response.status_code == 200:
        image_name = f"generated_image_{prompt.replace(' ', '_')}.webp"
        image_path = os.path.join('static/images', image_name)
        
        # Save the generated image to the static/images directory
        with open(image_path, 'wb') as file:
            file.write(response.content)
        
        return image_name
    else:
        raise Exception(f"Image generation failed: {response.json()}")

# API route to generate the image
@app.route('/generate-image', methods=['POST'])
def generate_image_route():
    data = request.json
    prompt = data.get('prompt')

    if not prompt:
        return jsonify({"error": "Prompt is required"}), 400

    try:
        # Call the generate_image function using the provided prompt
        image_name = generate_image(prompt)
        return jsonify({"image_url": f"/static/images/{image_name}"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Serve static images
@app.route('/static/images/<path:filename>', methods=['GET'])
def serve_image(filename):
    return send_from_directory('static/images', filename)

# Route to serve the index.html file
@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(port=5000, debug=True)
