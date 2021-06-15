import os
import re
import argparse
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import logging
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k', (0.62, 0.42, 0.75), (0.21, 0.24, 0.57), (0.99, 0.20, 0.55), (0.02, 0.23, 0.55)]

def _getFiles(data):
    [path, header, metric, unit, output] = data
    logger.info('Reading files...')
    files = os.listdir(path)
    labels = []
    for idx, file in enumerate(files):
        name = re.search(r'_([a-zA-Z]*[0-9]*).', file)
        isFile = os.path.isfile(os.path.join(path, file))
        isCsv = file.endswith(".csv")
        if  isFile and isCsv:
            csv_root = path + '\\' + file
            dataset = pd.read_csv(csv_root, sep=",", decimal=".")
            labels.append((colors[idx], name.group(1)))
            for column in dataset.columns:
                if re.search(header, column):
                    plt.plot(dataset[column], color=colors[idx])

    # plt.axhline(0, 0, linestyle= '--', color= (0.69, 0.69, 0.69)  , label='pyplot horizontal line')
    plt.xlabel('Tiempo (%)')
    plt.ylabel('{} {} ({})'.format(metric, header, unit))
    plt.legend([Line2D([0], [0], color=clave[0], lw=2) for clave in labels],
           [clave[1] for clave in labels])
    os.makedirs('{}/Individuales/{}/'.format(output, name.group(1)), exist_ok=True)
    plt.savefig('{}/Individuales/{}/Grafica_{}_{}.png'.format(output,  name.group(1),header, name.group(1)))

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('path',
                        type=str)
    parser.add_argument('header',
                        type=str)
    parser.add_argument('metric',
                        type=str)
    parser.add_argument('unit',
                        type=str)
    parser.add_argument('output',
                        type=str)

args = parser.parse_args()
data = [args.path, args.header, args.metric, args.unit, args.output]
_getFiles(data)
