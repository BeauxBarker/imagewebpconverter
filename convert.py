from flask import Flask, request, render_template, send_from_directory
import pandas as pd
from PIL import Image
import os
import zipfile
import io
import uuid
import requests

app = Flask(__name__)

# Create a directory to store the converted images
os.makedirs("converted_images", exist_ok=True)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle CSV file upload and conversion here
        uploaded_file = request.files['csv_file']
        if uploaded_file.filename != '':
            csv_data = pd.read_csv(uploaded_file)

            # Create a list to store the file names of the converted images
            converted_filenames = []

            # Add your conversion code here
            for index, row in csv_data.iterrows():
                image_url = row['ImageURL']

                # Fetch the image data from the URL
                response = requests.get(image_url)
                if response.status_code == 200:
                    image_data = response.content

                    # Perform the image conversion to WebP format and save it
                    converted_filename = f"converted_images/image_{str(uuid.uuid4())}.webp"
                    with open(converted_filename, "wb") as img_file:
                        img_file.write(image_data)
                    converted_filenames.append(converted_filename)

            # Create a zip file containing the converted images
            with zipfile.ZipFile('converted_images.zip', 'w') as zipf:
                for filename in converted_filenames:
                    zipf.write(filename)

            # Send the zip file for download
            return send_from_directory('', 'converted_images.zip', as_attachment=True)

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
