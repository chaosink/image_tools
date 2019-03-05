#!/usr/bin/env python3

import os
from exrtime import exrtime

print('main:')
os.system('./exrtime.py test_time.exr')
os.system('./exrtime.py test_no-time.exr')

print('-----')

print('module:')
print(exrtime('test_time.exr'))
print(exrtime('test_no-time.exr'))
