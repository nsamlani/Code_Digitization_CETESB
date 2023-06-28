"""
Author: Nouha Samlani

Requirements: pytesseract, regex, por.traindata included in the tesseract installed folder
Files: Folder of images of teh year 2008
"""

import cv2
import numpy as np
import pytesseract
import os
import re
import pandas as pd
from pytesseract import Output


import time
 
# record start time
start = time.time()

pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

folder = r"Registry2008_300dpi"
year = "2008"

forms_list = os.listdir(folder)
print(forms_list)

roi = [[(118, 309), (2311, 360), 'text', 'Company Name'],
       [(119, 371), (2311, 406), 'text', 'Address'], 
       [(404, 472), (579, 517), 'text', 'Fuse'], 
       [(706, 476), (962, 515), 'text', 'Datum'], 
       [(1086, 474), (1290, 518), 'text', 'UTM_E'], 
       [(1410, 476), (1709, 516), 'text', 'UTM_N'], 
       [(340, 520), (1851, 569), 'text', 'Classification']]

    
whitelist = "0123456789., "

img = cv2.imread(folder+'/'+forms_list[0])
img = cv2.cvtColor(img,cv2.COLOR_RGB2BGR)
img = cv2.resize(img,(0,0),fx=1,fy=1)
## Checking the textboxes on the image file
for i,r in enumerate(roi):
    cv2.rectangle(img,(r[0][0],r[0][1]),(r[1][0],r[1][1]),(0,255,0),2)
    
cv2.imwrite(f'Detected_Textboxes_{year}_300dpi.jpg',img)

myData = []
#
for j,y in enumerate(forms_list):
    form = []
    img = cv2.imread(folder+"/"+ y,0)
    img = cv2.resize(img, (0, 0), fx=1,fy=1)
#    cv2.imshow(y,s_img)
#    cv2.waitKey(0)


    print(f'######### Extracting Data from {folder} form number {j} ##########')
    regex = re.compile(r'\d+')
    form_nb = regex.findall(y)[1]
    form.insert(0,form_nb)
#         form.append(form_nb)
    for x,r in enumerate(roi):
        imgCrop = img[r[0][1]:r[1][1],r[0][0]:r[1][0]]

 
##     if text or box
        if r[3] in ['UTM_E','UTM_N']:
    #        cv2.imshow(r[3],imgCrop)
    #        cv2.waitKey(0)
            _,binary = cv2.threshold(imgCrop, 0,255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
            data = pytesseract.image_to_data(binary,lang='por',config = f'-c tessedit_char_whitelist={whitelist}',output_type = Output.DATAFRAME, pandas_config=None)
            text = pytesseract.image_to_string(binary,lang='por')
            data_seq_only  = data[data['word_num']!= 0]
            probs = data_seq_only['conf'].mean()
            print(f'{r[3]}:{text}:{probs}')
            form.append(text)
            form.append(probs)
            
#            form = [s.strip('\n') for s in form]

        else:
            data = pytesseract.image_to_data(imgCrop,lang='por',output_type = Output.DATAFRAME, pandas_config=None)
            text = pytesseract.image_to_string(imgCrop,lang='por')
            data_seq_only  = data[data['word_num']!= 0]
            probs = data_seq_only['conf'].mean()
            print(f'{r[3]}:{text}:{probs}')
            form.append(text)
            form.append(probs)
      
    myData.append(form)

print(myData)

# record end time
end = time.time()
# print the difference between start and end time in milli. secs
print("The time of execution of above program is :",(end-start) * 10**3, "ms") 


# Create the pandas DataFrame
data_text = pd.DataFrame(myData, columns = ['FormNb', 'Company Name','Company Name_prob','Address','Address_probs','UTMFuse','UTMFuse_probs',
                                            'Datum','Datum_probs','UTM_E','UTM_E_probs','UTM_N','UTM_N_probs','Classification','Classification_probs'])
data_text.to_excel(f'por_Data_text_{year}_300dpi_nbs_text_FINAL.xlsx')

