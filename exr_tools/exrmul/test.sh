#!/bin/sh

./exrmul.py mul.exr .
./exrmul.py mul.exr \
	512x512_1.00_1.00_1.00.exr \
	512x512_0.50_0.50_0.50.exr \
	512x512_1.00_0.00_0.00.exr
