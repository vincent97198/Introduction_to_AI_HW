import os
import readline
import cv2
import adaboost
import matplotlib.pyplot as plt

def detect(dataPath, clf):
    """
    Please read detectData.txt to understand the format. Load the image and get
    the face images. Transfer the face images to 19 x 19 and grayscale images.
    Use clf.classify() function to detect faces. Show face detection results.
    If the result is True, draw the green box on the image. Otherwise, draw
    the red box on the image.
      Parameters:
        dataPath: the path of detectData.txt
      Returns:
        No returns.
    """
    
    # Begin your code (Part 4)
    # raise NotImplementedError("To be implemented")
    clf = adaboost.Adaboost.load('clf_200_1_10')
    with open(dataPath,'r') as detect_file:
        while Line := detect_file.readline():
            [file_name,number_of_rec] = Line.split()
            number_of_rec = int(number_of_rec)
            image = cv2.imread(dataPath[:-14]+file_name,cv2.IMREAD_GRAYSCALE)
            print(dataPath[:-14])
            image_draw = cv2.imread(dataPath[:-14]+file_name,cv2.IMREAD_COLOR)
            for id in range(1,number_of_rec+1):
                Line = detect_file.readline()
                (x,y,x_len,y_len) = map(int,Line.split())
                # print(x,y,x+x_len,y+y_len)
                image_face = image[y:y+y_len,x:x+x_len]
                # cv2.imshow("image_face",image_face)
                if clf.classify(image_face) == True:
                    color = (0,255,0)
                else:
                    color = (0,0,255)
                cv2.rectangle(image_draw, (x, y), (x+x_len, y+y_len), color, 2)
            cv2.imwrite('new_'+file_name,image_draw)
    # End your code (Part 4)