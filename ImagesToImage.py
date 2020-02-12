# Still to do: Optimise image run through, by reducing number of images in folder (time consuming).

import cv2
import numpy as np
from itertools import product
from get_components import get_component_images
import argparse


# set arguments to be retrieved later
def get_args(img_name):
    image_name_inp = "inputs/" + img_name + ".jpg"
    image_name_out = "outputs/" + img_name + "_out_Images.jpg"

    args = argparse.ArgumentParser("Darren Gebler ImagesToImage")
    args.add_argument("--input", type=str, default=image_name_inp)  # Input image path
    args.add_argument("--output", type=str, default=image_name_out)  # Output image path
    args.add_argument("--images", type=str, default="images")  # PASCAL Image Data Set path
    args.add_argument("--imgsize", type=int, default=20)  # Size of each image
    arguments = args.parse_args()
    return arguments

# Core function behind finding images from PASCAL image data set
def core(args):
    input_image = cv2.imread(args.input, cv2.IMREAD_COLOR)  # Return input image
    height, width, number_channels = input_image.shape  # Returns height, width and number of channels
    blank_image = np.zeros((height, width, 3), np.uint8)  # Allocates memory for blank image
    images, avg_colours = get_component_images(args.images, args.imgsize)  # Returns images for PASCAL Image data set
    # and Average Colours of images

    # Divides image into segments to find ideal PASCAL image
    for x, y in product(range(int(width / args.imgsize)), range(int(height / args.imgsize))):
        part_of_input = input_image[y * args.imgsize: (y + 1) * args.imgsize, x * args.imgsize: (x + 1) * args.imgsize,
                        :]  # Splitting image into segments
        part_of_avgcolour = np.sum(np.sum(part_of_input, axis=0), axis=0) / (args.imgsize ** 2)  # Calculating average
        # colour of segmented image
        matrices = np.linalg.norm(part_of_avgcolour - avg_colours, axis=1)  # Normalises segements average colour and
        # average colour retrieved form PASCAL set
        min_values = np.argmin(matrices)  # return minimum values along axis
        blank_image[y * args.imgsize: (y + 1) * args.imgsize, x * args.imgsize:(x + 1) * args.imgsize, :] = images[min_values]
        # Add chosen PASCAL image to blank image in location of segmented input image

    cv2.imwrite(args.output, blank_image)  # Write new image


if __name__ == '__main__':
    print("Enter the Input Image Name: ")
    img_name = input()
    args = get_args(img_name)
    core(args)
