from google.cloud import bigquery
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
    dataset = None
    logging.info('{} ya existe'.format(dataset_id))

  
  table_id = '{}.{}'.format(dataset_id,tableName)
  squema = []
  try:
    columns = list(data.keys())
    columns.sort()
    for column in columns:
      squema.append(bigquery.SchemaField(column, 'STRING', mode='REQUIRED'))

    table = bigquery.Table(table_id, squema)
    table = client.create_table(table)
    logging.info("Created table {}".format(table_id))
  except Exception as e:
    print(e)
    logging.info('{} ya existe'.format(table_id))

  _insertData(client, data, table_id)



def _insertData(client, data, table_id):
  print(data, table_id)
  try:
    client.insert_rows_json(table_id, [data])
  except Exception as e:
    print(e)
    logging.info('Error insertando datos')



def _add_data(data):
  [listDf, documentNumber, age, weight, sex, experience, efectivity, metricName, gestureType] = data

  playerData = {}
  for df in listDf:
    i = df.columns[5]
    f = df.columns[6]
    std = df.columns[4]
    playerData[i] = str(df[i][0])
    playerData[f] = str(df[f][0])
    playerData[std] = str(df[std][0])
  # print(playerData)
  playerData['idJugador'] = str(documentNumber)
  playerData['edad'] = str(age)
  playerData['peso'] = str(weight)
  playerData['sexo'] = str(sex)
  playerData['experiencia'] = str(experience)
  playerData['efectividad'] = str(efectivity)

  _createSquema(gestureType, metricName, playerData)
  
def startSaveData(body):
  _add_data(body)
