import os
import argparse
import pandas as pd
import logging
import re
import sys
sys.path.append('..\\utils\\')
import util as u

logging.basicConfig(level=logging.INFO)

# u = Utils()
logger = logging.getLogger(__name__)

def _getExtremities(dataset):
    expressions = ['codo', 'muñeca', 'hombro', 'cadera', 'rodilla', 'tobillo']
    for column in dataset.columns:
        elbow = [column for column in dataset.columns if expressions[0]
                 in column.lower()]
        wrist = [column for column in dataset.columns if expressions[1]
                 in column.lower()]
        shoulder = [
            column for column in dataset.columns if expressions[2] in column.lower()]
        hip = [column for column in dataset.columns if expressions[3]
               in column.lower()]
        knee = [column for column in dataset.columns if expressions[4]
                in column.lower()]
        ankle = [column for column in dataset.columns if expressions[5]
                 in column.lower()]

    return [elbow, wrist, shoulder, hip, knee, ankle]


def _getFiles(root, separator, decimal):
    logging.info('Beginning load files...')

    files = os.listdir(root)
    csv_files = []
    name_player = ''
    for file in files:
        if os.path.isfile(os.path.join(root, file)) and file.endswith(".csv"):
            csv_files.append(file)
            regex = re.search(r'_([a-zA-Z]*)', file)
            name_player = regex.group(1)

    arrayDatasets = []
    for idx, csv_file in enumerate(csv_files):
        csv_root = root + '\\' + csv_file
        dataset = pd.read_csv(csv_root, sep=separator, decimal=decimal)
        newColumns = {}
        for column in dataset.columns:
            newColumns[column] = '{}_{}'.format(column, idx)
        dataset.rename(columns=newColumns, inplace=True)
        arrayDatasets.append(_joinAngles(dataset))

    joinedDataset = pd.concat(arrayDatasets, axis=1)
    _moveInitTimes(joinedDataset, name_player)


def _joinAngles(dataset):
    logging.info('Joining angles...')

    extremities = _getExtremities(dataset)
    dataset = dataset.fillna(0)
    for limb in extremities:
        if len(dataset[limb].columns) > 1:
            columnAux = 0
            nameAux = ''
            for column in limb:
                nameAux = column
                columnAux += dataset[column]
                dataset = dataset.drop([nameAux], 1)
            dataset[nameAux] = columnAux
    return dataset


def _moveInitTimes(dataset, player):
    logging.info('Calculating duration time of movements...')
    extremities = _getExtremities(dataset)
    dataset = dataset.fillna(0)
    timeIndex = []
    for limb in extremities:
        for column in limb:
            mask = dataset[column] != 0
            title = column.split('_')
            timeIndex.append({
                'timeColumn': 'Tiempo (ms)_{}'.format(title[1]),
                'indexMask': dataset[column][mask].index,
                'columnLimb': column
            })

    for idx, element in enumerate(timeIndex):
        firstTime = dataset[element['timeColumn']][element['indexMask'][0]]
        dataMoveDict = {
            '{}{}'.format(element['timeColumn'], idx): (dataset[element['timeColumn']][element['indexMask']] - firstTime).tolist(),
            '{}{}'.format(element['columnLimb'], idx): (dataset[element['columnLimb']][element['indexMask']]).tolist()
        }
        name = element['columnLimb'].replace(' ', '_')
        name = name.replace('/', '%')
        u.createFile(pd.DataFrame(dataMoveDict), os.getcwd(),
            '#PL{}#EX{}'.format(player, name))

    logging.info('Temp file created!')

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('root',
                        help='Ruta de archivos /carpeta1/carpeta2',
                        type=str)
    parser.add_argument('separator',
                        help='Separador del dataset',
                        type=str)
    parser.add_argument('decimal',
                        help='Simbolo de decimal',
                        type=str)

args = parser.parse_args()
_getFiles(args.root, args.separator, args.decimal)
