import argparse
import re
import pandas as pd
import logging
import os
from player import Player
from base import Base, engine, Session
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger(__name__)

def save_data(playerData, playerId): 
  Base.metadata.create_all(engine)
  session = Session()
  player = Player(playerId,
                  playerData['peso'],
                  playerData['aniosE'],
                  playerData['aI_muñeca'],
                  playerData['aF_muñeca'],
                  playerData['std_muñeca'],
                  playerData['aI_codo'],
                  playerData['aF_codo'],
                  playerData['std_codo'],
                  playerData['aI_hombro'],
                  playerData['aF_hombro'],
                  playerData['std_hombro'],
                  playerData['aI_cadera'],
                  playerData['aF_cadera'],
                  playerData['std_cadera'],
                  playerData['aI_rodilla'],
                  playerData['aF_rodilla'],
                  playerData['std_rodilla'],
                  playerData['aI_tobillo'],
                  playerData['aF_tobillo'],
                  playerData['std_tobillo'],
                  playerData['efectividad'],
                  )
  session.add(player)

  session.commit()
  session.close()

def add_data(path, fileRoot, fileName):
  root = '{}/compare/temp'.format(fileRoot)
  files = os.listdir(root)

  playerName = ''
  playerData = {}
  for file in files:
    rootFile = '{}/{}'.format(root, file)
    dataset = pd.read_csv(rootFile)
    playerName = re.search(r'#PL([a-zA-Z]*[0-9]*)', file)
    playerId = re.search(r'#PI([0-9]*)', file)
    extremity = re.search(r'#EX(\S*[0-9]*)#', file)
    playerData['aI_{}'.format(extremity.group(1).lower())] = dataset['ai'][0]
    playerData['aF_{}'.format(extremity.group(1).lower())] = dataset['af'][0]
    playerData['std_{}'.format(extremity.group(1).lower())] = dataset['std'][0]

  rootFile = '{}\\{}_{}.csv'.format(path, fileName, playerName.group(1))
  extraData = pd.read_csv(rootFile)
  playerData['aniosE'] = extraData['years'][0]
  playerData['peso'] = extraData['peso'][0]
  playerData['efectividad'] = extraData['efectividad'][0]
  
  save_data(playerData, playerId.group(1))
  
if __name__ == '__main__':
  parser = argparse.ArgumentParser()
  parser.add_argument('path',
                      help='Ruta de archivos /carpeta1/carpeta2',
                      type=str)
  parser.add_argument('root',
                      help='Ruta de archivos /carpeta1/carpeta2',
                      type=str)
  parser.add_argument('fileName',
                      help='',
                      type=str)
  args = parser.parse_args()
  add_data(args.path, args.root, args.fileName)
