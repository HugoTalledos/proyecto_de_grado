import logging
logging.basicConfig(level=logging.INFO)
import subprocess
from common import config
from time import sleep
import os
from shutil import rmtree

logger = logging.getLogger(__name__)

def main(data):
	for path in data['dataPath']:
		_preparePathScheme(data['mainPath'], data['clearMode'], data['output'])

		if data['graphMode'] is True:
			_graphMode(data)
			data['clearMode'] = True

		if data['clearMode'] is False:
			_extract(path, data['mainPath'], data['separator'],
				data['decimalSeparator'], data['columnsLabels'], data['timeColumn'])
			_percentile(data['mainPath'], data['point'], data['autoDelete'],
				data['columnsLabels'])
			_compare(data['mainPath'], data['metricName'], data['output'], data['imageName'],
				data['unit'])

def _preparePathScheme(main, clearMode, output):
	logger.info(' -------------------->       Clear Mode: {}      <-------------------- '.format(clearMode))
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

def _graphMode(data):
	path = data['graphModePath']
	header = data['graphHeader']
	metric = data['metricName'] 
	unit = data['unit'] 
	output = data['output']
	logger.info(' --------------------> Graph Mode init  <-------------------- ')
	subprocess.run(['python', 'main.py', path, header, metric, unit, output], cwd='./graph_mode')

def _extract(data, main, separator, decimal, labels, timeColumn):
	logger.info(' --------------------> Starting data organization  <-------------------- ')
	subprocess.run(['python', 'main.py', data, separator, decimal, labels, timeColumn], cwd='./extract_average')
	logger.info(' --------------------> Moving temp files  <-------------------- ')
	subprocess.run(['move', r'{}\extract_average\*.csv'.format(main), r'{}\percentile\temp'.format(main)], shell=True)
	sleep(1.5)
	subprocess.run(['cls'], shell=True)

def _percentile(main, point, delete, columnsLabels):
	logger.info(' --------------------> Starting data interpolation  <-------------------- ')
	subprocess.run(['python', 'main.py', point, columnsLabels], cwd='./percentile')
	if bool(delete):
		logger.info(' --------------------> Removing temp files  <-------------------- ')
		rmtree(r'{}\percentile\\temp'.format(main))
		sleep(1)
	

def _compare(main , metricName, output, imageName, unit):
	logger.info(' --------------------> Starting compare process <-------------------- ')
	subprocess.run(['python', 'main.py', r'{}\percentile\temp_average'.format(main), metricName, output, imageName, unit], cwd='./compare')

if __name__ == '__main__':
	data = {
		"dataPath": config()['dataPath'], 
		"mainPath": config()['mainPath'],
		"point": config()['points'],
		"autoDelete": eval(config()['autoDeleteMode']),
		"metricName": config()['metricName'],
		"output": config()['outputPath'],
		"columnsLabels": config()['columnsLabels'],
		"timeColumn": config()['timeColumn'],
		"imageName": config()['imageName'],
		"clearMode": eval(config()['clearMode']),
		"graphMode": eval(config()['graphMode']),
		"graphHeader": config()['graphHeader'],
		"graphModePath": config()['graphModePath'],
		"separator": config()['separator'],
		"decimalSeparator": config()['decimalSeparator'],
		"unit": config()['units']
	}

	main(data)
