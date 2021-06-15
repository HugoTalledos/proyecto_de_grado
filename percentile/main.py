import argparse
import pandas as pd
import logging
import re
import sys
from datetime import datetime
logging.basicConfig(level=logging.INFO)
import os
sys.path.append('..\\utils\\')
import util as u

logger = logging.getLogger(__name__)

def _main(point, expressions):
	root = '{}/temp'.format(os.getcwd())
	files = os.listdir(root)
	for limb in expressions:
		datasetarray = []
		logging.info('Interpolating points for {}'.format(limb))
		for file in files:
			dataset = pd.DataFrame()
			calculatedFile = pd.DataFrame()
			percentilCalculatedArray = []
			metricValueArray = []
			fileRoot = '{}/{}'.format(root, file)
			player = re.search(r'#PL([a-zA-Z]*[0-9]*)', file)

			if os.path.isfile(os.path.join(root, file)) and file.endswith(".csv") and limb in file.lower():
				dataset = pd.read_csv(fileRoot , sep=',', decimal=".")
				timeRow = dataset.columns[0]
				limbRow = dataset.columns[1]
				lastTimeValue = dataset[timeRow][len(dataset) -1]
				for i in range(int(point), 101, int(point)):
					percentil = (lastTimeValue * i)/100
					value = _interpolation(dataset, percentil, timeRow, limbRow)
					percentilCalculatedArray.append(percentil)
					metricValueArray.append(value)
				calculatedFile[timeRow] = percentilCalculatedArray
				calculatedFile[limbRow] = metricValueArray
				datasetarray.append(calculatedFile)
		res = pd.concat(datasetarray, axis=1)
		u.createFile(res,
					'{}\\temp_average'.format(os.getcwd()),
            		'#PL{}#EX{}'.format(player.group(1), limb))


def _interpolation(dataset, percentil, time, limb):
	for j in range(len(dataset)-1):
		if percentil == dataset[time][len(dataset) -1]:
			return dataset[limb][len(dataset) -1]
		if percentil == dataset[time][j]:
			return dataset[limb][j]
		if percentil < dataset[time][j]:
			div = ((dataset[limb][j] - dataset[limb][j-1]) / (dataset[time][j] - dataset[time][j-1]))
			interpolation = dataset[limb][j-1] + div * (percentil - dataset[time][j-1])
			
			return interpolation

def _createArrayLabels(labels):
	labelsArray = labels.split('#')
	labels = []
	for label in labelsArray:
		labels.append(label)
	return labels

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('point',
						help='Incremento entre puntos',
						type=str)
	parser.add_argument('labels',
						help='Cabeceras de articulasciones a analizar',
						type=str)
	
	args = parser.parse_args()
	labels = _createArrayLabels(args.labels)

	_main(args.point, labels)
