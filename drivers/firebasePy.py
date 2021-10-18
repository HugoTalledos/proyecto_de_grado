import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

_firebaseSDK = None

def getInstance():
  if _firebaseSDK is None:
    return _startInstance()
  else:
    return _firebaseSDK

def _startInstance():
  _firebaseSDK =  credentials.Certificate('backend-credentials.json')
  firebase_admin.initialize_app(_firebaseSDK)
  return firestore.client()

