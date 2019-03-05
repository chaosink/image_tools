#!/usr/bin/env python3

import pyexr
import sys

# channel: 'R','G','B','A'
if len(sys.argv) != 4:
	print("extract_channel_pyexr: Extract a channel as 'Y' into a new EXR.")
	print("Usage: extract_channel_pyexr.py input_file channel output_file")
	exit()

r = pyexr.read(sys.argv[1], sys.argv[2])
pyexr.write(sys.argv[3], r, channel_names=['Y'])
