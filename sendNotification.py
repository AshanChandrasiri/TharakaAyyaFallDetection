

import requests
import json

serverToken = 'AAAA5j-Z_W0:APA91bG4jbl9RBIsmPNJNNJ4JnJOLCivloprUraMhRmgAU4G0SEgsJyezfsMeqMo1jxMdDNKUI_Xp_RtgMqFifTyy3MsSQ0YM29juUprpsqBHUG9OI3jlx2l24_mRzS7ioMdP85eKvlK'
deviceToken = 'd_Ze7MBWQ6CVN7hEx89c8x:APA91bEJ91IRH2IgXAMG_CoIebz_yAkmHKha4rDwTfCqIfhr803Fh0bbd4A_ut4ecLHOC_yo_7r2-WIo2OaKOP2TkxY7_h5eODoYwBVFx0HDOrs39Zxu7TkPmToubqrdXHzM58Wf9Jl3'

# Push notification sending process
def sendPN(body):
    # Set headers of the API Call
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'key=' + serverToken,
    }

    # Set the body to be transferred
    body = {
        'notification': {'title': 'Fall Detected!',
                         'body': "Open for more details"
                         },
        'to':
        deviceToken,
            'priority': 'high',
        'data': {
            'type' : body.type,
            'image': body.imageUrl
        },
    }

    # Call the POST API call
    response = requests.post(
        "https://fcm.googleapis.com/fcm/send", headers=headers, data=json.dumps(body))
    
    # Checks the response status
    print(response.status_code)

    # Checks the response
    print(response.json())
