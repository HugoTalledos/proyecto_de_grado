import io
import re
import logging
import sys
import matplotlib.pyplot as plt
logging.basicConfig(level=logging.INFO)

import utils.util as u

logger = logging.getLogger(__name__)

def _createNormalBand(dataset, xTimeLabel, yExtremityLabel, data):
	[_, metricName, unit, documentNumber, playerName, _, _, gestureName] = data

	plt.plot(dataset[xTimeLabel], dataset[yExtremityLabel], color='blue')
	plt.plot(dataset[xTimeLabel], dataset['MaxValue'], ls= '--',color='black')
	plt.plot(dataset[xTimeLabel], dataset['MinValue'], ls= '--',color='black')
	plt.fill_between(dataset[xTimeLabel], dataset['MaxValue'], dataset['MinValue'], color='lightgray')
	plt.xlabel('Tiempo (%)')
	plt.ylabel('{} {} ({})'.format(metricName, yExtremityLabel, unit))

	root = '{0}/images/{1}/{2}/{2}_{3}_{4}'.format(documentNumber, gestureName, metricName, playerName, yExtremityLabel)
	buf = io.BytesIO()
	plt.savefig(buf, fromat='png')
	u.createImage(root, buf.getvalue())
	plt.clf()
	buf.close()

	logging.info('Chart image created')


def _average(data):
	[listTempDf, metricName, _, playerID, playerName, labels, nameVariable, gestureName] = data
	logging.info('Calculating averages')
	columns = u.createArrayLabels(labels)
	datasetList = []

	for df in listTempDf:
		extremity = ''
		for column in columns:
			extremity = column if re.search(column, df.columns[1].lower()) else extremity

		timeAux = 0
		metricAux = 0
		columnsValue = [column for column in df.columns if 'Tiempo' not in column]
		columnsTime = [column for column in df.columns if 'Tiempo' in column]
		nameTimeAux = ''
		nameValueAux = ''

		for columnTime in columnsTime:
			nameTimeAux = columnTime
			timeAux += df[columnTime]
			df = df.drop([columnTime], 1)
		df[nameTimeAux] = timeAux / len(columnsTime)

		for columnValue in columnsValue:
			nameValueAux = columnValue
			metricAux += df[columnValue]
			df = df.drop([columnValue], 1)
		df[nameValueAux] = metricAux / len(columnsValue)
		df[nameTimeAux] = (df[nameTimeAux] * 100) / df[nameTimeAux][len(df[nameTimeAux]) - 1]

		std = df[nameValueAux].std()
		df['MaxValue'] = df[nameValueAux] + std
		df['MinValue'] = df[nameValueAux] - std

		yExtremityLabel = extremity.title()

		xTimeLabel = 'Tiempo (%)'
		df.rename(columns = { nameValueAux: yExtremityLabel }, inplace=True)
		df.rename(columns = { nameTimeAux: xTimeLabel }, inplace=True)

		# Create image with normal band 
		try:
			_createNormalBand(df, xTimeLabel, yExtremityLabel, data)
		except:
			return { 'status': 500, 'success':False, 'message': 'Error creando banda normal. ERR#G02' }

		df['{}_std_{}'.format(nameVariable, yExtremityLabel)] = std
		df['{}_i_{}'.format(nameVariable, yExtremityLabel)] = df[yExtremityLabel][0]
		df['{}_f_{}'.format(nameVariable, yExtremityLabel)] = df[yExtremityLabel][71]

		fileName = '{}_{}'.format(playerName, yExtremityLabel)
		root = '{0}/data/{1}/{2}/{3}'.format(playerID, gestureName, metricName, fileName)
		try:
			u.createFile(df, root)
		except:
			{ 'status': 500, 'success':False, 'message': 'Error creando Archivo final. ERR#G03' }
		datasetList.append(df)
	return { 'success': True, 'data': datasetList }


def startCompare(body):
	[listTempDf, metric, unity, documentNumber, name, labels, nameVariable, gestureType] = body
	gestureName = 'Saque_con_salto' if gestureType == '1' else 'Saque_sin_salto' if gestureType == '2' else 'Remate'

	data = [
		listTempDf,
		metric,
		unity,
		documentNumber,
		name,
		labels,
		nameVariable,
		gestureName
	]

	datasetList =_average(data)
	return datasetList