#!/usr/bin/env python3

import sys
import array
import OpenEXR
import Imath

# channel: 'R','G','B','A'
if len(sys.argv) != 4:
	print("extract_channel: Extract a channel as 'Y' into a new EXR.")
	print("Usage: extract_channel.py input_file channel output_file")
	exit()

# Open the input file
file = OpenEXR.InputFile(sys.argv[1])
channel = sys.argv[2]

# Compute the size
dw = file.header()['dataWindow']
sz = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)

# Read the three color channels as 32-bit floats
FLOAT = Imath.PixelType(Imath.PixelType.FLOAT)
Y = array.array('f', file.channel(channel, FLOAT)).tolist()

# Convert to strings
Y = array.array('f', Y).tostring()

# Set header
header = OpenEXR.Header(sz[0], sz[1])
header['compression'] = Imath.Compression(Imath.Compression.PIZ_COMPRESSION)
header['channels'] = {'Y' : Imath.Channel(Imath.PixelType(OpenEXR.FLOAT))}

# Write the three color channels to the output file
out = OpenEXR.OutputFile(sys.argv[3], header)
out.writePixels({'Y' : Y})
