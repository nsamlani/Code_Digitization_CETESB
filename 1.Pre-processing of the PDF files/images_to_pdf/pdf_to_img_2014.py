# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import os
from pdf2image import convert_from_path

output_path = r"E:/Nouha_forms/300 dpi images/Registry2014_300dpi/"
os.makedirs(output_path)

files = os.listdir(r"E:/Nouha_forms/pdf_files/Registry2014_split/")

for filename in files:
    page = convert_from_path(r"E:/Nouha_forms/pdf_files/Registry2014_split/" + filename,300,poppler_path=r"C:\Program Files\poppler-22.01.0\Library\bin")
    print(f"{filename} is converted")
    page[0].save(output_path + filename[:-4] + '.jpg', 'JPEG')