

import requests
import json

serverToken = 'AAAA5j-Z_W0:APA91bG4jbl9RBIsmPNJNNJ4JnJOLCivloprUraMhRmgAU4G0SEgsJyezfsMeqMo1jxMdDNKUI_Xp_RtgMqFifTyy3MsSQ0YM29juUprpsqBHUG9OI3jlx2l24_mRzS7ioMdP85eKvlK'
deviceToken = 'f_kLdrRbTlG73KWjRn2L5C:APA91bGuHaCvJoWvfZRncr8U4XJHnf3aoPRadAHCke5PDtI2fCYNOsBa3-Vd6xGzGPl44xOAbDmPRuIAHC9wKD7a8vxPmqyxOVp39Tt56uW7wIcAP6fct-M27OVW1o7oAr0EQM_JCHNv'


def sendPN(msg):
    print('------------ SEND PUSH NOIFICATION --------------------')
    headers = {
            'Content-Type': 'application/json',
            'Authorization': 'key=' + serverToken,
        }

    body = {
            'notification': {'title': 'Sending push form python script',
                                'body': msg
                                },
            'to':
                deviceToken,
            'priority': 'high',
            #   'data': dataPayLoad,
            }
    response = requests.post("https://fcm.googleapis.com/fcm/send",headers = headers, data=json.dumps(body))
    print(response.status_code)

    print(response.json())