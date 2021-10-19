import pandas as pd
import logging
import sys
sys.path.append('..\\utils\\')
import util as u

logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

def _getFiles(data):
    [listDataset, labels, timeColumn] = data
    logging.info('Beginning load files...')

    arrayDatasets = []
    for idx, dataset in enumerate(listDataset):
        newColumns = {}
        for column in dataset.columns:
            newColumns[column] = '{}_{}'.format(column, idx)
        dataset.rename(columns=newColumns, inplace=True)
        arrayDatasets.append(_joinAngles(dataset, labels))

    joinedDataset = pd.concat(arrayDatasets, axis=1)
    list = _moveInitTimes(joinedDataset, labels, timeColumn)
    return list


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


def _moveInitTimes(dataset, labels, timeColumn):
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
    listDataset = []
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
        listDataset.append (pd.DataFrame(dataMoveDict))

    logging.info('Temp file created!')
    return listDataset

def startExtractAverage(data):
    print('----------------- START PROCCESS-------------------------')
    [listDataset, labels, timeColumn] = data
    listTempDataset = _getFiles([
        listDataset,
        labels,
        timeColumn
    ])
    print('----------------- END PROCCESS-------------------------')
    return listTempDataset
