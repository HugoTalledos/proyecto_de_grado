from flask import Flask, request
from flask_cors import CORS
import logging
from dotenv import load_dotenv
import sys

sys.path.append('.\\controllers\\')
sys.path.append('.\\drivers\\')
sys.path.append('.\\utils\\')

from graphModeController import startGraphMode
from extractAverageController import startExtractAverage
from percentileController import startPercentile
from compareController import startCompare
from saveDataController import startSaveData
from util import getDataset, deletePath
from firebasePy import FirestoreApp
import userController

load_dotenv()
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

firestore = FirestoreApp()
app = Flask(__name__)
CORS(app) 

@app.route('/graphMode', methods=['POST'])
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
def clearMode():
  deletePath(request.json)
  return { 'success': True, 'data': 'Archivos eliminados exitosamente' }

@app.route('/startProcess', methods=['POST'])
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
  column = body['column']
  path = '{}/data'.format(documentNumber)
  listDataset = []

  for idx in range(lenListFiles):
    nameFile = '{}_{}_{}.csv'.format(documentNumber, playerName, idx)
    listDataset.append(getDataset(path, nameFile, separator, decSeparator))

  listTempDf = startExtractAverage([
    listDataset,
    column,
    body['timeColumn'],
  ])
  tempDf = startPercentile([ column, listTempDf ])

  metricName = 'Movimiento Angular' if metric == '1' else 'Velocidad Lineal' if metric == '2' else 'Velocidad Angular'
  nameVariable = 'ma' if metric == '1' else 'vl' if metric == '2' else 'va'
  finalDatasetList = startCompare([
    tempDf,
    metricName,
    body['unity'],
    documentNumber,
    playerName,
    column,
    nameVariable
  ])

  startSaveData([
    finalDatasetList,
    documentNumber,
    body['age'],
    body['weight'],
    body['sex'],
    body['experience'],
    body['efectivity'],
    metricName.replace(' ', '_'),
    body['gestureType']
  ])
  return ''

@app.route('/users', methods=['POST'])
def createUser():
  response = userController.createUser(firestore, request.json)
  return response

if __name__ == '__main__':
	app.run(host='0.0.0.0')
