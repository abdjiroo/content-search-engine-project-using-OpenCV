# -*- coding: utf-8 -*-
"""
Created on Wed May 27 19:16:58 2020

@author: visce
"""

import cv2
import math

cap = cv2.VideoCapture('visce.avi');
fps = math.floor(cap.get(cv2.CAP_PROP_FPS))
fourcc = cv2.VideoWriter_fourcc(*'XVID') 
out = cv2.VideoWriter('Output Result.avi' , fourcc , fps , (640,480))
knife_det=cv2.CascadeClassifier('cascadeknife.xml')
gun_det=cv2.CascadeClassifier('cascadeguninhand.xml')

frameRate=0
timeSecond = 0
timeMin=0
n=0
g=0
array=[]
while (True):
    ret,frame=cap.read()
    if not ret:
        break
    frameRate=frameRate+1
    if frameRate == fps :
        timeSecond = timeSecond +1
        frameRate = 0
    if timeSecond == 60:
        timeMin = timeMin+1
        timeSecond = 0
        
    frame = cv2.resize(frame, (640, 480))
    gray = cv2.cvtColor(frame, cv2.COLOR_RGB2GRAY)
    knife=knife_det.detectMultiScale(gray,1.3,7)
    gun=gun_det.detectMultiScale(gray,1.3,7)
    for (x, y, w, h) in knife:
        
        cv2.rectangle(frame, (x, y), (x+w, y+h),(0, 255, 0), 2)
        if n != timeSecond:
            array.append("Knife has been detected in %s minutes and %s seconds\r\n" % (timeMin,timeSecond))
        n = timeSecond 
            
    
    for (a, s, d, f) in gun:
        
        cv2.rectangle(frame, (a, s), (a+d, s+f),(255, 0, 0), 2) 
        if g != timeSecond:
            array.append("Gun has been detected in %s minutes and %s seconds\r\n" % (timeMin,timeSecond))
        g = timeSecond 
        
        
    cv2.imshow('frame',frame)
    out.write(frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break;

with open('Output Text Result.txt', 'w+') as f:
    for item in array:
        f.write("%s\n" % item)   
        
cap.release()
cv2.destroyAllWindows()
cv2.waitKey(1)
        