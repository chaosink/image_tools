#!/usr/bin/env python3

import sys
import numpy as np
import imageio as iio

if len(sys.argv) < 4:
	print("stitch:")
	print("	Stitch multiple images into an array form.")
	print("Usage:")
	print("	stitch.py size output_file [input_files]...")
	print("Example:")
	print("	stitch.py 2x3 merge.png 1_1.png 1_2.png 1_3.png 2_1.png 2_2.png 2_3.png")
	print("	'size' is 2x3, so 2x3=6 images are input in order.")
	print("Notes:")
	print("	Input images must be of the same size.")
	exit()

size = sys.argv[1]
split = size.find('x')
y = int(size[0:split])
x = int(size[split+1:])

if len(sys.argv) < x*y+2:
	print("%d images are needed." % (x*y))
	exit()

for i in range(y):
	row = iio.imread(sys.argv[i * x + 3])
	for j in range(1, x):
		ai = i * x + j + 3
		im = iio.imread(sys.argv[ai])
		row = np.concatenate((row, im), axis=1)
	if i == 0:
		result = row
	else:
		result = np.concatenate((result, row), axis=0)

iio.imwrite(sys.argv[2], result)

print("Stitched image saved as", sys.argv[2])
