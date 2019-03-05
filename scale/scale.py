#!/usr/bin/env python3

import sys
import cv2 as cv

if len(sys.argv) < 5:
	print("scale: Scale images using cubic/linear interpolation.")
	print("Usage: scale.py input_file output_file scale_method(cubic/linear) scale_factor_x [scale_factor_y]")
	exit()

scale_x = float(sys.argv[4])
if len(sys.argv) > 5:
	scale_y = float(sys.argv[5])
else:
	scale_y = scale_x

image = cv.imread(sys.argv[1])
if sys.argv[3] == 'cubic':
	image = cv.resize(image, (0, 0), image, scale_x, scale_y, cv.INTER_CUBIC)
elif sys.argv[3] == 'linear':
	image = cv.resize(image, (0, 0), image, scale_x, scale_y, cv.INTER_LINEAR)
else:
	print("Invalid scale method:", sys.argv[3])
	exit()

cv.imwrite(sys.argv[2], image)
