firebase_app = None
PROJECT_ID = "falldetection-b32b2"

import firebase_admin
from firebase_admin import credentials
from firebase_admin import storage

cred = credentials.Certificate('falldetection-b32b2-firebase-adminsdk-jjkd0-957adad3ce.json')

# Initialize firebase
firebase_app = firebase_admin.initialize_app(cred, {
        'storageBucket': f"{PROJECT_ID}.appspot.com"
    })

def uploadToFirebase(fileName):
    # Produce the image
    bucket = storage.bucket()
    imageBlob = bucket.blob("/")
    imagePath = fileName
    imageBlob = bucket.blob(fileName)
    imageBlob.upload_from_filename(imagePath)

    imageBlob.make_public()
    # Return firebase link of uploaded image
    return imageBlob.public_url