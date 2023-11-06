# -*- coding: utf-8 -*-

"""
Author: Nouha Samlani

REQUIREMENTS:
* Python packages: numpy, OpenCV 4.5.4.60
* Files: folder with the pdf files 


"""

import numpy as np
import cv2

params = np.zeros([1, 2])  # init params
s_img = np.zeros((702, 496, 3), np.uint8)

window_name = 'img'
#posList = []

def main():
    global s_img
    img = cv2.imread(r"path_of_the_folder"')
    s_img = cv2.resize(img, (0, 0), fx=1, fy=1)
    s_img = cv2.cvtColor(s_img, cv2.COLOR_BGR2RGB)

#     cv2.startWindowThread()
    cv2.imshow(window_name, s_img)

    print ('Click corners to determine the field')
    cv2.setMouseCallback(window_name, on_mouse, None)

    while True:
        k = cv2.waitKey(0) & 0xFF

        if k == 27:
            break # destroy window
counter=0
counter2 = 0
myPoints = []
point1 = (0,0)
point2 = (0,0)

def on_mouse(event, x, y, flag, param):
    global s_img,counter,counter2,myPoints,point1,point2

    if event == cv2.EVENT_LBUTTONDOWN:
        cv2.circle(s_img, (x, y), 1, (255, 0, 0), -1)
        cv2.imshow(window_name, s_img)
        if counter==0:
            point1 =(x,y)
            print(point1)
            counter += 1
        elif counter ==1:
            point2 =(x,y)
            print(point2)
            starting_x = point1[0]
            starting_y = point1[1]
            ending_x = point2[0]
            ending_y = point2[1]
            cv2.rectangle(s_img, (starting_x, starting_y), (ending_x, ending_y), (0, 255, 0), 2)

            type_area = input('Enter Type:')
            name = input('Enter Name:')
            myPoints.append([point1,point2,type_area,name])
            print(myPoints)
            counter = 0 
            counter2 += 1



      
if __name__ == '__main__':
    main()
