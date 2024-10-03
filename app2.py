from flask import Flask, request, jsonify, render_template, send_from_directory
from flask_cors import CORS
import os
import requests

app = Flask(__name__, static_folder='static', template_folder='templates')
CORS(app)

# Ensure the 'static/images' directory exists for storing generated images
if not os.path.exists('static/images'):
    os.makedirs('static/images')

# Function to generate an image using DeepAI API
def generate_image(prompt):
    api_url = "https://api.deepai.org/api/text2img"
    api_key = "6e4f5606-b6d7-413c-8abe-ed03d6824242"  # Your DeepAI API key
    
    response = requests.post(
        api_url,
        headers={"api-key": api_key},
        data={"text": prompt}
    )
    
    # Print response for debugging
    print("API Response Status Code:", response.status_code)
    print("API Response Content:", response.text)

    # Check if the request was successful
    if response.status_code == 200:
        result = response.json()
        image_url = result.get("output_url")
        
        # Check if image URL is present in response
        if not image_url:
            raise Exception("No image URL returned by API")
        
        # Download the generated image from the provided URL
        image_response = requests.get(image_url)
        
        if image_response.status_code == 200:
            image_name = f"generated_image_{prompt.replace(' ', '_')}.jpg"
            image_path = os.path.join('static/images', image_name)
            
            # Save the generated image to the static/images directory
            with open(image_path, 'wb') as file:
                file.write(image_response.content)
            
            return image_name
        else:
            raise Exception(f"Failed to download the image: {image_response.status_code}")
    else:
        raise Exception(f"Image generation failed: {response.text}")

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
