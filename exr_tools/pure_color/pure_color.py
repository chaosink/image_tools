#!/usr/bin/env python3

import pyexr
import sys
import numpy as np

if len(sys.argv) != 4 and len(sys.argv) != 6 and len(sys.argv) != 7:
	print("pure_color: Generate pure color EXRs(1/3/4 channels) with specific value and size.")
	print("Usage: pure_color.py width height channel_1 [channel_2 channel_3 [channel_4]]")
	exit()

width = int(sys.argv[1])
height = int(sys.argv[2])
n_channel = len(sys.argv) - 3
value = np.zeros(n_channel)
exr_name = "%dx%d" % (width, height)
for i in range(n_channel):
	value[i] = float(sys.argv[i + 3])
	exr_name += "_%.2f" % value[i]

img = np.ones((height, width, n_channel)) * value

exr_name += ".exr"
if n_channel == 1:
	pyexr.write(exr_name, img, channel_names=['Y'])
else:
	pyexr.write(exr_name, img)
