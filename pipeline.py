import logging
logging.basicConfig(level=logging.INFO)
import subprocess
from common import config
from time import sleep
from shutil import rmtree
import sys
sys.path.append('.\\utils\\')
import util as u

logger = logging.getLogger(__name__)

def main(data):
	logger.info(' -------------------->       Clear Mode: {}      <-------------------- '.format(data['clearMode']))
	for path in data['dataPath']:
		u.preparePathScheme(data['mainPath'], data['output'])

		if data['graphMode'] is True:
			_graphMode([
				data['graphModePath'],
				data['graphHeader'],
				data['metricName'],
				data['unit'],
				data['output']
			])
			data['clearMode'] = True

		if data['clearMode'] is False:
			_extract([
				path,
				data['mainPath'],
				data['separator'],
				data['decimalSeparator'],
				data['columnsLabels'],
				data['timeColumn'],
				data['fileName']
			])

			_percentile([
				data['mainPath'],
				data['point'],
				data['autoDelete'],
				data['columnsLabels']
			])

			_compare([
				data['mainPath'],
				data['metricName'],
				data['output'],
				data['imageName'],
				data['unit'],
			])

			_save_data([
				path,
				data['mainPath'],
				data['fileName']
			])

def _graphMode(data):
	[path, header, metric, unit, output] = data
	logger.info(' --------------------> Graph Mode init  <-------------------- ')
	subprocess.run([
		'python', 'main.py',
		path,
		header,
		metric,
		unit,
		output], cwd='./graph_mode')

def _extract(data):
	[path, main, separator, decimal, labels, fileName, timeColumn] = data
	logger.info(' --------------------> Starting data organization  <-------------------- ')
	subprocess.run([
		'python', 'main.py',
		path,
		separator,
		decimal,
		labels,
		timeColumn,
		fileName], cwd='./extract_average')

	logger.info(' --------------------> Moving temp files  <-------------------- ')
	subprocess.run([
		'move',
		r'{}\extract_average\*.csv'.format(main),
		r'{}\percentile\temp'.format(main)], shell=True)
	sleep(1.5)
	subprocess.run(['cls'], shell=True)

def _percentile(data):
	[main, point, delete, columnsLabels] = data
	logger.info(' --------------------> Starting data interpolation  <-------------------- ')
	subprocess.run(['python', 'main.py', point, columnsLabels], cwd='./percentile')

	if bool(delete):
		logger.info(' --------------------> Removing temp files  <-------------------- ')
		rmtree(r'{}\percentile\\temp'.format(main))
		sleep(1)

def _compare(data):
	[main, metricName, output, imageName, unit] = data
	logger.info(' --------------------> Starting compare process <-------------------- ')
	subprocess.run([
		'python', 'main.py',
		r'{}\percentile\temp_average'.format(main),
		metricName,
		output,
		imageName,
		unit], cwd='./compare')

def _save_data(data):
	[path, fileRoot, fileName] = data
	logger.info(' --------------------> Savign data <-------------------- ')
	subprocess.run(
		['python', 'main.py', path, fileRoot, fileName],
		cwd='./save_data'
	)

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
		"unit": config()['units'],
		"fileName": config()['fileName']
	}

	main(data)
