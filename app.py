from flask import Flask, request
from flask_cors import CORS
import logging
from dotenv import load_dotenv
import sys

sys.path.append('.\\controllers\\')
sys.path.append('.\\drivers\\')
sys.path.append('.\\utils\\')

from graphModeController import startGraphMode
from util import getDataset
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

@app.route('/users', methods=['POST'])
def createUser():
  response = userController.createUser(firestore, request.json)
  return response

if __name__ == '__main__':
	app.run(host='0.0.0.0')
