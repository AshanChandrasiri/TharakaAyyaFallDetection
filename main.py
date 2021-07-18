from datetime import datetime
from uploadToFirebase import uploadToFirebase
from push_notification_body import PushNotificationBody
from sendNotification import sendPN
import time
import _thread
from detectFall import detect, detectFallType
from distanceCalculator import calcFootHeights, calcHipsHeights, calcKneeHeights, calcShoulderHeights
import cv2
import matplotlib.pyplot as plt
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# Variables
forceSkip = True
isInitialToePosition = False
previousToePosition = 0.0
kneeToToe = 0.0
index=0
isSleepMode=False
personHeight=0.0
initialPersonHeight=False
kneePositions = []
toePositions = []
hipPositions = []
shoulderPositions = []
indexes = []
thresholdSleepLimit=0.0


# Saving image to make it ready to upload to firebase
def saveImage():
    filename = f'{time.strftime("%Y%m%d-%H%M%S")}.jpg'
    cv2.imwrite(filename, originalImage)
    return filename

# Process of Fall type identification
def detectFallenType(threadName, delay):
    time.sleep(delay)
    
    # Idenitfy the fall type
    fallType = detectFallType(foot=footHeight, knee=kneeHeight,
                              hip=hipsHeight, shoulder=shoulderHeight,index=index)
    
    # Save a snapshot of the fall
    filename = saveImage()

    # Upload the image to firebase
    firebaseLink = uploadToFirebase(filename)

    # Send the push notification to the care taker
    # Body : fall details and the snapshot
    body = PushNotificationBody(type=fallType, imageUrl=firebaseLink)
    sendPN(body)

    time.sleep(3000)

# Capture video stream
cap = cv2.VideoCapture('25.mp4')

with mp_pose.Pose(
        min_detection_confidence=0.5, 
        min_tracking_confidence=0.5) as pose:
    while cap.isOpened():

        # Get image frames
        success, image = cap.read()
        if not success:
            # Generate the plot diagram
            plt.plot(indexes, kneePositions)
            plt.plot(indexes, toePositions)
            plt.xlabel('Frame Index')
            plt.ylabel('Vertical Height')
            plt.show()
            
            # If loading a video, use 'break' instead of 'continue'.
            cap.release()
            continue

        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        originalImage = image
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)

        # Get the image orientation
        image_height, image_width, _ = image.shape

        # Set the sleeping threshold
        thresholdSleepLimit = image_height*0.5

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False

        # Process the frame for marking the skeleton points
        results = pose.process(image)

        
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        try:
            # Draw the pose annotation on the image.
            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            # Calibrating the toe position
            footHeight = calcFootHeights(
                results=results, image_height=image_height)
            
            # Calibrating the knee position
            kneeHeight = calcKneeHeights(
                results=results, image_height=image_height)

            # Calibrating the hip position
            hipsHeight = calcHipsHeights(
                results=results, image_height=image_height)

            # Calibrating the shoulder position
            shoulderHeight = calcShoulderHeights(
                results=results, image_height=image_height)
            
            # Data preparation for plots
            indexes.insert(index,index)
            kneePositions.insert(index,image_height-(kneeHeight-footHeight))
            toePositions.insert(index,image_height-(hipsHeight- footHeight))
            hipPositions.insert(index,image_height-hipsHeight)
            shoulderPositions.insert(index,image_height-shoulderHeight)
            index = index+1

            current_person_height=footHeight-shoulderHeight

            # Ignoring the false positive person identifications
            if(personHeight-current_person_height<10 ):
                forceSkip=True
            
            # Calibrate person height
            if(initialPersonHeight==False):
                personHeight=footHeight-shoulderHeight

            if(personHeight>100):
                # disable person height check
                initialPersonHeight=True

            # Set sleeping status
            if(personHeight>100):
                if(footHeight<thresholdSleepLimit and kneeHeight<thresholdSleepLimit):
                    
                    isSleepMode=True
                else:
                    isSleepMode=False
           

            # Detect Fall
            if(isSleepMode==False and personHeight>100):
                isFall = detect(foot=footHeight, knee=kneeHeight,
                            hip=hipsHeight, shoulder=shoulderHeight)
                
            # Once fall detected, start thread for fall type identification process
            if(forceSkip & isFall):
                forceSkip = False
                cv2.imshow('1st detection', image)
                
                # Start thread
                try:
                    _thread.start_new_thread(detectFallenType, ("Thread-1", 2, ))

                except:
                    print("Error: unable to start thread")

            
        except:
            # Skipped the frame when it does not satisfy the requirements
            print('skipped image')
       

        cv2.imshow('MediaPipe Pose', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
