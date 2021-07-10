

import requests
import json

serverToken = 'AAAA5j-Z_W0:APA91bG4jbl9RBIsmPNJNNJ4JnJOLCivloprUraMhRmgAU4G0SEgsJyezfsMeqMo1jxMdDNKUI_Xp_RtgMqFifTyy3MsSQ0YM29juUprpsqBHUG9OI3jlx2l24_mRzS7ioMdP85eKvlK'
deviceToken = 'fvgmAjkHTDewQUCLpgC_7N:APA91bFoSdthmO55NhgGKlqdHafi_lg67Bd6jAqPu7OTr1z5y6yRDIzvwEZFkP9D7BSXfZt7AM93dieBI6aCGwnCdOe84KcIHIQda7EOckrhkXq7mP5VyJrMr4KbVuVMzBmGmDOgVEvn'


def sendPN(body):
    print('------------ SEND PUSH NOIFICATION --------------------')
    headers = {
        'Content-Type': 'application/json',
        'Authorization': 'key=' + serverToken,
    }

    body = {
        'notification': {'title': 'Alert !!',
                         'body': body.type
                         },
        'to':
        deviceToken,
            'priority': 'high',
        # 'data': json.dumps(body.__dict__),
    }
    response = requests.post(
        "https://fcm.googleapis.com/fcm/send", headers=headers, data=json.dumps(body))
    print(response.status_code)

    print(response.json())
