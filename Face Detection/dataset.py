import os
import cv2

def loadImages(dataPath):
    """
    load all Images in the folder and transfer a list of tuples. The first 
    element is the numpy array of shape (m, n) representing the image. 
    The second element is its classification (1 or 0)
      Parameters:
        dataPath: The folder path.
      Returns:
        dataset: The list of tuples.
    """
    # Begin your code (Part 1)
    # raise NotImplementedError("To be implemented")
    dataset = []
    data_path = dataPath + '/face'
    for image_path in os.listdir(data_path):
        image = cv2.imread(data_path+'/'+image_path,cv2.IMREAD_GRAYSCALE)
        dataset.append((image,1))
    data_path = dataPath + '/non-face'
    for image_path in os.listdir(data_path):
        image = cv2.imread(data_path+'/'+image_path,cv2.IMREAD_GRAYSCALE)
        dataset.append((image,0))
    # End your code (Part 1)
    return dataset