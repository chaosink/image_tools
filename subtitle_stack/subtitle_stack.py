#!/usr/bin/env python3

import imageio as iio
import sys
import os
import numpy as np

if len(sys.argv) < 4:
	print("subtitle_stack: Stack multiple images to show only subtitles.")
	print("Usage: subtitle_stack.py output_file subtitle_height {[movie_screenshots]... | movie_screenshots_dir}")
	exit()

height_subtitle = int(sys.argv[2])

files = []
if os.path.isdir(sys.argv[3]):
	files = os.listdir(sys.argv[3])
	to_be_removed = []
	for file in files:
		if file.startswith('merge'):
			to_be_removed.append(file)
	for file in to_be_removed:
		files.remove(file)
	files.sort()
	for i in range(len(files)):
		files[i] = os.path.join(sys.argv[3], files[i])
else:
	for i in range(3, len(sys.argv)):
		files.append(sys.argv[i])

result = iio.imread(files[0])
height_image = result.shape[0]

for i in range(1, len(files)):
	image = iio.imread(files[i])
	result = np.append(result, image[height_image - height_subtitle:,:], axis=0)
iio.imwrite(sys.argv[1], result)

print("Stacked image saved as", sys.argv[1])
