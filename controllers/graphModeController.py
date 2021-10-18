import io
import re
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D
import logging
from handle_response import successResponse, errorResponse
from util import createImage
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

colors = ['r', 'g', 'b', 'c', 'm', 'y', 'k', (0.62, 0.42, 0.75), (0.21, 0.24, 0.57), (0.99, 0.20, 0.55), (0.02, 0.23, 0.55)]

def _getFiles(data):
    [listDataset, header, metric, unit, playerName, documentNumber] = data
    print('---------------START GRAPH MODE------------------')
    logger.info('Reading files...')

    labels = []
    for idx, dataset in enumerate(listDataset):
        labels.append((colors[idx], '{}_{}'.format(playerName, idx)))
        for column in dataset.columns:
            if re.search(header.lower(), column.lower()):
                plt.plot(dataset[column], color=colors[idx])

    plt.xlabel('Tiempo (%)')
    plt.ylabel('{} {} ({})'.format(metric, header, unit))

    # Avoid repeated labels in chart
    plt.legend([Line2D([0], [0], color=clave[0], lw=2) for clave in labels],
           [clave[1] for clave in labels])
    root = '{}/Individuales/{}_{}'.format(documentNumber, metric, playerName)
    buf = io.BytesIO()
    plt.savefig(buf, format= 'png')
    createImage(root, buf.getvalue())
    buf.close()
    print('---------------END GRAPH MODE------------------')


def startGraphMode(data):
    [listDataset, header, metric, unity, playerName, documentNumber] = data
    metricName = 'Movimiento Angular' if metric == '1' else 'Velocidad Lineal' if metric == '2' else 'Velocidad Angular'
    _getFiles([
        listDataset,
        header,
        metricName,
        unity,
        playerName,
        documentNumber
    ])
    return successResponse(True, 'Grafico creado exitosamente')
