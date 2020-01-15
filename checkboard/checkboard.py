#!/usr/bin/env python3

import imageio
import sys
import numpy as np

if len(sys.argv) < 3:
	print("checkboard: Generate checkboard images.")
	print("Usage: checkboard.py board_size block_size")
	exit()

board_size = int(sys.argv[1])
block_size = int(sys.argv[2])
block_num = board_size // block_size
image = np.zeros([board_size, board_size], dtype=np.ubyte)
for x in range(block_num):
	for y in range(block_num):
		if (x + y) % 2:
			for xb in range(block_size):
				for yb in range(block_size):
					xx = x * block_size + xb
					yy = y * block_size + yb
					if xx < board_size and yy < board_size:
						image[xx][yy] = 255

image_name = "checkboard_%s_%s.png" % (sys.argv[1], sys.argv[2])
imageio.imwrite(image_name, image)

print("Checkboard image saved as", image_name)
