#!/usr/bin/env python3

import sys, os
import imageio as iio

if len(sys.argv) < 7:
	print("crop: crop images.")
	print("Usage: crop.py input_file output_file origin_x_0 origin_y_0 origin_x_1 origin_y_1")
	exit()

image_name = sys.argv[1]
image_out_name = sys.argv[2]
image = iio.imread(image_name)
origin_x_0 = int(sys.argv[3])
origin_y_0 = int(sys.argv[4])
origin_x_1 = int(sys.argv[5])
origin_y_1 = int(sys.argv[6])
image_crop = image[origin_y_0:origin_y_1+1, origin_x_0:origin_x_1+1]
iio.imwrite(image_out_name, image_crop)

print("Cropped image saved as", image_out_name)
