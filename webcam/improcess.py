import cv2
import numpy as np
from matplotlib import pyplot as plt

global cv_low_version
cv_low_version=True
if (int( cv2.__version__.split('.')[0]) > 3):
    cv_low_version=False

def closing_circle(image,radius=3):
    kernel = np.ones((radius,radius),np.uint8)
    closing_img= cv2.morphologyEx(image,cv2.MORPH_CLOSE,kernel)
    return closing_img
def select_region(image,min_size=1):
    ret,labels,stats,centroids =cv2.connectedComponentsWithStats(image)                       
    num_labels=labels.max()                      
    for i in range(1,num_labels+1):
        if(stats[i, cv2.CC_STAT_AREA]>min_size):
            x=stats[i, cv2.CC_STAT_LEFT ]
            y=stats[i, cv2.CC_STAT_TOP ]
            x1=stats[i, cv2.CC_STAT_WIDTH ]+x
            y1=stats[i, cv2.CC_STAT_HEIGHT ]+y
            cv2.rectangle(image,(int(x),int(y)),(int((x1)),int((y1))),(200,0,0),2)
    return image

def detect_and_get_area_template(image):
    if (image is None):
        return None,0,0
    kernel = np.ones((20,1),np.uint8)
    erosion = cv2.erode(image,kernel,iterations = 2)
    kernel = np.ones((20,1),np.uint8)
    expand = cv2.dilate(erosion,kernel,iterations = 2)
    retval,im_thresh= cv2.threshold(expand,150,255,cv2.THRESH_BINARY)
    max_width=0   
    max_contour_area=0
    if (cv_low_version):
        _,contours,hier=cv2.findContours(im_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    else:
        contours,hier=cv2.findContours(im_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for cnt in contours:
        rect = cv2.minAreaRect(cnt)
        (x, y), (w, h), angle = rect
        area=cv2.contourArea(cnt)
        if (area> max_contour_area):
            max_contour_area=area
            max_width= w
            rect_max= rect

    ret,labels,stats,centroids =cv2.connectedComponentsWithStats(im_thresh)    
    #find biggest object  
    max_index=-1
    max_size=0 
             
    num_labels=labels.max()                      
    for i in range(1,num_labels+1):
        if(stats[i, cv2.CC_STAT_AREA]>30):
            if (stats[i, cv2.CC_STAT_AREA]>max_size):
                max_size = stats[i, cv2.CC_STAT_AREA]
                max_index = i
    imcrop = image[stats[max_index, cv2.CC_STAT_TOP]-20:stats[max_index, cv2.CC_STAT_TOP]+stats[max_index, cv2.CC_STAT_HEIGHT]+20,stats[max_index, cv2.CC_STAT_LEFT]-20:stats[max_index, cv2.CC_STAT_LEFT]+stats[max_index, cv2.CC_STAT_WIDTH]+20]
    return imcrop,max_size,max_width


# template_image = cv2.imread('D:\\template2.jpg',0)
# template,template_size,template_width = detect_and_get_area_template(template_image)
# template_w, template_h = template.shape[::-1]

# All the 6 methods for comparison in a list
# method = cv2.TM_SQDIFF_NORMED
# import os

# path = 'D:\\opencv\\'

# files = []
# # r=root, d=directories, f = files
# for r, d, f in os.walk(path):
#     for file in f:
#         if '.jpg' in file:
#             files.append(os.path.join(r, file))
def display_text_with_box(image,text,pos,margin=5,text_color=(0,0,0),box_color=(255,255,255)):
    size,base_line= cv2.getTextSize(text,cv2.FONT_HERSHEY_COMPLEX,0.5,1)
    cv2.rectangle(image,pos,(pos[0]+2*margin+size[0],pos[1]+2*margin+size[1]+base_line),box_color,-1)
    cv2.putText(image,text,(pos[0]+margin,pos[1]+margin+size[1]),cv2.FONT_HERSHEY_COMPLEX,0.5,text_color,1)
global total
total=0
global pass_count
pass_count=0
global fail
fail=0
def inspection(img_color,template,template_width,vertical_diff=1400,horizontal_diff=20):
    global total
    global pass_count
    global fail
    result=True
    template_w, template_h = template.shape[::-1]
    img = cv2.cvtColor(img_color,cv2.COLOR_BGR2GRAY)
    img_color_display = img_color.copy()
    imgw,imgh= img.shape[::-1]
    if (template_w>imgw*0.8 or template_h >imgh*0.8):
        display_text_with_box(img_color_display,'template too big',(10,10),text_color=(255,255,255),box_color=(0,0,255))
        return img_color_display,False
    res = cv2.matchTemplate(img,template,cv2.TM_SQDIFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    top_left = min_loc
    bottom_right = (top_left[0] + template_w, top_left[1] + template_h)
    imcrop = img[int(max( top_left[1]-20,0)):int(bottom_right[1]+20),int(max(top_left[0]-20,0)):int(bottom_right[0]+20)]
    kernel = np.ones((20,1),np.uint8)
    erosion = cv2.erode(imcrop,kernel,iterations = 2)
    kernel = np.ones((20,1),np.uint8)
    expand = cv2.dilate(erosion,kernel,iterations = 2)
    retval,im_thresh= cv2.threshold(expand,140,255,cv2.THRESH_BINARY)
    ret,labels,stats,centroids =cv2.connectedComponentsWithStats(im_thresh)
    max_size=0                 
    num_labels=labels.max()                      
    for i in range(1,num_labels+1):
        if(stats[i, cv2.CC_STAT_AREA]>30):
            if (stats[i, cv2.CC_STAT_AREA]>max_size):
                max_size = stats[i, cv2.CC_STAT_AREA]
    #find max contour
    max_contour_area=0
    rect_max=[(0,0),(0,0),0]
    if (cv_low_version):
        _,contours,hier=cv2.findContours(im_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    else:
        contours,hier=cv2.findContours(im_thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    statcontours=[]
    for cnt in contours:
        rect = cv2.minAreaRect(cnt)
        (x, y), (w, h), angle = rect
        area=cv2.contourArea(cnt)
        if (area> max_contour_area):
            max_contour_area=area
            rect_max= rect

    
    if (max_size>0):       
        (x, y), (w, h), angle = rect_max        
        area_diff = abs( w*h-max_size)
        percent_diff = (area_diff/(w*h))*100
        width_diff = abs(template_width - w)
        width_diff_percent = (width_diff/template_width)*100
        rec_draw = (x+top_left[0]-20, y+top_left[1]-20), (w, h), angle
        box = cv2.boxPoints(rec_draw)
        box = np.int0(box)
        miss_align_vertical=False
        miss_align_horizontal=False

        if (percent_diff>vertical_diff):
            miss_align_vertical=True
            cv2.putText(img_color_display,'miss aligned vetical: '+str(percent_diff),(int(x+top_left[0]-20),int(y+top_left[1]-20)),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,255),1)       
            #cv2.rectangle(img_color,top_left_new, bottom_right_new, (0,0,255), 2)
        if (width_diff_percent>horizontal_diff):
            cv2.putText(img_color_display,'miss aligned horizontal: '+str(width_diff_percent) ,(int(x+top_left[0]-20),int(y+20+top_left[1]-20)),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,255),1)
            miss_align_horizontal=True       
            #cv2.rectangle(img_color,top_left_new, bottom_right_new, (0,0,255), 2)
        if (miss_align_vertical or miss_align_horizontal):
            result=False
            cv2.drawContours(img_color_display,[box],0,(0,0,255),2)
        else:
            cv2.putText(img_color_display,'Label OK',top_left,cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,255),1)
            cv2.drawContours(img_color_display,[box],0,(255,0,0),2)
        display_text_with_box(img_color_display,'Vertical difference: ' + str(round( percent_diff,1)) + ' %',(10,140))
        display_text_with_box(img_color_display,'Horizontal difference: ' + str(round( width_diff_percent,1)) + ' %',(10,180))
    else: 
        
        result=False
  

    total=total+1
    if (result):
        pass_count=pass_count+1
    else:
        fail=fail+1


    size,base_line= cv2.getTextSize('total: '+ str(total),cv2.FONT_HERSHEY_COMPLEX,0.5,1)
    size1,base_line= cv2.getTextSize(str(pass_count),cv2.FONT_HERSHEY_COMPLEX,0.5,1)
    size2,base_line= cv2.getTextSize(str(fail),cv2.FONT_HERSHEY_COMPLEX,0.5,1)
    box_width=size[0]+20
    cv2.rectangle(img_color_display,(10,10),(box_width+10,130),(255,255,255),-1)
    cv2.putText(img_color_display,'total: '+str(total),(20,40),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,0),1)
    cv2.putText(img_color_display,'pass: ',(20,80),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,0),1)
    cv2.putText(img_color_display,str(pass_count),(box_width- size1[0],80),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,0),1)
    cv2.putText(img_color_display,'fail: ',(20,120),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,0),1)
    cv2.putText(img_color_display,str(fail),(box_width- size2[0],120),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,0),1)

    return img_color_display,result
def main_removed():
    for f in files:
        img_color = cv2.imread(f)
        imcrop = inspection()

            #box = cv2.boxPoints(rect)
            #box = np.int0(box)
            #cv2.drawContours(img_color,[box],0,(0,0,255),2)    
        #find biggest object  
        cv2.imshow('template image',template)
        cv2.imshow('detected maker',imcrop)
        cv2.imshow('source image',img_color)
        cv2.waitKey()
    # continue
    # max_index=-1
    # max_size=0                 
    # num_labels=labels.max()                      
    # for i in range(1,num_labels+1):
    #     if(stats[i, cv2.CC_STAT_AREA]>30):
    #         if (stats[i, cv2.CC_STAT_AREA]>max_size):
    #             max_size = stats[i, cv2.CC_STAT_AREA]
    #             max_index = i
    # min_vertical_miss_aligned_area =1500
    # min_horizontal_diff=20
    
    # if (max_index!=-1):       
    #     w=stats[max_index, cv2.CC_STAT_WIDTH ]
    #     h=stats[max_index, cv2.CC_STAT_HEIGHT ]
    #     area_diff = abs( w*h-max_size)
    #     width_diff = abs(template_width - w)
    #     top_left_new=(stats[max_index, cv2.CC_STAT_LEFT ]+top_left[0]-40,stats[max_index, cv2.CC_STAT_TOP ]+top_left[1]-40)
    #     bottom_right_new=(top_left_new[0]+stats[max_index, cv2.CC_STAT_WIDTH ],top_left_new[1]+stats[max_index, cv2.CC_STAT_HEIGHT ])
    #     miss_align_vertical=False
    #     miss_align_horizontal=False
        
    #     if (area_diff>min_vertical_miss_aligned_area):
    #         miss_align_vertical=True
    #         cv2.putText(img_color,'miss aligned vetical',top_left,cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,255),1)       
    #         #cv2.rectangle(img_color,top_left_new, bottom_right_new, (0,0,255), 2)
    #     if (width_diff>min_horizontal_diff):
    #         cv2.putText(img_color,'miss aligned horizontal',(top_left[0],top_left[1]-20),cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,255),1)
    #         miss_align_horizontal=True       
    #         #cv2.rectangle(img_color,top_left_new, bottom_right_new, (0,0,255), 2)
    #     if (miss_align_vertical or miss_align_horizontal):
    #         cv2.rectangle(img_color,top_left_new, bottom_right_new, (0,0,255), 2)
    #     else:
    #         cv2.putText(img_color,'Label OK',top_left,cv2.FONT_HERSHEY_COMPLEX,0.5,(0,0,255),1)
    #         cv2.rectangle(img_color,top_left_new, bottom_right_new, (255,0,0), 2)

        
            
    # cv2.imshow('aaa',template)
    # cv2.imshow('aaa1',img_color)
    # cv2.waitKey()
