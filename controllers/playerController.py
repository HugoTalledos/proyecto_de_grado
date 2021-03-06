from utils.handle_response import successResponse, errorResponse
userCollection = 'users'
playerCollection = 'players'

def createPlayer(firestore, data):
  db = firestore.get_firestore_instance()
  try:
    db.collection(playerCollection).document().set({
      'playerName': data['name'],
      'documentNumber': data['documentNumber'],
      'sex': data['sex'],
      'weight': data['weight'],
      'age': data['age'],
      'experience': data['experience'],
      'efectivity': data['efectivity'],
      'processStatus': data['status'],
      'picture': data['photo'],
    })
    return successResponse(True, 'Jugador creado')
  except Exception as e:
    print(e)
    return errorResponse(500, str(e))

def getPlayers(firestore):
  try:
    db = firestore.get_firestore_instance()
    playerList = []
    docs = db.collection(playerCollection).stream()
    for doc in docs:
      playerList.append(doc.to_dict())
    return successResponse(True, playerList)
  except Exception as e:
    print(e)
    return errorResponse(500, str(e))
