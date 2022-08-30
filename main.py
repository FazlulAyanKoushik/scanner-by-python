import urllib.request as req
from xml.dom.expatbuilder import FragmentBuilder
import numpy as np
import cv2
from PIL import Image
import time
import os

url = 'http://192.168.1.100:8080/shot.jpg'
path_out = 'E:\Projects\Python Projects\scanner-by-python\Scanned File'

while True:
    img = req.urlopen(url)
    img_bytes = bytearray(img.read())
    img_np = np.array(img_bytes, dtype = np.uint8)
    frame = cv2.imdecode(img_np, -1)
    frame_cvt = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    frame_blur = cv2.GaussianBlur(frame_cvt, (5,5), 0)
    frame_edge = cv2.Canny(frame_blur, 30,50)
    contours, h = cv2.findContours(frame_edge, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        max_contour = max(contours, key=cv2.contourArea)
        x, y, w, h = cv2.boundingRect(max_contour)
        if cv2.contourArea(max_contour) > 10000:
            cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 255), 2)
            object_only = frame[y:y+h, x:x+w]
    
            cv2.imshow('My Smart Scanner', object_only)
            
            if cv2.waitKey(1) == ord('q'):
                img_pill = Image.fromarray(object_only)
                time_str = time.strftime('%Y -%m -%d -%H -%M -%S')
                img_pill.save(os.path.join(path_out, f'my scanned file{time_str}.pdf'))
                print(time_str)