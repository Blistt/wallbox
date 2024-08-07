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
  for i in knn[1][0][1:]:
    filename = filenames[i].split('.')[0] + '.jpg'  # Replace .npy with .jpg for image retrieval
    knn_filenames.append(filename)

  return knn_filenames