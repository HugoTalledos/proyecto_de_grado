from flask import Flask, request
from flask_cors import CORS
from dotenv import load_dotenv
from functools import wraps
import logging
import sys

from utils.handle_response import errorResponse

sys.path.append('.\\controllers\\')
sys.path.append('.\\drivers\\')
sys.path.append('.\\utils\\')

from graphModeController import startGraphMode
from extractAverageController import startExtractAverage
from percentileController import startPercentile
from compareController import startCompare
from saveDataController import startSaveData
from playerController import createPlayer, getPlayers
from util import getDataset, deletePath
from firebasePy import FirestoreApp
import userController

load_dotenv()
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

firestore = FirestoreApp()
app = Flask(__name__)
CORS(app) 

def validate_token(f):
    @wraps(f)
    def decorator(*args, **kwargs):
      token = None

      if 'Authorization' in request.headers:
        token = request.headers['Authorization']

      if not token:
        return errorResponse(400, 'A valid token is missing')

      try:
        auth = firestore.get_auth_instance()
        db = firestore.get_firestore_instance()
        decoded_token = auth.verify_id_token(token)
        uid = decoded_token['uid']

        query = db.collection('users').where(u'id', u'==', uid)
        docs = query.stream()
        accountExist = False
        for doc in docs:
          accountExist = True
        
        if not accountExist:
          return errorResponse(401, 'Unauthorized user')
        
      except Exception as e:
        print(e)
        return errorResponse(401, 'Token is invalid')

      return f(*args, **kwargs)
    return decorator

@app.route('/graphMode', methods=['POST'])
@validate_token
def startProcces():
  data = request.json
  graphMode = data['graph']
  documentNumber = data['documentNumber']
  separator = data['separator']
  decSeparator = data['decimalSeparator']
  path = '{}/data'.format(documentNumber)
  lenListFiles = len(data['listFiles'])
  playerName = data['name']
  listDataset = []
  response = ''
  if graphMode is True: 
      for idx in range(lenListFiles):
          nameFile = '{}_{}_{}.csv'.format(documentNumber, playerName, idx)
          listDataset.append(getDataset(path, nameFile, separator, decSeparator))

      response = startGraphMode([
          listDataset,
          data['columns'],
          data['metric'],
          data['unity'],
          data['name'],
          documentNumber
      ])

  return response

@app.route('/clearMode', methods=['POST'])
@validate_token
def clearMode():
  deletePath(request.json)
  return { 'success': True, 'data': 'Archivos eliminados exitosamente' }

@app.route('/startProcess', methods=['POST'])
@validate_token
def startProcess():
  body = request.json
  print('------------------------------------------BODY-------------------------------------')
  print(body)
  print('------------------------------------------ENDBODY-------------------------------------')
  documentNumber = body['documentNumber']
  metric = body['metric']
  separator = body['separator']
  decSeparator = body['decimalSeparator']
  lenListFiles = len(body['listFiles'])
  playerName = body['name']
  column = body['columns']
  path = body['rootFiles']
  listDataset = []
  try:
    for idx in range(lenListFiles):
      nameFile = '{}_{}_{}.csv'.format(documentNumber, playerName, idx)
      listDataset.append(getDataset(path, nameFile, separator, decSeparator))
  except:
    return errorResponse(500, 'Error obteniendo archivos ERR#G01')

  listTempDf = startExtractAverage([
    listDataset,
    column,
    body['columnTime'],
  ])

  if not listTempDf['success']:
    return errorResponse(listTempDf['status'], listTempDf['message'])

  tempDf = startPercentile([ column, listTempDf['data'] ])

  if not tempDf['success']:
    return errorResponse(tempDf['status'], tempDf['message'])

  metricName = 'Movimiento Angular' if metric == '1' else 'Velocidad Lineal' if metric == '2' else 'Velocidad Angular'
  nameVariable = 'ma' if metric == '1' else 'vl' if metric == '2' else 'va'
  finalDatasetList = startCompare([
    tempDf['data'],
    metricName,
    body['unity'],
    documentNumber,
    playerName,
    column,
    nameVariable,
    body['gestureType']
  ])

  if not finalDatasetList['success']:
    return errorResponse(finalDatasetList['status'], finalDatasetList['message'])

  response = startSaveData([
    finalDatasetList['data'],
    documentNumber,
    body['age'],
    body['weight'],
    body['sex'],
    body['experience'],
    body['efectivity'],
    metricName.replace(' ', '_'),
    body['gestureType']
  ])
  if not response['success']:
    return errorResponse(response['status'], response['message'])

  return response

@app.route('/users', methods=['POST'])
def createUser():
  response = userController.createUser(firestore, request.json)
  return response

@app.route('/getPlayers', methods=['GET'])
@validate_token
def getPlayersRoute():
  response = getPlayers(firestore)
  return response

@app.route('/createPlayers', methods=['POST'])
@validate_token
def createPlayerRoute():
  response= createPlayer(firestore, request.json)
  return response

if __name__ == '__main__':
	app.run(host='0.0.0.0')
