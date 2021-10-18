from flask import Flask, request
from flask_cors import CORS
import logging
from dotenv import load_dotenv
import sys
sys.path.append('.\\controllers\\')
sys.path.append('.\\drivers\\')
sys.path.append('.\\utils\\')
from startProcessController import getListDocuments
import userController

load_dotenv()
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)


app = Flask(__name__)
CORS(app) 

@app.route('/processPlayer', methods=['POST'])
def startProcces():
  data = request.json
  print('---------REQUEST-----------')
  print(data)
  print('---------END REQUEST-----------')
  getListDocuments()

  return ''

@app.route('/users', methods=['POST'])
def createUser():
  response = userController.createUser(request.json)
  return response

if __name__ == '__main__':
	app.run(host='0.0.0.0')
