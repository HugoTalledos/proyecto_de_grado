import os
import argparse
import pandas as pd
import logging
import re
import sys
sys.path.append('..\\utils\\')
import util as u

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

def _getFiles(data):
    [root, separator, decimal, labels, timeColumn] = data
    logging.info('Beginning load files...')

    files = os.listdir(root)
    csv_files = []
    name_player = ''
    playerID = ''
    for file in files:
        if os.path.isfile(os.path.join(root, file)) and file.endswith(".csv"):
            csv_files.append(file)
            regex = re.search(r'([0-9]*)_([a-zA-Z]*)', file)
            playerID = regex.group(1)
            name_player = regex.group(2)

    arrayDatasets = []
    for idx, csv_file in enumerate(csv_files):
        csv_root = root + '\\' + csv_file
        dataset = pd.read_csv(csv_root, sep=separator, decimal=decimal)
        newColumns = {}
        for column in dataset.columns:
            newColumns[column] = '{}_{}'.format(column, idx)
        dataset.rename(columns=newColumns, inplace=True)
        arrayDatasets.append(_joinAngles(dataset, labels))

    joinedDataset = pd.concat(arrayDatasets, axis=1)
    _moveInitTimes(joinedDataset, name_player, playerID, labels, timeColumn)


def _joinAngles(dataset, labels):
    logging.info('Joining angles...')

    extremities = u.getExtremities(dataset, labels)
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


def _moveInitTimes(dataset, player, playerId, labels, timeColumn):
    logging.info('Calculating duration time of movements...')
    extremities = u.getExtremities(dataset, labels)
    dataset = dataset.fillna(0)
    timeIndex = []
    for limb in extremities:
        for column in limb:
            mask = dataset[column] != 0
            title = column.split('_')
            timeIndex.append({
                'timeColumn': '{}_{}'.format(timeColumn, title[1]),
                'indexMask': dataset[column][mask].index,
                'columnLimb': column
            })

    for idx, element in enumerate(timeIndex):
        firstTime = dataset[element['timeColumn']][element['indexMask'][0]]
        keyTime = '{}{}'.format(element['timeColumn'], idx)
        valueTime = (dataset[element['timeColumn']][element['indexMask']] - firstTime).tolist()

        keyExtremity = '{}{}'.format(element['columnLimb'], idx)
        valueExtremity = (dataset[element['columnLimb']][element['indexMask']]).tolist()
        dataMoveDict = {
            keyTime: valueTime,
            keyExtremity: valueExtremity
        }
        name = element['columnLimb'].replace(' ', '_')
        name = name.replace('/', '%')
        u.createFile(pd.DataFrame(dataMoveDict), os.getcwd(),
            '#PL{}#PI{}#EX{}'.format(player, playerId, name))

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
    parser.add_argument('labels',
                        help='etiquetas',
                        type=str)
    parser.add_argument('timeColumn',
                        help='etiqueta de tiempo',
                        type=str)

args = parser.parse_args()
_getFiles([args.root, args.separator, args.decimal, args.labels, args.timeColumn])
