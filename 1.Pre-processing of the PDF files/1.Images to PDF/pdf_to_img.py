
"""
Author: Nouha Samlani

REQUIREMENTS:
* Python packages: poppler-22.01.0, pdf2image
* Files: folder with the pdf files 


"""

import os
from pdf2image import convert_from_path

output_path = r'outputFolder/'
# os.makedirs(output_path)

files = os.listdir(r"path_of_the_folder")

for filename in files:
    page = convert_from_path(r"outputFolder/" + filename,300,poppler_path=r"C:\Program Files\poppler-22.01.0\Library\bin") # resolution of 300 dpi
    print(f"{filename} is converted")
    page[0].save(output_path + filename[:-4] + '.jpg', 'JPEG')
    
