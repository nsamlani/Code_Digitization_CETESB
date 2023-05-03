# -*- coding: utf-8 -*-
"""
Created on Tue Jan 24 14:38:25 2023

@author: U0035488
"""

import os
from pdf2image import convert_from_path

output_path = r'E:/Nouha_forms/300 dpi images/Registry2007_300dpi/'
os.makedirs(output_path)

files = os.listdir(r"E:/Nouha_forms/pdf_files/Registry2007_split/")

for filename in files:
    page = convert_from_path(r"E:/Nouha_forms/pdf_files/Registry2007_split/" + filename,300,poppler_path=r"C:\Program Files\poppler-22.01.0\Library\bin")
    print(f"{filename} is converted")
    page[0].save(output_path + filename[:-4] + '.jpg', 'JPEG')