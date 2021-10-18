import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from firebase_admin import auth


class FirestoreApp:
  _app = None

  def __init__(self):
    if self._app is None:
      self._app = self._start_instance()
      self.firestoreI = firestore.client()
      self.authI = auth


  def _start_instance(self): 
    service =  credentials.Certificate('backend-credentials.json')
    return firebase_admin.initialize_app(service)

  def get_firestore_instance(self):
    return self.firestoreI

  def get_auth_instance(self):
    return self.authI
