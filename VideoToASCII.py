# Not currently working

import cv2
import numpy as np
import argparse
from PIL import Image, ImageFont, ImageDraw, ImageOps

def get_args(video_name, complexity):
    video_name_inp = "inputs/" + video_name + ".mp4"
    video_name_out = "outputs/" + video_name + "_out_ASCII.mp4"
    args = argparse.ArgumentParser("Darren Gebler VideoToASCII")
    args.add_argument("--input", type=str, default=video_name_inp)  # Input image path
    args.add_argument("--output", type=str, default=video_name_out)  # Output image path
    args.add_argument("--complex", type=str, default=complexity)  # Number of chars to use
    args.add_argument("--columns", type=int, default=100)  # Default number of columns for output width
    args.add_argument("--scale", type=int, default=2)  # Scale for font size
    args.add_argument("--fps", type=int, default=0)  # FPS of video
    arguments = args.parse_args()
    return arguments

def core(args):
    if args.complex == "complex":  # Complex number of characters
        character_list = ' !"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    else:  # Simple number of characters
        character_list = ' !"#$%&'
    font = ImageFont.truetype("fonts/VeraMono-Bold.ttf", size=int(10 * args.scale))  # Setting font to be used
    video_cap = cv2.VideoCapture(args.input)
    if args.fps == 0:
        fps = int(video_cap.get(cv2.CAP_PROP_FPS))
    else:
        fps = args.fps
    number_chars = len(character_list)
    num_columns = args.columns
    while video_cap.isOpened():
        flag, frame = video_cap.read()
        if flag:
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        else:
            break
        height, width = frame.shape
        sec_width = width/args.columns
        sec_height = 2 * sec_width
        num_rows = int(height/sec_height)

        if num_columns > width or num_rows > height:
            print("Too many columns or rows. Use default setting")
            cell_width = 6
            cell_height = 12
            num_columns = int(width / cell_width)
            num_rows = int(height / cell_height)

        char_width, char_height = font.getsize("Z")
        output_width = char_width * num_columns
        output_height = 2 * char_width * num_rows
        output_image = Image.new("L", (output_width, output_height), 255)
        draw = ImageDraw.Draw(output_image)

        for x in range(num_rows):
            line = "".join([character_list[min(int(np.mean(
                frame[int(x * sec_height):min(int((x + 1) * sec_height), height),
                int(y * sec_width):min(int((y + 1) * sec_width), width)]) * number_chars / 255), number_chars - 1)] for
                            y in range(num_columns)]) + "\n"  # logic behind picking character and printing to line
            draw.text((0, x * char_height), line, fill=0, font=font)

        cropped_image = ImageOps.invert(output_image).getbbox()
        output_image = output_image.crop(cropped_image)
        output_image = cv2.cvtColor(np.array(output_image), cv2.COLOR_GRAY2BGR)
        output_image = np.array(output_image)
        try:
            output
        except:
            output = cv2.VideoWriter(args.output, cv2.VideoWriter_fourcc(*"XVID"), fps, (output_image.shape[1], output_image.shape[0]))
        output.write(output_image)

    video_cap.release()
    output.release()

if __name__ == '__main__':
    print("Enter the Input Video Name:")
    img_name = input()
    print("Enter 'complex' or 'simple':")
    complexity = input()
    args = get_args(img_name, complexity)
    core(args)