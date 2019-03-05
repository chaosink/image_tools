#!/usr/bin/env python3

import pyexr
import sys
import numpy as np

if len(sys.argv) != 4:
	print("pure_color: Generate pure color EXRs(1 and 3 channels) with specific value and size.")
	print("Usage: pure_color.py width height value")
	exit()

width = int(sys.argv[1])
height = int(sys.argv[2])
value = float(sys.argv[3])

rgb = np.ones((height, width, 3)) * value
y = np.ones((height, width, 1)) * value

pyexr.write('%d_%d_%.2f_3.exr' % (width, height, value), rgb)
pyexr.write('%d_%d_%.2f_1.exr' % (width, height, value), y, channel_names=['Y'])
