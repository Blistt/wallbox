import tensorflow as tf
from pathlib import Path
import numpy as np
from tqdm import tqdm


def get_embeddings(visual_model, f_levels, images, filenames=None):
  '''
  Compute embeddings of images using the VGG19 model
  '''
  # Create a single string with all the f_levels
  levels = '_'.join([str(f) for f in f_levels])
  path = Path(f'./dataset/embeddings/{levels}')
  path.mkdir(parents=True, exist_ok=True)
  # Initialize embeddings
  E = []
  for i, img in enumerate(images):
    print('embedding image', i)
    img = np.expand_dims(img, axis=0)
    img = tf.keras.applications.vgg19.preprocess_input(img)       # Pre-processes image for VGG19
    # run an image through the network by making a prediction
    feature_maps = visual_model.predict(img)
    
    temp = np.zeros((0))
    for level in f_levels:
      A = feature_maps[level]
      # Flatten feature map to 2x2 matrix if it is 4D (e.g. Conv layer)
      if len(A.shape) == 4:
        A = A.reshape(A.shape[0], A.shape[1]*A.shape[2], A.shape[3], order='F')
        A = A.reshape(A.shape[1], A.shape[2])
        # Compute Gram matrix (cummulative co-activation of filter per layer)
        G = np.matmul(np.transpose(A),A)
        # Append this layer's flattened Gram matrix to images embedding
        dummy = np.zeros(temp.shape[0] + G.flatten().shape[0])
        dummy[:temp.shape[0]] = temp
        dummy[temp.shape[0]:] = G.flatten()
        emb = np.copy(dummy) 
      # Flatten feature map to 1D vector if it is 2D (e.g. FC layer)
      else:
        emb = np.copy(A.flatten())

    E.append(np.copy(emb))

    # convert layer names to a single string all of them concatenated
    layers = '_'.join([str(f) for f in f_levels])

    if filenames is not None:
      # save embeddings as .npy files
      filename = filenames[i].split('.')[0]
      np.save(f'./dataset/embeddings/{layers}/{filename}', emb)

    if i%10 == 0:
      print(f'Getting embedding of img no. {i}, with shape {E[i].shape}, and {len(f_levels)} layers')
    
  return np.array(E)


def load_precomp_embeddings(filenames, layer, path='./dataset/embeddings/', names=False):
    '''
    Load precomputed embeddings from disk
    '''
    embeddings = []
    filenames = []
    for filename in tqdm(filenames):
        emb = np.load(f'{path}/{layer}/{filename.split(".")[0]}.npy')
        embeddings.append(emb)
        filenames.append(filename.split(".")[0])
    if names:
        return embeddings, filenames
    else:
        return embeddings