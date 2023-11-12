from flask import Flask, request, render_template, send_file
import pandas as pd
from PIL import Image
import zipfile
import io
import uuid
import requests

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        # Handle CSV file upload and conversion here
        uploaded_file = request.files['csv_file']
        if uploaded_file.filename != '':
            csv_data = pd.read_csv(uploaded_file)

            # Create a list to store the converted images
            converted_images = []

            # Add your conversion code here
            for index, row in csv_data.iterrows():
                image_url = row['Images']

                # Fetch the image data from the URL
                response = requests.get(image_url)
                if response.status_code == 200:
                    image_data = response.content

                    # Perform the image conversion to WebP format
                    with Image.open(io.BytesIO(image_data)) as img:
                        img_byte_io = io.BytesIO()
                        img.save(img_byte_io, format='WebP')

                    # Add the converted image to the list
                    converted_images.append(
                        (img_byte_io.getvalue(), f"image_{index}.webp"))

            # Create a ZIP archive in memory
            zip_buffer = io.BytesIO()
            with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED, False) as zipf:
                for img_data, img_name in converted_images:
                    zipf.writestr(img_name, img_data)

            # Move the cursor to the beginning of the ZIP buffer
            zip_buffer.seek(0)

            # Serve the ZIP archive as a downloadable file
            return send_file(zip_buffer, as_attachment=True, download_name='converted_images.zip', mimetype='application/zip')

    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
