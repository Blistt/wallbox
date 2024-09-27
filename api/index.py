from flask import Flask, request, jsonify
from flask_cors import CORS
from s3_utils.s3_retrieve import get_image_url
from retrieval_scripts.knn_retriever import retrieve_images
import json

app = Flask(__name__)
CORS(app)  # Enable CORS for all routes

@app.route("/api/retrieve_images", methods=["POST"])
def api_retrieve_images():
    query_path = request.json.get('query_path', 'public/uploaded_images/')
    image_embedding_path = request.json.get('image_embedding_path', 'public/dataset/embeddings/23')
    try:
        knn_emb_filenames = retrieve_images(query_path, image_embedding_path)
        print('Succesfully identified filenames of images to be retrieved')

        with open('image_mapping.json', 'r') as f:
            mapping = json.load(f)
    
        # Get pre-signed S3 urls
        urls = {}
        for filename in knn_emb_filenames:
            s3_filename = mapping.get(filename)
            urls[filename] = get_image_url(s3_filename)
        return jsonify(urls)

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
