import cv2
from detection import AccidentDetectionModel
import numpy as np
import os
from alert import sendAlert

model = AccidentDetectionModel("model.json", 'model_weights.h5')
font = cv2.FONT_HERSHEY_SIMPLEX


def processVid(accFound, name):
    video = cv2.VideoCapture(name)
    fps = video.get(cv2.CAP_PROP_FPS)
    total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
    accidents = {}
    maxi = 0
    i = 0
    print("Processing started...")
    while True:
        ret, frame = video.read()
        if ret:
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            roi = cv2.resize(gray_frame, (250, 250))
            pred, prob = model.predict_accident(roi[np.newaxis, :, :])
            if(pred == "Accident"):
                prob = (round(prob[0][0]*100, 5))
                # print(prob)
                if(prob > 98.8):
                    position_ms = video.get(cv2.CAP_PROP_POS_MSEC)
                    maxi = max(prob, maxi)
                    print(prob)
                    accFound = True
                    accidents[prob] = position_ms / 1000
        else:
            break
    print("Processing ended...")
    if(len(accidents) > 0):
        print("Accident with highest probabilty found at t=",
              accidents[maxi], "s")
    return accFound


if __name__ == '__main__':
    processVid()
