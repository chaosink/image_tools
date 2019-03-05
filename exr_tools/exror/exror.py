#!/usr/bin/env python3

import sys
import numpy as np
import pyexr
from skimage.measure import compare_ssim, compare_mse, compare_psnr

import importlib.util
spec = importlib.util.spec_from_file_location("*", "/media/lin/MintSpace/program/CV_IP/image_tools/exr_tools/exrtime/exrtime.py")
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

ssim = compare_ssim(img1, img0, multichannel=True, gaussian_weights=True)
# psnr = compare_psnr(img1, img0, 255)
mse = compare_mse(img1, img0)
time = exrtime(sys.argv[1])
if time:
	print("Time:", time)
print("MSE :", mse)
print("RMSE:", RMSE(img0, img1))
print("SSIM:", ssim)
