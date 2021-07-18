from sendNotification import sendPN
import cv2

# Algorithm : Fall detection 
def detect(foot, knee, hip, shoulder):
    difKneeFoot = foot-knee

    # Detect fall
    if(difKneeFoot <= 25):
        print(f'fall detected {difKneeFoot}')
        return True
    else:
        return False

# Algorithm : Fall type identification
def detectFallType(foot, knee, hip, shoulder,index):

    difKneeHip = knee - hip
    
    if(difKneeHip< -20):
        return 'Sitting Position'
        
    if(difKneeHip <= 25):
        return 'Lying Position'
    else:
        return 'Kneel Position'
