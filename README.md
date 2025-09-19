# AI Text-to-Image Generator

This project is an AI-powered application that converts text prompts into images using advanced deep learning models. The application uses two different APIs for testing and production: Stability.ai for testing purposes and Deep.ai for the actual model. The system allows users to input a description, and the model will generate an image based on that text.

## Tools and Technologies Used

- **Python**: The backend is written in Python.
- **Stability.ai API**: Used for testing purposes. The API key for this service is utilized in `app.py`.
- **Deep.ai API**: This will be the primary API for generating images in the final model. The API key for this service is referenced in `app2.py`.
- **Google Gemini API**: Used in `img_to_text_to_img.py` for generating image descriptions from images.
- **Flask**: A lightweight WSGI web application framework for building the backend of the project.
- **HTML/CSS**: Used for building the front-end of the application.
- **JavaScript**: Utilized for handling the image generation requests from the client side and processing responses.

## How It Works

1. **User Input**: Users provide a description of the image they want to generate in a text field.
2. **Backend Processing**:
   - For testing, the input is sent to the Stability.ai API via the `app.py` file, which processes the text and returns an image.
   - For actual deployment, the input will be sent to the Deep.ai API via the `app2.py` file.
   - For image-to-text description, the image is sent to the Gemini API via the `img_to_text_to_img.py` file, which returns a detailed description of the image content.
3. **Image Generation/Description**: The generated image is then returned to the user, displayed on the webpage, and can be downloaded. For image description, the generated text is returned to the user.

## API Keys

- **Stability.ai API Key**: Used in `app.py` for testing the image generation.
- **Deep.ai API Key**: Used in `app2.py` for the final version of the image generator.
- **Google Gemini API Key**: Used in `img_to_text_to_img.py` for generating text descriptions from images.

## Screenshots

### Screenshot 1: User Interface
![Screenshot 1](./screenshot1.png)

### Screenshot 2: Generated Image Example
![Screenshot 2](./screenshot2.png)

## Technologies and Tools Used

<div style="display: flex; align-items: center; justify-content: space-around;">
    <img src="https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg" alt="Python" width="60">
    <img src="static\images\flask.jpg" alt="Flask" width="100">
    <img src="static\images\stabilityai.jpg" alt="Stability.ai" width="108">
    <img src="static\images\deepai.jpg" alt="Deep.ai" width="100">
    <img src="static\images\gemini.jpg" alt="Gemini" width="100">
</div>

- **Python**: Programming language used to develop the backend.
- **Flask**: Framework used for creating the web application.
- **Stability.ai**: API for testing text-to-image generation.
- **Deep.ai**: API for the production model of text-to-image generation.
- **Google Gemini**: API for generating detailed text descriptions from images.

## File Structure

```
.
├── app.py                 # Backend using Stability.ai for testing
├── app2.py                # Backend using Deep.ai for actual image generation
├── img_to_text_to_img.py  # Backend using Stable Diffusion and Gemini API for image generation and image-to-text description
├── templates/
│   └── index.html         # Frontend interface for user input
├── static/
│   ├── style.css          # CSS styles
│   ├── script.js          # JavaScript for handling front-end actions
│   └── images/            # Directory for storing images used for description
└── README.md              # This readme file
```

### `img_to_text_to_img.py`

- Uses the Stable Diffusion model (via HuggingFace Diffusers) to generate images from text prompts.
- Provides an endpoint to generate images from text (`/generate-image`).
- Provides an endpoint to generate detailed descriptions of images using the Google Gemini API (`/describe-image`). Images are read from the `static/images` directory.
- Requires a valid Gemini API key set in the environment.
- Example usage:
  - POST to `/generate-image` with JSON: `{"prompt": "your description"}`
  - POST to `/describe-image` with JSON: `{"image_name": "your_image.jpg"}`

HAPPY CODING!!