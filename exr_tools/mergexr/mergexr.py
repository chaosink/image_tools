#!/usr/bin/env python3

import os, sys
import pyexr

if len(sys.argv) != 3:
	print("mergexr: Merge multiple EXRs into a single one with multiple channels.")
	print("Usage: mergexr.py input_dir output_file")
	exit()

dir = sys.argv[1]
output = sys.argv[2]

data = {}

for dirpath, dirnames, filenames in os.walk(dir):
	for file in filenames:
		buffer_name, ext = os.path.splitext(file)
		if ext == '.exr':
			fullpath = os.path.join(dirpath, file)
			data[buffer_name] = pyexr.read(fullpath)

pyexr.write(output, data)
