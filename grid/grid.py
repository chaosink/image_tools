#!/usr/bin/env python3

import sys
import imageio as iio
import numpy as np

if len(sys.argv) < 5:
	print("grid: Generate a grid of an image.")
	print("Usage: grid.py input_image output_image row column")
	exit()

image_name = sys.argv[1]
image_out_name = sys.argv[2]
r = int(sys.argv[3])
c = int(sys.argv[4])

image = iio.imread(image_name)
h = image.shape[0]
w = image.shape[1]
channel = image.shape[2]
grid = np.zeros([h * r, w * c, channel], dtype=image.dtype)

for x in range(r):
	for y in range(c):
		grid[h*x:h*x+h, w*y:w*y+w] = image


# for x in range(r):
# 	for y in range(c):
# 		for xb in range(w):
# 			for yb in range(h):
# 				xx = x * w + xb
# 				yy = y * h + yb
# 				grid[xx][yy] = image[xb][yb]

iio.imwrite(image_out_name, grid)

print("Grid image saved as", image_out_name)
