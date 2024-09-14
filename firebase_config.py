# firebase_config.py

import firebase_admin
from firebase_admin import credentials, storage

# Initialize Firebase app with credentials
cred = credentials.Certificate('firebase_key.json')
firebase_admin.initialize_app(cred, {
    'storageBucket': 'mirrorlink-22549.appspot.com'
})
