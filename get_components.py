import cv2
import glob
import numpy as np

# returns images from PASCAL data set, and their avg colours
def get_component_images(imagesPath, imgsize):
    images = []
    avg_colours = []

    for image_path in glob.glob("{}/*.png".format(imagesPath)) + glob.glob("{}/*.jpg".format(imagesPath)):
        images_temp = cv2.imread(image_path, cv2.IMREAD_COLOR)
        images_temp = cv2.resize(images_temp, (imgsize, imgsize))
        images.append(images_temp)
        avg_colours.append(np.sum(np.sum(images_temp, axis=0), axis=0)/(imgsize**2))

    return images, np.array(avg_colours)