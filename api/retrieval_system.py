'''
This file assembles the entire modularized image retrieval system that
returns a list of neighbors given a query image.
'''
from pathlib import Path
from model_loader import load_model
from embedder import get_embeddings
from knn_retriever import get_knn_for_query
from utils import load_images, load_from_filenames, save_images
import joblib

def retrieve_images(query_path='test_image/'):
    # Load deep learning feature extractor
    print('Loading VGG19 model...')
    visual_model = load_model()

    # Load and embed query image
    print('Loading and embedding query image...')
    query_image = load_images(query_path)
    query_embedding = get_embeddings(visual_model, [23], query_image)

    # Load filenames
    dir_path = Path('dataset/embeddings/23')
    emb_filenames = [f.name for f in dir_path.glob('*') if f.is_file()]

    # Load pre-fit knn model
    print('Loading KNN model...')
    knn_model = 'models/knnbr_50.joblib'
    knnbr = joblib.load(knn_model)

    # Retrieve query results from knn model
    print('Retrieving embeddings of query results...')
    knn_emb_filenames = get_knn_for_query(query_embedding, knnbr, emb_filenames)
    print(f'Retrieved {len(knn_emb_filenames)} embeddings')

    # Function to display query results (not to be deployed, only for dev testing purposes)
    print('Loading images from embeddings...')
    knn_images = load_from_filenames(knn_emb_filenames, path='dataset/images/')
    print(f'Retrieved {len(knn_images)} images')

    # Save retrieved images in a grid
    save_images(knn_images, 'retrieved_images.png')

if __name__ == '__main__':
    retrieve_images()