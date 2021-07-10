from pykinect2 import PyKinectV2
from pykinect2.PyKinectV2 import *
from pykinect2 import PyKinectRuntime
import numpy as np
import cv2

kinect = PyKinectRuntime.PyKinectRuntime(PyKinectV2.FrameSourceTypes_Infrared)

while True:
    # --- Getting frames and drawing
    if kinect.has_new_infrared_frame():
        frame = kinect.get_last_infrared_frame()
        frame = frame.astype(np.uint8)
        frame = np.reshape(frame, (424, 512))
        img = cv2.cvtColor(frame, cv2.COLOR_GRAY2BGR)
        output = cv2.bilateralFilter(img, 9, 150, 75)
        print(output)
        cv2.imshow('KINECT Video Stream', output)
        frame = None

    key = cv2.waitKey(1)
    if key == 27: break