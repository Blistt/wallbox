from flask import Flask, request, jsonify
from flask_cors import CORS
from pathlib import Path
from retrieval_scripts.model_loader import load_model
from retrieval_scripts.embedder import get_embeddings
from retrieval_scripts.knn_retriever import get_knn_for_query
from retrieval_scripts.utils import load_images
import joblib
import traceback

app = Flask(__name__)
CORS(app)

def retrieve_images(query_path='test_image/', image_embedding_path='dataset/embeddings/23'):
    try:
        # Load deep learning feature extractor
        print('Loading VGG19 model...')
        visual_model = load_model()

        # Load and embed query image
        print('Loading and embedding query image...')
        query_image = load_images(query_path)
        query_embedding = get_embeddings(visual_model, [23], query_image)

        # Load filenames
        dir_path = Path(image_embedding_path)
        emb_filenames = [f.name for f in dir_path.glob('*') if f.is_file()]

        # Load pre-fit knn model
        print('Loading KNN model...')
        knn_model = 'api/knnmodels/knnbr_50.joblib'
        knnbr = joblib.load(knn_model)

        # Retrieve query results from knn model
        print('Retrieving embeddings of query results...')
        knn_emb_filenames = get_knn_for_query(query_embedding, knnbr, emb_filenames)
        print(f'Retrieved {len(knn_emb_filenames)} embeddings')

        # Print filenames of retrieved images
        for emb_filename in knn_emb_filenames:
            print(emb_filename)

        return knn_emb_filenames
    except Exception as e:
        print('Error:', e)
        traceback.print_exc()
        raise e

@app.route("/api/retrieve_images", methods=["POST"])
def api_retrieve_images():
    query_path = request.json.get('query_path', 'public/uploaded_images/')
    image_embedding_path = request.json.get('image_embedding_path', 'public/dataset/embeddings/23')
    try:
        knn_emb_filenames = retrieve_images(query_path, image_embedding_path)
        return jsonify({"status": "success", "retrieved_images": knn_emb_filenames})
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
