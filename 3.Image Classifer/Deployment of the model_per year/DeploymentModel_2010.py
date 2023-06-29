"""" 
Author: Nouha Samlani

Model Deployment code for the year 2010

Requirements: 
* Tensorflow, opencv, regex
* Model .h5 file
* Folder of the form images of the year
Copy and past roi of the correspondent year from bounding_boxes_checkboxes.txt text file
""""

import cv2
import numpy as np
import pytesseract
import os
import re
import pandas as pd

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.optimizers import RMSprop
from tensorflow.keras.preprocessing import image
import matplotlib.pylab as plt
import tensorflow as tf

# check if it is the right folder
folder = r"Registry2010/"
year = '2010'
forms_list = os.listdir(folder)

# print(forms_list)

#  Load the model
from tensorflow.keras.models import load_model
model = load_model('checkboxes_classifier.h5')
## Copy and paste the roi from bounding_boxes_checkboxes.txt text file
roi = [[]]
data_boxes = []
pixels_check= []
value = 0

img = cv2.imread(folder+'/'+forms_list[0])
img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
img = cv2.resize(img,(0,0),fx=1,fy=1)
#forms_list = ['CETESB_registry_2019-1.jpg', 'CETESB_registry_2019-10.jpg',
#              'CETESB_registry_2019-100.jpg', 'CETESB_registry_2019-1000.jpg', 'CETESB_registry_2019-1001.jpg']
for i,r in enumerate(roi):
    x=r[0][0]
    y=r[0][1]
    cv2.rectangle(img,(r[0][0],r[0][1]),(r[1][0],r[1][1]),(0,255,0),2)
    cv2.putText(img=img, text=r[3],org =(x-2,y-2), fontFace=cv2.FONT_HERSHEY_TRIPLEX, fontScale=0.25, color=(0, 0, 0),thickness=1)
    
cv2.imwrite(f'Detected_Textboxes_{year}_updated.jpg',img)
for j,y in enumerate(forms_list):
    data = []
    pixels = []
    img = cv2.imread(folder+"/"+ y)
    s_img = cv2.resize(img, (0, 0), fx=1,fy=1)
#     cv2.imwrite()
#     cv2.imshow(y,s_img)
#     cv2.waitKey(0)


    print(f'######### Extracting Data from {j} ##########')
    regex = re.compile(r'\d+')
    form_nb = regex.findall(y)[1]
    data.append(year)
    data.append(form_nb)
#     pixels.append(form_nb)
    for x,r in enumerate(roi):
        
        imgCrop = s_img[r[0][1]:r[1][1],r[0][0]:r[1][0]]
#         gray = cv2.cvtColor(imgCrop,cv2.COLOR_BGR2GRAY)

#         n_white_pix = np.sum(gray == 255)

#         pixels.append(n_white_pix)
        imgCrop_resized = cv2.resize(imgCrop, (112,112))
        
        X = image.img_to_array(imgCrop_resized)
        X = np.expand_dims(X,axis=0)
        images = np.vstack([X])
        val = model.predict(images)
        if val == 0:
            ### box is checked ###
            value = 1
            data.append(value)
        else: 
            ### box is not checked ###
            value = 0
            data.append(value)  
#     print(data)


#     pixels_check.append(pixels)
    data_boxes.append(data)

list_columns = [r[3] for r in (roi)]
list_columns.insert(0,'FormNb')
list_columns.insert(0,'Year')

# pixel_boxes = pd.DataFrame(pixels_check, columns=list_columns)
data_boxes = pd.DataFrame(data_boxes, columns=list_columns)

# pixel_boxes.to_excel(f'../Final_Boxes/{year}.xlsx')
data_boxes.to_excel(f'{year}_model_classifier.xlsx')
