from flask import Flask, request, jsonify
from flask_cors import CORS
import os
from werkzeug.utils import secure_filename
from predict import predict  # Import the predict function from predict.py
import torch
from torchvision import transforms
from PIL import Image

# Initialize Flask app
app = Flask(__name__)
CORS(app)

# Set up file upload folder
UPLOAD_FOLDER = 'uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

@app.route('/')
def hello_world():
    return "Hello World!"

# Helper function to check if a file is allowed
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

# Route for uploading and predicting
@app.route('/predict', methods=['POST'])
def upload_file():
    # Check if a file is part of the request
    if 'file' not in request.files:
        return jsonify({"error": "No file part"})
    
    file = request.files['file']
    
    # If the user did not select a file
    if file.filename == '':
        return jsonify({"error": "No selected file"})
    
    # If the file is allowed, save it
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(file_path)
        
        # Use the predict function from predict.py to get the disease name
        disease_name = predict(file_path)
        
        # Return the disease name (prediction based on file name)
        return jsonify({"disease": disease_name})

    return jsonify({"error": "File type not allowed"})

if __name__ == '__main__':
    # Create the upload folder if it doesn't exist
    if not os.path.exists(UPLOAD_FOLDER):
        os.makedirs(UPLOAD_FOLDER)
    
    app.run(debug=True)
