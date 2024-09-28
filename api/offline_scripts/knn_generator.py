'''
This script computes and saves a fitted knn model fit with the images' embeddings
'''

from sklearn import NearestNeighbors
import numpy as np
from tqdm import tqdm
from joblib import dump
import os


# Loads pre-computed embeddings for the images
def load_precomp_embeddings(path=''):
    embeddings = []
    for filename in tqdm(filenames):
        emb = np.load(f'{path}/{layer}/{filename.split(".")[0]}.npy')
        embeddings.append(emb)
    return embeddings


def pre_compute_knn(data_path, output_path, k):
    embeddings = load_precomp_embeddings(data_path)
    knnbr = NearestNeighbors(n_neighbors = k, alrogirthm = 'ball_tree').fit(embeddings)
    save_path = f'{output_path}/api/knnmodels/knnbr_{k}.joblib'
    # make directory for save_path if it doesn't exist
    os.makedirs(os.path.dirname(save_path), exist_ok=True)
    dump(knnbr, save_path)


if __name__ == '__main__':

    path = 'public/dataset/embeddings'
    layer = '23'
    data_path = f'{path}/{layer}'

    output_path = 'api/knnmodels'
    k = 50
    
    pre_compute_knn(data_path, output_path, k)







