from firebasePy import getInstance
from handle_response import successResponse, errorResponse

firestore = getInstance()
userCollection = 'users'

def createUser(data):
  try:
    accountExist = False
    query = firestore.collection(userCollection).where(u'email', u'==', data['email'])
    docs = query.stream()
    for dosc in docs:
      accountExist = True
    if not accountExist:
      firestore.collection(userCollection).document().set({
        'email': data['email'],
        'id': data['userData']['id'],
        'name': data['userData']['name'],
        'locale': data['userData']['locale'],
        'hd': data['userData']['hd'],
        'picture': data['userData']['picture'],
        'permissionId': data['permissionId'],
      })
      return successResponse(True, 'Usuario Creado')
    else:
      return errorResponse(400, 'El usuario ya existe')
  except Exception as e:
    print(e)
    return errorResponse(500, str(e))