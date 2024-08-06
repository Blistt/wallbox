from tqdm import tqdm
import numpy as np
from pathlib import Path
import matplotlib.pyplot as plt
import tensorflow as tf
import PIL


def index_files(dir, prefix='wb'):
    '''
    Indexes files in a directory by renaming them with a prefix and a number.
    '''
    path = Path(dir)
    files = list(path.glob('*.*'))  # Get all files regardless of extension
    for i, file in enumerate(files):
        new_filename = f'{prefix}_{i}.jpg'
        if file != path / new_filename:
            file.rename(path / new_filename)
    print(f'Renamed {len(files)} files in {dir}')


def save_images(images, output_path):
    '''
    Saves retrieved images in a grid
    '''
    grid_size = int(np.ceil(np.sqrt(len(images))))
    fig = plt.figure(figsize=(10, 10))

    for i, img in enumerate(images):
        ax = fig.add_subplot(grid_size, grid_size, i+1)  # add 1 to i because subplot indices start from 1
        ax.imshow(img)
        ax.axis('off')

    plt.savefig(output_path)
    plt.close(fig)

    print(f"The grid of images was successfully saved to {output_path}")
    


def load_images(path, return_filenames=False):
  '''
  Loads images with keras.preprocessing.image.load_img for VGG19 pre-processing
  '''
  path = Path(path)
  # Ensures only valid image files are loaded
  img_paths = list(path.glob('*.jpg')) + list(path.glob('*.jpeg')) + list(path.glob('*.png')) \
              + list(path.glob('*.gif'))
  images = []
  filenames = []
  print(f'Loading {len(img_paths)} images')
  for img_path in tqdm(img_paths):
    # load image
    img = tf.keras.preprocessing.image.load_img(img_path, target_size=(224,224))
    images.append(img)
    filenames.append(img_path.name)
  print('images loaded as' , type(images[0]), 'type')
  
  if return_filenames:
    return images, filenames
  else:
    return images
  

def load_from_filenames(filenames, path='./dataset/images/'):
    '''
    Load images from a list of filenames
    '''
    # Remove .npy extension if present
    filenames = [filename.split('.')[0] for filename in filenames]
    images = []
    for filename in filenames:
        # Load image with PIL
        try:
          img = PIL.Image.open(f'{path}/{filename}.jpg')
          images.append(img)
        except:
           print(f'Error loading {filename}.jpg, skipping...')
    return images