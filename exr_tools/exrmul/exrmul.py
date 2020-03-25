#!/usr/bin/env python3

import os, sys
import glob
import pyexr

if len(sys.argv) < 3:
	print("exrmul: Multiply all EXRs specified or in a dir.")
	print("Usage: exrmul.py output_EXR {input_EXR_dir | input_EXRs...}")
	exit()

output_name = sys.argv[1]
path = sys.argv[2]
exr_files = []
if os.path.isdir(path):
	exr_files = glob.glob(os.path.join(path, "*.exr"))
else:
	for i in range(2, len(sys.argv)):
		exr_files.append(sys.argv[i])

output_exr = None
for file in exr_files:
	if output_exr is None:
		output_exr = pyexr.read(file)
	else:
		output_exr *= pyexr.read(file)

if output_exr.shape[2] == 1:
	pyexr.write(output_name, output_exr, channel_names=['Y'])
else:
	pyexr.write(output_name, output_exr)
