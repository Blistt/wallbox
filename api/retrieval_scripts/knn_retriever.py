from pathlib import Path
from retrieval_scripts.model_loader import load_model
from retrieval_scripts.embedder import get_embeddings
from retrieval_scripts.utils import load_images
import joblib
import traceback


'''
This file implements a function to retrieve the k nearest neighbors of a query image
using a pre-fit KNN model from the sklearn library.
'''

def get_knn_for_query(query_embedding, knnbr, filenames):
  query_embedding = query_embedding.reshape(1, -1)

  # Get the neighbors of the query image
  knn = knnbr.kneighbors(query_embedding)
            
  # GETS THE IMAGES OF THE KNN
  knn_filenames = []
  # Retrieve the k nearest neighbor images of the query image 
  print(f'there are {len(filenames)} filenames')
  for i, index in enumerate(knn[1][0][0:]):
    filename = filenames[index].split('.')[0]
    distance = knn[0][0][i]
    print(f'filename: {filename}, distance: {distance}')
    knn_filenames.append(filename)

  return knn_filenames


def retrieve_images(query_path='public/uploaded_images/', image_embedding_path='public/dataset/embeddings/23'):
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

        return knn_emb_filenames
    except Exception as e:
        print('Error:', e)
        traceback.print_exc()
        raise e