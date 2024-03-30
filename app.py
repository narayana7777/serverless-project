from flask import Flask, render_template, request
import os
import pytesseract
from PIL import Image
import boto3

pytesseract.pytesseract.tesseract_cmd = "C:\Users\Narayana\Downloads\tesseract-ocr-w64-setup-5.3.3.20231005.exe"
# Create a Flask application instance

app = Flask(__name__)

# Ensure the 'uploads' directory exists
uploads_dir = os.path.join(app.instance_path, 'uploads')
os.makedirs(uploads_dir, exist_ok=True)

# Define routes and their corresponding functions
@app.route('/')
def index():
    return render_template('index.html', recognized_text='')

@app.route('/upload', methods=['POST'])
def upload():
    # Get uploaded image
    uploaded_file = request.files['image']
    if uploaded_file.filename != '':
        # Save the uploaded image to the 'uploads' directory
        image_path = os.path.join(uploads_dir, uploaded_file.filename)
        uploaded_file.save(image_path)
        # Perform text recognition using Tesseract
        recognized_text = pytesseract.image_to_string(Image.open(image_path))
        # Render the template with recognized text
        return render_template('index.html', recognized_text=recognized_text)
    else:
        return render_template('index.html', recognized_text='No image uploaded.')

# Run the Flask application if this script is executed
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
