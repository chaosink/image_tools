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

def SSE(img0, img1):
	d = img0 - img1
	d *= d
	sse = d.sum()
	return sse

def MSE(img0, img1):
	sse = SSE(img0, img1)
	mse = sse / img0.size
	return mse

def RMSE(img0, img1):
	d = img0 - img1
	d *= d
	ref = img1 * img1 + 0.01
	d = d / ref
	rmse = d.sum()
	rmse = rmse / img0.size
	return rmse

# def CorrectGamma(Mat &img)
# 	Mat m
# 	pow(img, 1 / 2.2, m)
# 	m *= 255
# 	m.convertTo(m, CV_8U)
# 	return m

if len(sys.argv) < 3:
	print("exror: Evaluate image in MSE, rMSE and SSIM.")
	print("Usage: exror.py noisy_image reference_image")
	exit(0)

img0 = pyexr.read(sys.argv[1]).astype(np.float64)
img1 = pyexr.read(sys.argv[2]).astype(np.float64)

if img0.shape != img1.shape:
	print("Images have different sizes:")
	print("	image0:", img0.shape)
	print("	image1:", img1.shape)
	exit(1)

ssim = structural_similarity(img1, img0, multichannel=True, gaussian_weights=True)
# psnr = peak_signal_noise_ratio(img1, img0, 255)
mse = mean_squared_error(img1, img0)
time = exrtime(sys.argv[1])
if time:
	print("Time:", time)
print("MSE :", mse)
print("RMSE:", RMSE(img0, img1))
print("SSIM:", ssim)
