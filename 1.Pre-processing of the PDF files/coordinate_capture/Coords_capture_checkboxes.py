
import cv2
import numpy as np

img = cv2.imread('blanked_form.jpg')
s_img = cv2.resize(img, (0, 0), fx=0.5,fy=0.5)
s_img = cv2.cvtColor(s_img,cv2.COLOR_BGR2RGB)
s_img = cv2.cvtColor(s_img,cv2.COLOR_RGB2GRAY)

(thresh,img_bin) = cv2.threshold(s_img,255,255,cv2.THRESH_BINARY|cv2.THRESH_OTSU)

img_bin = 255-img_bin

cannyKernel_size = 100
img_canny = cv2.Canny(img_bin,cannyKernel_size,cannyKernel_size)

#cv2.imshow("img_canny",img_canny)
#cv2.waitKey()

contours,hierarchy = cv2.findContours(img_canny,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
print(contours)

#for i,h in enumerate(hierarchy):
#    if h[2]==-1:
#        index.append(i)
#print(index)


disp = cv2.merge((img_canny,img_canny,img_canny))
s_img = cv2.cvtColor(s_img, cv2.COLOR_GRAY2BGR)
#index_cnt = list(range(0,10))
disp = cv2.drawContours(s_img,contours,2,color=(0,255,255)) 
#cv2.imshow("img_canny",disp)
#cv2.waitKey()
#
#        
##cv2.drawContours(img_canny,contours_filtered,-1, (0, 255, 0), 3)
#cv2.imwrite("img_contour_edge_detection_blanked_w/o_checks.jpg",disp)


#def box_area(contours,expected_area=169,tolerance=55,squareness_tolerance=5):
#    contours_filtered = []
#    for contour in contours:
#        
#        area = cv2.contourArea(contour)
#        print(area)
#        x,y,w,h = cv2.boundingRect(contour)
#        
#        if (abs(area-expected_area)<= tolerance) and (abs(area-expected_area)<= squareness_tolerance):
#            contours_filtered.append(contour)
#    return contours_filtered

boxes =[]
for i,c in enumerate(contours):
    x, y, w, h = cv2.boundingRect(c)
    if w >= 8 and h >=8: 
        cv2.rectangle(s_img,(x,y),(x+w,y+h),(0,255,0),2)
        box_XY = (i,x, y,w,h)
        print(box_XY)
        boxes.append(box_XY)
    cv2.imshow(f"contour{i}",s_img)
    cv2.waitKey()  
  
print(len(boxes))    
    
