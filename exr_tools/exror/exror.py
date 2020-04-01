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

# Sum of Absolute Error
def SAE(img_refer, img_noisy):
	d = img_noisy - img_refer
	d = np.abs(d)
	sae = d.sum()
	return sae

# Sum of Squared Error
def SSE(img_refer, img_noisy):
	d = img_noisy - img_refer
	d *= d
	sse = d.sum()
	return sse

# Mean Absolute Error
def MAE(img_refer, img_noisy):
	sae = SAE(img_refer, img_noisy)
	mae = sae / img_noisy.size
	return mae

# Mean Squared Error
def MSE(img_refer, img_noisy):
	return mean_squared_error(img_refer, img_noisy)
	sse = SSE(img_refer, img_noisy)
	mse = sse / img_noisy.size
	return mse

# Root Mean Squared Error
def RootMSE(img_refer, img_noisy):
	mse = MSE(img_refer, img_noisy)
	root_mse = np.sqrt(mse)
	return root_mse

# Relative Mean Absolute Error
def RMAE(img_refer, img_noisy):
	d = img_noisy - img_refer
	d = np.abs(d)
	ref = img_refer + 0.01
	d = d / ref
	rmae = d.sum()
	rmae = rmae / img_noisy.size
	return rmae

# Relative Mean Squared Error
def RMSE(img_refer, img_noisy):
	d = img_noisy - img_refer
	d *= d
	ref = img_refer * img_refer + 0.01
	d = d / ref
	rmse = d.sum()
	rmse = rmse / img_noisy.size
	return rmse

def SSIM(img_refer, img_noisy):
	return structural_similarity(img_refer, img_noisy, multichannel=True, gaussian_weights=True)

def Tonemap(hdr, gamma=2.2):
	ldr = np.clip(hdr, 0, 1)
	ldr = np.power(hdr, gamma)
	ldr = np.round(hdr)
	return ldr

def PSNR(img_refer, img_noisy):
	img_refer_ldr = Tonemap(img_refer)
	img_noisy_ldr = Tonemap(img_noisy)
	return peak_signal_noise_ratio(img_refer_ldr, img_noisy_ldr, data_range=255)

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

	time = exrtime(img_noisy_name)
	print(img_noisy_name)
	if time:
		print("Time :", time)
	print("MAE ↓:", MAE(img_refer, img_noisy))
	print("MSE ↓:", MSE(img_refer, img_noisy))
	# print("RootMSE:", RootMSE(img_refer, img_noisy))
	print("RMAE↓:", RMAE(img_refer, img_noisy))
	print("RMSE↓:", RMSE(img_refer, img_noisy))
	print("SSIM↑:", SSIM(img_refer, img_noisy))
	print("PSNR↑:", PSNR(img_refer, img_noisy))
	print()
