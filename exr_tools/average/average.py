#!/usr/bin/env python3

import pyexr
import sys
import numpy as np

if len(sys.argv) != 3:
	print("average: Average all channels into a single one.")
	print("Usage: average.py input_file output_file")
	exit()

rgb = pyexr.read(sys.argv[1])
y = np.average(rgb, 2)

pyexr.write(sys.argv[2], y, channel_names=['Y'])
