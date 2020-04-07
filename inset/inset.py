#!/usr/bin/env python3

import sys
import numpy as np
import imageio as iio

########## parameters

insets = [
	{
		'pos': [330, 260],
		'border_color': [1, 0, 0],
	},
	{
		'pos': [220, 130],
		'border_color': [0, 0, 1],
	},
]
size = [64, 64]
border_width = 1
scale = 4

##########

if len(sys.argv) != 3:
	print("inset: Outline and extract insets.")
	print("Usage: inset.py input_image outpu_image")
	exit()

input_image_name = sys.argv[1]
output_image_name = sys.argv[2]
p = output_image_name.rfind('.')
inset_name = output_image_name[:p] + '_inset'

image = iio.imread(input_image_name)

n_inset = len(insets)
for i in range(n_inset):
	x0 = insets[i]['pos'][0] - size[0] // 2
	y0 = insets[i]['pos'][1] - size[1] // 2
	border_color = np.array(insets[i]['border_color'])
	if image.dtype == np.uint8:
		border_color *= 255

	x1 = x0 + size[0]
	y1 = y0 + size[1]
	inset = image[y0:y1, x0:x1].copy()
	image[y0:y1, x0:x1] = border_color
	image[y0+border_width:y1-border_width, x0+border_width:x1-border_width] = inset[border_width:-border_width, border_width:-border_width]

	inset_output_shape = list(inset.shape)
	inset_output_shape[0] *= scale
	inset_output_shape[1] *= scale

	inset_output = np.full(inset_output_shape, border_color, dtype=image.dtype)
	for y in range(inset_output_shape[1]):
		for x in range(inset_output_shape[0]):
			xx = x // scale
			yy = y // scale
			inset_output[y][x] = image[y0 + yy][x0 + xx]

	inset_name_i = inset_name + "_" + str(i) + output_image_name[p:]
	iio.imwrite(inset_name_i, inset_output)

iio.imwrite(output_image_name, image)
