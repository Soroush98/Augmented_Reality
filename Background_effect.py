import cv2
import numpy as np
import time
from math import sqrt
import  random
from math import ceil,floor

# get captures
cap = cv2.VideoCapture(0)
background_capture = cv2.VideoCapture('test.mp4')
fgbg = cv2.createBackgroundSubtractorMOG2()
seconds = 10
paint_h = 50
def gen_random(radius,number,width):
        total = width ;
        rand = []
        tempx = []
        tempy =[]
        for ll in range(number):
            paint_x = 0
            r = (random.random()*total)
            rand.append(r)
            total = total - (2*radius)
            for xx in range(floor(r)):
                l=0
                for zz in range(len(rand)):
                    if (rand[zz] - radius < xx and xx < rand[zz] + radius):
                        l = 1
                        break;
                if (l==0):
                    paint_x = paint_x +1

            t=0
            l=0
            s=0
            while (s<paint_x):
                l=0

                for zz in range(len(rand)):
                    if (rand[zz] - radius < t and t < rand[zz] + radius):
                        l = 1
                        break;
                if (l==0):
                    s=s+1
                t = t +1

            tempx.append(t)
            tempy.append(paint_h)
        return tempx,tempy

def webcam_record(effect):
    counter =0
    ignore = 0
    x = []
    y = []
    radius = 0
    rainpic = cv2.imread("rain.png",-1)
    h , w ,c= rainpic.shape
    if effect == 1:
        radius = 5
        rate = 2
    else:
        radius = ceil(w/2)
        rate = 4

    while cap.isOpened():
        ret,frame = cap.read()
        fgmask = fgbg.apply(frame)
        hight,width= fgmask.shape
        if (counter%10 ==0):
            counter=0
            xt,yt = gen_random(radius,10,width)
            x.extend(xt)
            y.extend(yt)
        if (ret == True):
            t=len(x)
            f=0
            while (f<t):
                if (y[f]>480-3*radius  or x[f] > width-20 or x[f] <= 10):
                    del(x[f])
                    del(y[f])
                    t=t-1;
                f = f+1
            for i in range (len(x)):
                if effect ==1 :
                    cv2.circle(frame,(x[i],y[i]),radius,(255,255,255),cv2.FILLED)
                else :
                    # for xt1 in range( x[i] - 7 ,x[i] +8 ,1):
                    #     for yt1 in range( y[i] - 7 ,y[i] +8 ,1):
                    #         frame[yt1,xt1 ] = rainpic[yt1-(y[i]-7),xt1 -(x[i]-7)]
                    tx = x[i]
                    ty = y[i]
                    bg_img = frame.copy()
                    b,g,r,a = cv2.split(rainpic)
                    overlay_color = cv2.merge((b,g,r))
                    mask = cv2.medianBlur(a,5)
                    h, w, _ = overlay_color.shape
                    roi = bg_img[ty:ty+h, tx:tx+w]
                    img1_bg = cv2.bitwise_and(roi.copy(),roi.copy(),mask = cv2.bitwise_not(mask))
                    img2_fg = cv2.bitwise_and(overlay_color,overlay_color,mask = mask)
                    frame[ty:ty+h, tx:tx+w] = cv2.add(img1_bg, img2_fg)

            cv2.imshow('Frame', frame)
            k = cv2.waitKey(25) & 0xff
            if k == 27:
                break;
            for i in range(len(x)):

                if (effect != 1):
                    x[i] = x[i] +7
                    y[i] = y[i] +7
                if (ignore > 10):

                    right = 0
                    left = 0
                    down=0
                    eps= 1
                    z=0

                    for x1 in range(x[i]-radius ,x[i] + radius,rate):
                        for y1 in range(-1*ceil(sqrt(radius*radius-(x1-x[i])*(x1-x[i])))+y[i],
                                        ceil(sqrt(radius*radius-(x1-x[i])*(x1-x[i]))+y[i]),rate):

                                if (fgmask[y1][x1] !=0):
                                    z =1
                                    if (y1<y[i]+radius and y1>y[i]):
                                        down = down +1
                                    if (x1<=x[i] +radius and x1 >=x[i]):
                                        right = right +1
                                    else:
                                        left = left +1
                    if z==1:
                        if (not((right - left <= eps  and right - left>=0)or (left-right <=eps and left-right>=0))):
                            if (right>left ):
                                x[i] = x[i] -1
                            else :
                                x[i] = x[i] +1
                    if down ==0 :
                        y[i] = y[i] +2
                if (effect != 1):
                    x[i] = x[i] -7
                    y[i] = y[i] -7
            counter=counter+1
            ignore = ignore+ 1
    cap.release()
    cv2.destroyAllWindows()
def video_output(effect):
    counter =0
    ignore = 0
    frame_width = int(background_capture.get(3))
    frame_height = int(background_capture.get(4))
    x = []
    y = []
    radius = 0
    rainpic = cv2.imread("rain.png",-1)
    h , w ,c= rainpic.shape
    if effect == 1:
        radius = 5
        rate = 2
    else:
        radius = ceil(w/2)
        rate = 4

    out = cv2.VideoWriter('output.avi',cv2.VideoWriter_fourcc('M','J','P','G'), 25, (frame_width,frame_height))
    while background_capture.isOpened():
        ret,frame = background_capture.read()
        fgmask = fgbg.apply(frame)
        hight,width= fgmask.shape
        if (counter%10 ==0):
            counter=0
            xt,yt = gen_random(radius,10,width)
            x.extend(xt)
            y.extend(yt)
        if (ret == True):
            t=len(x)
            f=0
            while (f<t):
                if (y[f]>hight-3*radius  or x[f] > width-20 or x[f] <= 10):
                    del(x[f])
                    del(y[f])
                    t=t-1;
                f = f+1
            for i in range (len(x)):
                if (effect == 1):
                    cv2.circle(frame,(x[i],y[i]),radius,(255,255,255),cv2.FILLED)
                else:
                    tx = x[i]
                    ty = y[i]
                    bg_img = frame.copy()
                    b,g,r,a = cv2.split(rainpic)
                    overlay_color = cv2.merge((b,g,r))
                    mask = cv2.medianBlur(a,5)
                    h, w, _ = overlay_color.shape
                    roi = bg_img[ty:ty+h, tx:tx+w]
                    img1_bg = cv2.bitwise_and(roi.copy(),roi.copy(),mask = cv2.bitwise_not(mask))
                    img2_fg = cv2.bitwise_and(overlay_color,overlay_color,mask = mask)
                    frame[ty:ty+h, tx:tx+w] = cv2.add(img1_bg, img2_fg)

            cv2.imshow('Frame', frame)
            out.write(frame)
            k = cv2.waitKey(25) & 0xff
            if k == 27:
                break;
            for i in range(len(x)):

                if (effect != 1):
                    x[i] = x[i] +7
                    y[i] = y[i] +7
                if (ignore > 10):

                    right = 0
                    left = 0
                    down=0
                    eps= 1
                    z=0

                    for x1 in range(x[i]-radius ,x[i] + radius,rate):
                        for y1 in range(-1*ceil(sqrt(radius*radius-(x1-x[i])*(x1-x[i])))+y[i],ceil(sqrt(radius*radius-(x1-x[i])*(x1-x[i]))+y[i]),rate):

                            if (fgmask[y1][x1] !=0):
                                z =1
                                if (y1<y[i]+radius and y1>y[i]):
                                    down = down +1
                                if (x1<=x[i] +radius and x1 >=x[i]):
                                    right = right +1
                                else:
                                    left = left +1
                    if z==1:
                        if (not((right - left <= eps  and right - left>=0)or (left-right <=eps and left-right>=0))):
                            if (right>left ):
                                x[i] = x[i] -1
                            else :
                                x[i] = x[i] +1
                    if down ==0 :
                        y[i] = y[i] +2
                if (effect != 1):
                    x[i] = x[i] -7
                    y[i] = y[i] -7
            counter=counter+1
            ignore = ignore+ 1
    cap.release()
    cv2.destroyAllWindows()
print('1: Webcam recording \n2: Save test.mp4  to output.avi\n')
select = int(input())
print('1:snow effect \n2: rain effect\n')
select2 = int(input())
if (select == 1):
    webcam_record(select2)
if (select == 2):
    video_output(select2)