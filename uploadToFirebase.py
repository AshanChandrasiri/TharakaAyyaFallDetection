from google.cloud import storage
from firebase import firebase
import os
os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="./falldetection-b32b2-firebase-adminsdk-jjkd0-957adad3ce.json"
# firebase = firebase.FirebaseApplication('<your firebase database path>')
# client = storage.Client()
# bucket = client.get_bucket('images')
# # posting to firebase storage
# imageBlob = bucket.blob("/")
# imagePath = "./cat.jpg"
# imageBlob = bucket.blob("cat.jpg")
# imageBlob.upload_from_filename(imagePath)


# from google.cloud import storage
# storage_client = storage.Client()
# bucket = storage_client.bucket("images")
# blob = bucket.blob("cat.jpg")
# blob.upload_from_filename("cat.jpg")


# from google.cloud import storage
# from firebase import firebase
# import os
# # You just get your CREDENTIALS on previous step
# os.environ["GOOGLE_APPLICATION_CREDENTIALS"]="filePathTo.json"  
# db_url='https://test-XXXXX.firebaseio.com'   # Your project url
# firebase = firebase.FirebaseApplication(db_url,None)
# client = storage.Client()
# bucket = client.get_bucket('test-XXXXX.appspot.com')
# imageBlob = bucket.blob("/")
# imagePath = "path/to/dir/" + fileName  # Replace with your own path
# imageBlob = bucket.blob(fileName)
# imageBlob.upload_from_filename(imagePath)

# import firebase_admin
# from firebase_admin import credentials
# from firebase_admin import storage

# cred = credentials.Certificate('./falldetection-b32b2-firebase-adminsdk-jjkd0-957adad3ce.json')
# firebase_admin.initialize_app(cred, {
#     'storageBucket': 'gs://falldetection-b32b2.appspot.com'
# })

# bucket = storage.bucket()

# imageBlob = bucket.blob("/")
# imagePath = "./cat.jpg"  # Replace with your own path
# imageBlob = bucket.blob("image1.jpg")
# imageBlob.upload_from_filename(imagePath)
firebase_app = None
PROJECT_ID = "falldetection-b32b2"

import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

cred = credentials.Certificate('falldetection-b32b2-firebase-adminsdk-jjkd0-957adad3ce.json')


firebase_app = firebase_admin.initialize_app(cred, {
        # 'projectId': PROJECT_ID,
        'storageBucket': f"{PROJECT_ID}.appspot.com"
    })

def uploadToFirebase(fileName):
    bucket = storage.bucket()
    imageBlob = bucket.blob("/")
    imagePath = fileName
    imageBlob = bucket.blob(fileName)
    imageBlob.upload_from_filename(imagePath)

    imageBlob.make_public()
    print('********************************* FIREBASE LINK ************************')
    print(imageBlob.public_url)
    return imageBlob.public_url