from flask import Flask
from pathlib import Path

app = Flask(__name__)

@app.route("/api/python")
def hello_world():
    # get all the elements of the public directory in the parent directory
    public_images_dir = Path(__file__).parent.parent / 'public' / 'uploaded_images'
    files = list(public_images_dir.glob('*'))
    if files:
        path = files[0]  # get the first file
    else:
        path = "No files found in the directory"
    return str(path)
