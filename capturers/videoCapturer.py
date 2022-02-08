import cv2
import os
from os.path import exists

def detect_from_video(videoPath, callback):
    if exists(videoPath) == False:
        return
    
    cap = cv2.VideoCapture(videoPath)
    i = 0
    while(cap.isOpened()):
        ret, frame = cap.read()
        if (ret == False):
            break
        
        if not callback == None:
            callback(frame, os.path.basename(videoPath), i)
        i += 1
    
    cap.release()
    cv2.destroyAllWindows()