#-*- coding: utf-8 -*-
import logging
from datetime import datetime
from time import sleep
import os
from shutil import rmtree
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

""" Create File
    Method to create a csv file containing the creation date
    Paramethers:
    data: Dataframe with information
    path: Path where the file will be created
    fileName: Created file name
"""
def createFile(data, path, fileName):
    today = (datetime.today()).strftime('%Y-%m-%d-%H%M%S')
    os.makedirs(path, exist_ok=True)
    data.to_csv(r'{}\\{}#D{}.csv'.format(path, fileName, today),
        index=False)
    logging.info('Temp average file created')


""" Create Array labels
    Method to extract the headrers from a text string concatenated with #
    Paramethers:
    labels: Labels concatenated with #
"""
def createArrayLabels(labels):
	labelsArray = labels.split('#')
	labels = []
	for label in labelsArray:
		labels.append(label)
	return labels


""" Get Extremities
    Get labels ordered per extremity.
    Return a list with labels lists per extremity
    Paramethers:
    dataset: Dataframe with information
    labels: Labels concatenated with #
"""
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


""" PreparePathScheme
    Create the necessary structure for the project
    Paramethers:
    main: Main path where the subfolders will be created
    output: Path where images and final files will be saved 
"""
def preparePathScheme(main, output):
	if os.path.isdir('{}/percentile/temp'.format(main)):
		rmtree('{}/percentile/temp'.format(main))

	if os.path.isdir('{}/percentile/temp_average'.format(main)):
		rmtree('{}/percentile/temp_average'.format(main))

	if os.path.isdir('{}/compare/image'.format(main)):
		rmtree('{}/compare/image'.format(main))

	if os.path.isdir('{}/compare/temp'.format(main)):
		rmtree('{}/compare/temp'.format(main))

	sleep(1)
	logger.info(' --------------------> checking project structure  <-------------------- ')
	os.makedirs('{}/percentile/temp'.format(main), exist_ok=True)
	os.makedirs('{}/percentile/temp_average'.format(main), exist_ok=True)
	os.makedirs('{}/compare/temp'.format(main), exist_ok=True)
	os.makedirs(output, exist_ok=True)
	sleep(1)