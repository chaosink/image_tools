#!/usr/bin/env python3

import cv2
import sys

if len(sys.argv) < 3:
	print("color2gray: Convert RGB image to grayscale.")
	print("Usage: color2gray.py input_file output_file")
	exit()

if_name = sys.argv[1]
of_name = sys.argv[2]
i_img = cv2.imread(if_name)
o_img = cv2.cvtColor(i_img, cv2.COLOR_BGR2GRAY)
cv2.imwrite(of_name, o_img)
