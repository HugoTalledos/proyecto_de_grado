import argparse
import re
import pandas as pd
import logging
from datetime import datetime
import os
import sys
import matplotlib.pyplot as plt
logging.basicConfig(level=logging.INFO)

sys.path.append('..\\utils\\')
import util as u

logger = logging.getLogger(__name__)

def _average(root, metricName, outputPath, imageName, unit):
	logging.info('Calculating averages')

	files = os.listdir(root)
	for file in files:
		rootFile = '{}/{}'.format(root, file)
		dataset = pd.read_csv(rootFile)
		timeAux = 0
		playerName = re.search(r'#PL([a-zA-Z]*[0-9]*)', file)
		extremity = re.search(r'#EX(\S*[0-9]*)#', file)
		metricAux = 0
		columnsValue = [column for column in dataset.columns if 'Tiempo' not in column]
		columnsTime = [column for column in dataset.columns if 'Tiempo' in column]
		nameTimeAux = ''
		nameValueAux = ''

		for columnTime in columnsTime:
			nameTimeAux = columnTime
			timeAux += dataset[columnTime]
			dataset = dataset.drop([columnTime], 1)
		dataset[nameTimeAux] = timeAux / len(columnsTime)

		for columnValue in columnsValue:
			nameValueAux = columnValue
			metricAux += dataset[columnValue]
			dataset = dataset.drop([columnValue], 1)
		dataset[nameValueAux] = metricAux / len(columnsValue)
		dataset[nameTimeAux] = (dataset[nameTimeAux] * 100) / dataset[nameTimeAux][len(dataset[nameTimeAux]) - 1]

		std = dataset[nameValueAux].std()
		dataset['MaxValue'] = dataset[nameValueAux] + std
		dataset['MinValue'] = dataset[nameValueAux] - std

		yExtremityLabel = (extremity.group(1)).title()
		xTimeLabel = 'Tiempo (%)'
		dataset.rename(columns = { nameValueAux: yExtremityLabel }, inplace=True)
		dataset.rename(columns = { nameTimeAux: xTimeLabel }, inplace=True)
		u.createFile(dataset,
					'{}\\temp'.format(os.getcwd()),
					'#PL{}#EX{}'.format(playerName.group(1), yExtremityLabel))

		plt.plot(dataset[xTimeLabel], dataset[yExtremityLabel], color='blue')
		plt.plot(dataset[xTimeLabel], dataset['MaxValue'], ls= '--',color='black')
		plt.plot(dataset[xTimeLabel], dataset['MinValue'], ls= '--',color='black')
		plt.fill_between(dataset[xTimeLabel], dataset['MaxValue'], dataset['MinValue'], color='lightgray')
		plt.xlabel('Tiempo (%)')
		plt.ylabel('{} {} ({})'.format(metricName, yExtremityLabel, unit))

		os.makedirs('{}/{}/{}'.format(
			outputPath,imageName, playerName.group(1)), exist_ok=True)
		plt.savefig('{}/{}/{}/{}_{}.png'.format(
			outputPath, imageName, playerName.group(1), imageName, yExtremityLabel))
		plt.clf()
	
		logging.info('Chart image created')


if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('root',
						help='Ruta de archivos organizados',
						type=str)
	parser.add_argument('metricName',
						help='Nombre de la metrica a graficar',
						type=str)
	parser.add_argument('outputPath',
						help='Ruta de salida en la que se guardan los archivos finales',
						type=str)
	parser.add_argument('imageName',
						help='Prefijo de archivos de imagen creados',
						type=str)
	parser.add_argument('unit',
						help='Unidad de medida del eje y',
						type=str)

	args = parser.parse_args()
	_average(args.root, args.metricName, args.outputPath, args.imageName, args.unit)