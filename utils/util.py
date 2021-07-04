#-*- coding: utf-8 -*-
import logging
from datetime import datetime
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

def createFile(data, path, nameFile):
	today = (datetime.today()).strftime('%Y-%m-%d-%H%M%S')
	data.to_csv(r'{}\\{}#D{}.csv'.format(
        path, nameFile, today),index=False)
	logging.info('Temp average file created')

def createArrayLabels(labels):
	labelsArray = labels.split('#')
	labels = []
	for label in labelsArray:
		labels.append(label)
	return labels

def getExtremities(dataset, labels):
    expressions = createArrayLabels(labels)
    arrayExtemitiesLabels = []
    for label in expressions:
        columnsLabels = []
        for column in dataset.columns:
            if label.lower() in column.lower():
                columnsLabels.append(column)
        arrayExtemitiesLabels.append(columnsLabels)
    return arrayExtemitiesLabels