# Still to do: Optimise image run through, by reducing number of images in folder (time consuming).

import cv2
import numpy as np
from itertools import product
from get_components import get_component_images
import argparse

# Set arguments to be retrieved later
def get_args(video_name):
    vid_input = "inputs/" + video_name + ".mp4"
    vid_output = "outputs/" + video_name + "_out_Videos.mp4"

    args = argparse.ArgumentParser("Darren Gebler ImagesToVideo")
    args.add_argument("--input", type=str, default=vid_input)  # Input video path
    args.add_argument("--output", type=str, default=vid_output)  # Output video path
    args.add_argument("--images", type=str, default="images")  # PASCAL Image Data Set path
    args.add_argument("--imgsize", type=int, default=20)  # Size of each image
    args.add_argument("--fps", type=int, default=0)  # FPS of Video
    args.add_argument("--overratio", type=float, default=0.2)  # Video size Ratio
    arguments = args.parse_args()
    return arguments

# Core function behind finding images from PASCAL image data set
def core(args):
    video_cap = cv2.VideoCapture(args.input)  # Return input video
    height = int(video_cap.get(cv2.CAP_PROP_FRAME_HEIGHT))  # return height of Video
    width = int(video_cap.get(cv2.CAP_PROP_FRAME_WIDTH))  # return width of video
    if args.fps == 0:
        fps = int(video_cap.get(cv2.CAP_PROP_FPS))  # return fps of video
    else:
        fps = args.fps  # default fps 0
    output = cv2.VideoWriter(args.output, cv2.VideoWriter_fourcc(*"XVID"), fps, (width, height))  # defines variable
    # to be able to write to video using defined variables from input video
    images, avg_colours = get_component_images(args.images, args.imgsize)  # Returns images for PASCAL Image data set
    # and Average Colours of images

    while video_cap.isOpened():
        flag, frame = video_cap.read()  # return input video flags and frame of video
        if not flag:
            break
        blank_image = np.zeros((height, width, 3), np.uint8)  # Allocates memory for blank image

        for x, y in product(range(int(width/args.imgsize)), range(int(height/args.imgsize))):
            part_of_input = frame[y * args.imgsize: (y+1) * args.imgsize, x*args.imgsize: (x+1) * args.imgsize, :]  # Splitting video frame into segments
            part_of_avgcolour = np.sum(np.sum(part_of_input, axis=0), axis=0)/(args.imgsize ** 2)  # Calculating average
            # colour of segmented video frame
            matrices = np.linalg.norm(part_of_avgcolour - avg_colours, axis=1)  # Normalises segements average colour and
            # average colour retrieved form PASCAL set
            min_values = np.argmin(matrices)  # return minimum values along axis
            blank_image[y* args.imgsize: (y+1) * args.imgsize, x*args.imgsize: (x+1)*args.imgsize, :] = images[min_values]  # Add chosen PASCAL image to blank image in location of segmented input image
            if args.overratio:
                overlay = cv2.resize(frame, (int(width* args.overratio), int(height*args.overratio)))  # resize blank image
                blank_image[height-int(height*args.overratio):, width-int(width*args.overratio):,:] = overlay
            output.write(blank_image)  # write blank image to output video frame
        video_cap.release()  # release input video
        output.release()  # release output video

if __name__ == '__main__':
    print("Enter the Input Video Name: ")
    vid_name = input()
    args = get_args(vid_name)
    core(args)

