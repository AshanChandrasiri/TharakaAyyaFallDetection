from datetime import datetime
from uploadToFirebase import uploadToFirebase
from push_notification_body import PushNotificationBody
from sendNotification import sendPN
import time
import _thread
from detectFall import detect, detectFallType
from distanceCalculator import calcFootHeights, calcHipsHeights, calcKneeHeights, calcShoulderHeights
import cv2
import mediapipe as mp
mp_drawing = mp.solutions.drawing_utils
mp_pose = mp.solutions.pose

# # For static images:
# IMAGE_FILES = []
# with mp_pose.Pose(
#         static_image_mode=True,
#         model_complexity=2,
#         min_detection_confidence=0.5) as pose:
#     for idx, file in enumerate(IMAGE_FILES):
#         image = cv2.imread(file)
#         image_height, image_width, _ = image.shape
#         # Convert the BGR image to RGB before processing.
#         results = pose.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

#         if not results.pose_landmarks:
#             continue
#         # print(
#         #     f'Nose coordinates: ('
#         #     f'{results.pose_landmarks.landmark[0].x * image_width}, '
#         #     f'{results.pose_landmarks.landmark[0].y * image_height})'
#         # )
#         # Draw pose landmarks on the image.
#         annotated_image = image.copy()
#         mp_drawing.draw_landmarks(
#             annotated_image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)
#         cv2.imwrite('/tmp/annotated_image' +
#                     str(idx) + '.png', annotated_image)
#         # Plot pose world landmarks.
#         mp_drawing.plot_landmarks(
#             results.pose_world_landmarks, mp_pose.POSE_CONNECTIONS)

# For webcam input:

forceSkip = True
isInitialToePosition = False
previousToePosition = 0.0
kneeToToe = 0.0
index=1
isSleepMode=False
personHeight=0.0
initialPersonHeight=False


def saveImage():
    # filename = f'{str(datetime.now())}.jpg'
    filename = f'{time.strftime("%Y%m%d-%H%M%S")}.jpg'
    cv2.imwrite(filename, originalImage)
    return filename


def detectFallenType(threadName, delay):
    time.sleep(delay)
    print('*************************************** TREAD stared ******************************')
    fallType = detectFallType(foot=footHeight, knee=kneeHeight,
                              hip=hipsHeight, shoulder=shoulderHeight)
    filename = saveImage()

    firebaseLink = uploadToFirebase(filename)

    body = PushNotificationBody(type=fallType, imageUrl=firebaseLink)
    sendPN(body)

    print('--------------------- FINAL RESULTS ------------------------------')
    print(f'---------------------FALL TYPE : {fallType} ')
    print(f'---------------------Uploaded image : {firebaseLink} ')
    time.sleep(3000)
    # cv2.imshow('after 2 seconds', image)
    # cv2.waitKey(5000)


# sendPN('hi')

cap = cv2.VideoCapture('28.mp4')
with mp_pose.Pose(
        min_detection_confidence=0.5, 
        min_tracking_confidence=0.5) as pose:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            cap.release()
            continue

        # Flip the image horizontally for a later selfie-view display, and convert
        # the BGR image to RGB.
        originalImage = image
        image = cv2.cvtColor(cv2.flip(image, 1), cv2.COLOR_BGR2RGB)
        image_height, image_width, _ = image.shape
        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        results = pose.process(image)

        # Draw the pose annotation on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        try:
            mp_drawing.draw_landmarks(
                image, results.pose_landmarks, mp_pose.POSE_CONNECTIONS)

            footHeight = calcFootHeights(
                results=results, image_height=image_height)
            
            kneeHeight = calcKneeHeights(
                results=results, image_height=image_height)

            hipsHeight = calcHipsHeights(
                results=results, image_height=image_height)

            shoulderHeight = calcShoulderHeights(
                results=results, image_height=image_height)
            
            
            
            
            
            if(initialPersonHeight==False):
                personHeight=footHeight-shoulderHeight

            if(isInitialToePosition==False and personHeight>150):
                previousToePosition=image_height-footHeight
                kneeToToe = footHeight-kneeHeight
                initialPersonHeight = True
                isInitialToePosition=True

            if(index%5==0):
                previousToePosition=image_height-footHeight
                index=index+1

            toePositionDistance = (image_height-footHeight)-previousToePosition

            
            if(kneeToToe-toePositionDistance<10 and personHeight>150):
                print("i am sleeeeeeeeeeeeeeepingggg")
                isSleepMode=True
            elif(personHeight>150):
                isSleepMode=False
            
            # if(isSleepMode==False):
                # print("++++++++++++++++++++++++++++++++++++++++++++")
                # print("previous toe position")
                # print(previousToePosition)
                
                # print("current toe position")
                # print(image_height-footHeight)
                

                
                # print("distance toe position")
                # print(toePositionDistance)
                # print("knee height")
                # print(kneeToToe)
                # print("person height")
                # print(personHeight)
            

            
            if(isSleepMode==False and personHeight>150):
                isFall = detect(foot=footHeight, knee=kneeHeight,
                            hip=hipsHeight, shoulder=shoulderHeight)
                

            if(forceSkip & isFall):
                

                forceSkip = False
                cv2.imshow('1st detection', image)
                print(' /////////// first call after detect /////////////////')

                # Create two threads as follows
                try:
                    _thread.start_new_thread(detectFallenType, ("Thread-1", 2, ))

                except:
                    print("Error: unable to start thread")

            # print(
            #     f'Foot coordinates: ('
            #     f'{ footHeight}, '
            #     '---- knee---- '
            #     f'{kneeHeight})'

            #     '---- hips---- '
            #     f'{hipsHeight})'

            #     '---- shoulder---- '
            #     f'{shoulderHeight})'

            # )
        except:
            print('skipped image')
        # print(
        #     f'Eye coordinates: ('
        #     f'{ round(results.pose_landmarks.landmark[6].x, 2) * image_width}, '
        #     f'{round(results.pose_landmarks.landmark[6].y, 2) * image_height})')

        cv2.imshow('MediaPipe Pose', image)
        if cv2.waitKey(5) & 0xFF == 27:
            break
