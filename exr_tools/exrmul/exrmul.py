#!/usr/bin/env python3

import sys
import os
import OpenEXR as exr
import Imath
import numpy as np

if len(sys.argv) < 4:
	print("exrmul: Multiply EXR image by a factor.")
	print("Usage: exrmul.py factor input.exr output.exr")
	exit(0)

print("This program can't retain all the logs into the output EXR. Don't use it.")
exit(0)

factor = float(sys.argv[1])

image = exr.InputFile(sys.argv[2])
header = image.header()
log = header['log'].decode()

FLOAT = Imath.PixelType(Imath.PixelType.FLOAT)
R = (np.frombuffer(image.channel('R', FLOAT), dtype=np.float32) * 2).tostring()
G = (np.frombuffer(image.channel('G', FLOAT), dtype=np.float32) * 2).tostring()
B = (np.frombuffer(image.channel('B', FLOAT), dtype=np.float32) * 2).tostring()

out = exr.OutputFile(sys.argv[3], header)
out.writePixels({'R': R, 'G': G, 'B': B})
