#!/usr/bin/env python3

import pyexr
import sys
import numpy as np

if len(sys.argv) != 3:
	print("clamp: Turn zero-value pixels into red, nonzero-value pixels into green.")
	print("Usage: clamp.py input_file output_file")
	exit()

img = pyexr.read(sys.argv[1])
size = img.shape[0:2]

zero = np.zeros(size)

is_zero = np.all(img == 0, 2)
img_out = np.stack((is_zero, 1 - is_zero, zero), 2)

n_zero = is_zero.sum()
print(n_zero / (size[0] * size[1]))

pyexr.write(sys.argv[2], img_out)
