import cv2
import numpy as np
import argparse
from PIL import Image, ImageFont, ImageDraw, ImageOps

# set arguments to be retrieved later
def get_args(img_name, complexity):
    img_name_inp = "inputs/" + img_name + ".jpg"
    img_name_out = "outputs/" + img_name + "_out_ASCII.jpg"
    args = argparse.ArgumentParser("Darren Gebler ImageToASCII")
    args.add_argument("--input", type=str, default=img_name_inp)  # Input image path
    args.add_argument("--output", type=str, default=img_name_out)  # Output image path
    args.add_argument("--complex", type=str, default=complexity)  # Number of chars to use
    args.add_argument("--columns", type=int, default=200)  # Default number of columns for output width
    args.add_argument("--scale", type=int, default=2)  # Scale for font size
    arguments = args.parse_args()
    return arguments


def core(args):
    if args.complex == "complex":  # Complex number of characters
        character_list = ' !"#$%&\'()*+,-./:;<=>?@[\]^_`{|}~AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0123456789'
    else:  # Simple number of characters
        character_list = ' !"#$%&'
    font = ImageFont.truetype("fonts/VeraMono-Bold.ttf", size=int(10 * args.scale))  # Setting font to be used
    number_chars = len(character_list)
    number_cols = args.columns
    image = cv2.imread(args.input)  # load input image
    image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)  # convert image to gray image
    height, width = image.shape  # return height and width of image
    sec_width = width / number_cols  # defines section width
    sec_height = 2 * sec_width  # defines section height
    number_rows = int(height / sec_height)  # defines number of rows
    char_width, char_height = font.getsize("Z")  # returns character height and width
    output_width = char_width * number_cols  # output image width
    output_height = char_height * number_rows * 2  # output image height
    output_image = Image.new("L", (output_width, output_height), 255)  # Allocates memory for new image. Mode: 8-bit pixels, black and white
    draw = ImageDraw.Draw(output_image)  # instantiates new image

    for x in range(number_rows):
        line = "".join([character_list[min(int(np.mean(
            image[int(x * sec_height):min(int((x + 1) * sec_height), height),
            int(y * sec_width):min(int((y + 1) * sec_width), width)]) * number_chars / 255), number_chars - 1)] for y
                        in range(number_cols)]) + "\n"  # logic behind picking character and printing to line
        draw.text((0, x * char_height), line, fill=0, font=font)

    cropped_image = ImageOps.invert(output_image).getbbox()  # calculates black border box

    output_image = output_image.crop(cropped_image)  # crops black box
    output_image.save(args.output)  # outputs final image


if __name__ == '__main__':
    print("Enter the Input Image Name:")
    img_name = input()
    print("Enter 'complex' or 'simple':")
    complexity = input()
    args = get_args(img_name, complexity)
    core(args)
