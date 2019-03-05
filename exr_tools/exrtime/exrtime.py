#!/usr/bin/env python3

import sys
import os
import re
import OpenEXR as exr

def exrtime(image):
	header = exr.InputFile(image).header()
	# for k,v in header.items():
	# 	print(k)
	# 	if isinstance(v, bytes):
	# 		print(v.decode())
	# 	else:
	# 		print(v)

	if 'log' in header:
		log = header['log'].decode()
		m = re.findall(r"(?<=Render time: ).*", log)
		if m:
			return m[-1]
		else:
			return None
	else:
		return None

if __name__ == '__main__':
	if len(sys.argv) < 2:
		print("exrtime: Get the timing log recording the time used for generating the EXR.")
		print("Usage: exrtime image.exr")
		exit(0)
	time = exrtime(sys.argv[1])
	if time:
		print(time)
		os.system("echo -n %s | xclip -selection clipboard" % time)
	else:
		print("No time information")
