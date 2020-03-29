#!/usr/bin/env python3

import sys, os
import numpy as np
import pyexr
from skimage.metrics import structural_similarity, mean_squared_error, peak_signal_noise_ratio

import importlib.util
script_dir = os.path.dirname(os.path.realpath(__file__))
spec = importlib.util.spec_from_file_location("*", os.path.join(script_dir, "../exrtime/exrtime.py"))
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)
exrtime = module.exrtime

def SSE(img_refer, img_noisy):
	d = img_noisy - img_refer
	d *= d
	sse = d.sum()
	return sse

def MSE(img_refer, img_noisy):
	sse = SSE(img_refer, img_noisy)
	mse = sse / img_noisy.size
	return mse

def RMSE(img_refer, img_noisy):
	d = img_noisy - img_refer
	d *= d
	ref = img_refer * img_refer + 0.01
	d = d / ref
	rmse = d.sum()
	rmse = rmse / img_noisy.size
	return rmse

# def CorrectGamma(Mat &img)
# 	Mat m
# 	pow(img, 1 / 2.2, m)
# 	m *= 255
# 	m.convertTo(m, CV_8U)
# 	return m

if len(sys.argv) < 3:
	print("exror: Evaluate image in MSE, rMSE and SSIM.")
	print("Usage: exror.py reference_image noisy_image [other_noisy_image]")
	exit(0)

img_refer_name = sys.argv[1]
img_refer = pyexr.read(img_refer_name).astype(np.float64)

print()
for i in range(2, len(sys.argv)):
	img_noisy_name = sys.argv[i]
	img_noisy = pyexr.read(img_noisy_name).astype(np.float64)

	if img_noisy.shape != img_refer.shape:
		print("Images have different sizes:")
		print("	%s:" % img_refer_name, img_refer.shape)
		print("	%s:" % img_noisy_name, img_noisy.shape)
		exit(1)

	ssim = structural_similarity(img_refer, img_noisy, multichannel=True, gaussian_weights=True)
	# psnr = peak_signal_noise_ratio(img_refer, img_noisy, 255)
	mse = mean_squared_error(img_refer, img_noisy)
	time = exrtime(img_noisy_name)
	print(img_noisy_name)
	if time:
		print("Time:", time)
	print("MSE :", mse)
	print("RMSE:", RMSE(img_refer, img_noisy))
	print("SSIM:", ssim)
	print()
