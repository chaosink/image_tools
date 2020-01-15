#!/usr/bin/env python3

import sys, os
import imageio as iio

if len(sys.argv) < 3:
	print("crop_wechat_window: crop the window of the chat records in WeChat.")
	print("Usage: crop_wechat_window.py input_file output_file")
	exit()

image_name = sys.argv[1]
image_out_name = sys.argv[2]
image = iio.imread(image_name)
script_path = os.path.realpath(__file__)
script_dir = os.path.dirname(script_path)
pattern = iio.imread(os.path.join(script_dir, "pattern.png"))

found_pattern = False
pattern_x = 0
pattern_y = 0
for x in range(image.shape[0] - pattern.shape[0] + 1):
	if not found_pattern:
		for y in range(image.shape[1] - pattern.shape[1] + 1):
			if (image[x:x+pattern.shape[0],y:y+pattern.shape[1]] == pattern).all():
				found_pattern = True
				pattern_x = x
				pattern_y = y
				break

if not found_pattern:
	print("Invalid screenshot!")
	exit()

bg_color = pattern[0, 0]

crop_x_0 = pattern_x
crop_y_0 = pattern_y
while crop_x_0 >= 1 and (image[crop_x_0 - 1][crop_y_0] == bg_color).all():
	crop_x_0 -= 1
while crop_y_0 >= 1 and (image[crop_x_0 + 1][crop_y_0 - 1] == bg_color).all():
	crop_y_0 -= 1

crop_x_1 = crop_x_0 + 1
crop_y_1 = crop_y_0 + 1
while crop_x_1 < image.shape[0] - 1 and (image[crop_x_1 + 1][crop_y_0 + 1] == bg_color).all():
	crop_x_1 += 1
crop_x_1 += 1
while crop_x_1 < image.shape[0] - 1 and (image[crop_x_1 + 1][crop_y_0 + 1] == bg_color).all():
	crop_x_1 += 1
while crop_y_1 < image.shape[1] - 1 and (image[crop_x_0 + 1][crop_y_1 + 1] == bg_color).all():
	crop_y_1 += 1

image[crop_x_0, crop_y_0] = image[crop_x_0, crop_y_1] = image[crop_x_1, crop_y_0] = image[crop_x_1, crop_y_1] = bg_color
image_crop = image[crop_x_0:crop_x_1+1, crop_y_0:crop_y_1+1]
iio.imwrite(image_out_name, image_crop)

print("Cropped image saved as", image_out_name)
