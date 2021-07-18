# Model: body of the push notification data passed 
class PushNotificationBody:
    def __init__(self, type, imageUrl):
        self.type = type
        self.imageUrl = imageUrl