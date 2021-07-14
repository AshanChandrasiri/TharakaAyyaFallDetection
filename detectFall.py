from sendNotification import sendPN
import cv2


def detect(foot, knee, hip, shoulder):
    difKneeFoot = foot-knee
    print(f'call method detect {difKneeFoot}')
    if(difKneeFoot <= 25):

        # print(f'------- knee - hip ---------- {knee-hip}')
        # print(f'------- hip - shoulder ---------- {hip-shoulder}')

        # cv2.imshow('fallen', image)
        print(f'fall detected {difKneeFoot}')

        return True
    else:
        # print(f'standing {difKneeFoot}')
        return False


def detectFallType(foot, knee, hip, shoulder):

    difKneeHip = knee - hip

    if(difKneeHip<-20):
        print('Fallen on back')
        return 'Sitting Position'
        # sendPN('completely fallen')


    if(difKneeHip <= 25):
        print('completely fallen')
        # sendPN('completely fallen')
        return 'Lying Position'
    else:
        print('fallen from knee')
        # sendPN('fallen from knee')
        return 'Kneel Position'
