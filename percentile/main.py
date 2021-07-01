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

def _main(point, labels):
	root = '{}/temp'.format(os.getcwd())
	files = os.listdir(root)
	for label in labels:
		logging.info('Interpolating points for {}'.format(label))
		datasetArray = []
		for file in files:
			dataset = pd.DataFrame()
			calculatedFile = pd.DataFrame()
			percentilCalculatedArray = []
			metricValueArray = []
			fileRoot = '{}/{}'.format(root, file)
			player = re.search(r'#PL([a-zA-Z]*[0-9]*)', file)

			isFile = os.path.isfile(os.path.join(root, file))
			isCsv = file.endswith(".csv")

			if  isFile and isCsv and label in file.lower():
				dataset = pd.read_csv(fileRoot , sep=',', decimal=".")
				timeColumn = dataset.columns[0]
				labelColumn = dataset.columns[1]
				lastTimeValue = dataset[timeColumn][len(dataset) -1]
				points = 100/int(point)
				for step in range(0, 101, int(points)):
					timeValuePercentile = (lastTimeValue * int(step))/100
					value = _interpolation(dataset, timeValuePercentile, timeColumn, labelColumn)
					percentilCalculatedArray.append(timeValuePercentile)
					metricValueArray.append(value)

				calculatedFile[timeColumn] = percentilCalculatedArray
				calculatedFile[labelColumn] = metricValueArray
				datasetArray.append(calculatedFile)
		response = pd.concat(datasetArray, axis=1)
		u.createFile(response,
					'{}\\temp_average'.format(os.getcwd()),
            		'#PL{}#EX{}'.format(player.group(1), label))

def _interpolation(dataset, timeValue, timeLabel, label):
	for j in range(len(dataset)-1):
		if timeValue == dataset[timeLabel][len(dataset) -1]:
			return dataset[label][len(dataset) -1]
		if timeValue == dataset[timeLabel][j]:
			return dataset[label][j]
		if timeValue < dataset[timeLabel][j]:
			div = ((dataset[label][j] - dataset[label][j-1]) / (dataset[timeLabel][j] - dataset[timeLabel][j-1]))
			return dataset[label][j-1] + div * (timeValue - dataset[timeLabel][j-1])

if __name__ == '__main__':
	parser = argparse.ArgumentParser()
	parser.add_argument('point',
						help='Incremento entre puntos',
						type=str)
	parser.add_argument('labels',
						help='Cabeceras de articulasciones a analizar',
						type=str)
	
	args = parser.parse_args()
	labels = u.createArrayLabels(args.labels)
	
	_main(args.point, labels)
