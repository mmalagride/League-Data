import os
import json
import logging
import requests
import pyodbc
import time
import sqlite3

def getRiotApi():
    keyPath =  os.path.dirname(os.path.dirname(os.path.dirname(__file__))) + "\\Secrets\\riot-api-key.json"
    key = open(keyPath, 'r')
    content = json.loads(key.read())
    return content['api_key']

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def ConnectDB():
    logging.info("Establishing Connection to SQL DB...")
    ReturnObject = dict()
    connection = sqlite3.connect(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "\\db.db")
    connection.row_factory = dict_factory
    cursor     = connection.cursor()
    ReturnObject['connection'] = connection
    ReturnObject['cursor']     = cursor
    logging.info("Connection Successful!")
    return ReturnObject

def PersistentRequest(endpoint):
    while True:
        try:
            logging.info("Requesting information from Riot API...") 
            response = requests.get(endpoint,headers={"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"},timeout=2)
            if response.status_code not in (429, 404):
                break
            else:
                logging.warning('Maximum API requests made, please wait 90 seconds')
                for i in range(90):
                    time.sleep(1)
                    if i % 15 == 0:
                        logging.warning('Time elapsed: %s' % str(i))
                logging.warning('Resuming Data collection...')
        except:
            logging.warning('Server is taking a long time to respond...')
    game_info = response.json()
    return game_info