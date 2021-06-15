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