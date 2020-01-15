#!/usr/bin/env python3

import sys
import imageio as iio

if len(sys.argv) < 3:
	print("crop_blender_view: Cut off borders of camera view.")
	print("Usage: crop_blender_view.py input_file output_file")
	exit()

image_name = sys.argv[1]
image_out_name = sys.argv[2]
image = iio.imread(image_name)
shape = image.shape

i = 0
not_found = True
while not_found:
	for j in range(shape[1]):
		if image[i][j][0] == 57:
			x0 = i
			not_found = False
			break
	i += 1

i = shape[0] - 1
not_found = True
while not_found:
	for j in range(shape[1]):
		if image[i][j][0] == 57:
			x1 = i
			not_found = False
			break
	i -= 1

j = 0
not_found = True
while not_found:
	for i in range(shape[0]):
		if image[i][j][0] == 57:
			y0 = j
			not_found = False
			break
	j += 1

j = shape[1] - 1
not_found = True
while not_found:
	for i in range(shape[0]):
		if image[i][j][0] == 57:
			y1 = j
			not_found = False
			break
	j -= 1

image_crop = image[x0+2:x1-1, y0+2:y1-1]
iio.imwrite(image_out_name, image_crop)

print("Cropped image saved as", image_out_name)
