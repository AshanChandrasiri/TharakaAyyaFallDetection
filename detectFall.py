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


fallType = {
    "FROM_KNEE": 0,
    "FULL": 1,
}


def detectFallType(foot, knee, hip, shoulder):
  
    difKneeHip = knee - hip
    if(difKneeHip <= 25):
        print('completely fallen')
        sendPN('completely fallen')
        return 0
    else:
        print('fallen from knee')
        sendPN('fallen from knee')
        return 1
