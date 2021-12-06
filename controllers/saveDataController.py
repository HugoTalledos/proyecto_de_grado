from google.cloud import bigquery
from utils.handle_response import successResponse, errorResponse
import logging

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

def _createSquema(gestureType, tableName, data):
  client = bigquery.Client()
  dataset_id = "{}.{}".format(client.project, gestureType)
  dataset = None
  try:
    dataset = bigquery.Dataset(dataset_id)
    dataset.location = 'US'
    dataset = client.create_dataset(dataset)
    logging.info("Created dataset {}".format(dataset_id))
  except Exception as e:
    print(e)
    logging.info('Dataset {} ya existe'.format(dataset_id))

  
  table_id = '{}.{}'.format(dataset_id,tableName)
  squema = []
  try:
    columns = list(data.keys())
    columns.sort()
    for column in columns:
      squema.append(bigquery.SchemaField(column, 'STRING'))

    table = bigquery.Table(table_id, squema)
    table = client.create_table(table)
    logging.info("Created table {}".format(table_id))
  except Exception as e:
    print(e)
    logging.info('Tabla {} ya existe'.format(table_id))

  return _insertData(client, data, table_id)



def _insertData(client, data, table_id):
  try:
    client.insert_rows_json(table_id, [data])
    logging.info('Datos insertados en {}'.format(table_id))
    return successResponse(True, 'Datos insertados')
  except Exception as e:
    print(e)
    logging.info('Error insertando datos')
    return { 'status': 500, 'success':False, 'message': 'Error insertando en BD. ERR#SD02' }



def _add_data(data):
  [listDf, documentNumber, age, weight, sex, experience, efectivity, metricName, gestureType] = data

  playerData = {}
  try:
    for df in listDf:
      i = df.columns[5]
      f = df.columns[6]
      std = df.columns[4]
      playerData[i.replace('ñ', 'n')] = str(df[i][0])
      playerData[f.replace('ñ', 'n')] = str(df[f][0])
      playerData[std.replace('ñ', 'n')] = str(df[std][0])
  except:
    return { 'status': 500, 'success':False, 'message': 'Error insertando en BD. ERR#SD01' }

  playerData['idJugador'] = str(documentNumber)
  playerData['edad'] = str(age)
  playerData['peso'] = str(weight)
  playerData['sexo'] = str(sex)
  playerData['experiencia'] = str(experience)
  playerData['efectividad'] = str(efectivity)

  gestureName = 'Saque_con_salto' if gestureType == '1' else 'Saque_sin_salto' if gestureType == '2' else 'Remate'

  return _createSquema(gestureName, metricName, playerData)
  
def startSaveData(body):
 return  _add_data(body)
