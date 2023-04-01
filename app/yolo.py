import cv2
import numpy as np
net = cv2.dnn.readNet("yolov3.weights", "yolov3.cfg")
classes = []
with open("coco.names", "r") as f:
    classes = [line.strip() for line in f.readlines()]
desired_classes = ['car', 'motorbike', 'truck']
conf_threshold = 0.5
cap = cv2.VideoCapture("input.mp4")
while True:
    ret, frame = cap.read()
    if not ret:
        break
    height, width, _ = frame.shape
    blob = cv2.dnn.blobFromImage(
        frame, 1 / 255.0, (416, 416), swapRB=True, crop=False)
    net.setInput(blob)
    layer_names = net.getLayerNames()
    output_layers = [layer_names[i[0] - 1]
                     for i in net.getUnconnectedOutLayers()]
    outputs = net.forward(output_layers)
    for output in outputs:
        for detection in output:
            scores = detection[5:]
            class_id = np.argmax(scores)
            confidence = scores[class_id]
            if classes[class_id] in desired_classes and confidence > conf_threshold:
                center_x = int(detection[0] * width)
                center_y = int(detection[1] * height)
                w = int(detection[2] * width)
                h = int(detection[3] * height)
                x = int(center_x - w / 2)
                y = int(center_y - h / 2)
                obj = frame[y:y+h, x:x+w]
                np.save(f"{classes[class_id]}_{confidence:.2f}.npy", obj)
cap.release()
