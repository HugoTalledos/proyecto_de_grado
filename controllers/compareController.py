import io
import re
import logging
import sys
import matplotlib.pyplot as plt
logging.basicConfig(level=logging.INFO)

sys.path.append('..\\utils\\')
import util as u

logger = logging.getLogger(__name__)

def _createNormalBand(dataset, xTimeLabel, yExtremityLabel, data):
	[_, metricName, unit, documentNumber, playerName, *_] = data

	plt.plot(dataset[xTimeLabel], dataset[yExtremityLabel], color='blue')
	plt.plot(dataset[xTimeLabel], dataset['MaxValue'], ls= '--',color='black')
	plt.plot(dataset[xTimeLabel], dataset['MinValue'], ls= '--',color='black')
	plt.fill_between(dataset[xTimeLabel], dataset['MaxValue'], dataset['MinValue'], color='lightgray')
	plt.xlabel('Tiempo (%)')
	plt.ylabel('{} {} ({})'.format(metricName, yExtremityLabel, unit))

	root = '{}/images/NormalBand/{}_{}'.format(documentNumber, playerName, yExtremityLabel)
	buf = io.BytesIO()
	plt.savefig(buf, fromat='png')
	u.createImage(root, buf.getvalue())
	plt.clf()
	buf.close()

	logging.info('Chart image created')


def _average(data):
	[listTempDf, metricName, _, playerID, playerName, labels, nameVariable] = data
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
		_createNormalBand(df, xTimeLabel, yExtremityLabel, data)

		df['{}_std_{}'.format(nameVariable, yExtremityLabel)] = std
		df['{}_i_{}'.format(nameVariable, yExtremityLabel)] = df[yExtremityLabel][0]
		df['{}_f_{}'.format(nameVariable, yExtremityLabel)] = df[yExtremityLabel][71]

		fileName = '{}_{}'.format(playerName, yExtremityLabel)
		root = '{0}/data/{1}/{2}'.format(playerID, metricName, fileName)
		u.createFile(df, root)
		datasetList.append(df)
	return datasetList


def startCompare(body):
	[listTempDf, metric, unity, documentNumber, name, labels, nameVariable] = body
	data = [
		listTempDf,
		metric,
		unity,
		documentNumber,
		name,
		labels,
		nameVariable
	]

	datasetList =_average(data)
	return datasetList