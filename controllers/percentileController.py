import argparse
import pandas as pd
import logging
import re
import sys
logging.basicConfig(level=logging.INFO)
import os
sys.path.append('..\\utils\\')
import util as u

logger = logging.getLogger(__name__)

def _main(listTempDf, point, labels):
	listDataset = []
	for label in labels:
		logging.info('Interpolating points for {}'.format(label))
		datasetArray = []
		for df in listTempDf:
			calculatedFile = pd.DataFrame()
			percentilCalculatedArray = []
			metricValueArray = []
			isRequired = re.search(label, df.columns[1].lower())
			if isRequired:
				timeColumn = df.columns[0]
				labelColumn = df.columns[1]
				lastTimeValue = df[timeColumn][len(df) -1]
				points = 100/int(point)
				for step in range(0, 101, int(points)):
					timeValuePercentile = (lastTimeValue * int(step))/100
					value = _interpolation(df, timeValuePercentile, timeColumn, labelColumn)
					percentilCalculatedArray.append(timeValuePercentile)
					metricValueArray.append(value)

				calculatedFile[timeColumn] = percentilCalculatedArray
				calculatedFile[labelColumn] = metricValueArray
				datasetArray.append(calculatedFile)
		response = pd.concat(datasetArray, axis=1)
		listDataset.append(response)
	return listDataset

def _interpolation(dataset, timeValue, timeLabel, label):
	for j in range(len(dataset)-1):
		if timeValue == dataset[timeLabel][len(dataset) -1]:
			return dataset[label][len(dataset) -1]
		if timeValue == dataset[timeLabel][j]:
			return dataset[label][j]
		if timeValue < dataset[timeLabel][j]:
			div = ((dataset[label][j] - dataset[label][j-1]) / (dataset[timeLabel][j] - dataset[timeLabel][j-1]))
			return dataset[label][j-1] + div * (timeValue - dataset[timeLabel][j-1])

def startPercentile(data):
	[column, listTempDf] = data
	labels = u.createArrayLabels(column)
	
	response = _main(listTempDf, 100, labels)
	return response
