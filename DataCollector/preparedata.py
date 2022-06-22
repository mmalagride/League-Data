import requests
import pyodbc
import json
import time
import unidecode
import pygsheets
import pandas as pd
import logging
import sqlite3
import os

def ConnectDB():
        logging.info("Establishing Connection to SQL DB...")
        ReturnObject = dict()
        connection = sqlite3.connect(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "\\Database\\db.db")
        connection.row_factory = dict_factory
        cursor     = connection.cursor()
        ReturnObject['connection'] = connection
        ReturnObject['cursor']     = cursor
        logging.info("Connection Successful!")
        return ReturnObject

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def LoadFreshData(sheetname):
    logging.info("Loading Game data into Googlesheets...")
    DW = ConnectDB()
    gc = pygsheets.authorize(service_file=os.path.dirname(os.path.dirname(__file__)) + "\\Secrets\\google-api-key.json")
    dataframe1 = pd.read_sql('SELECT * FROM fullgamedetails', con=DW['connection'])
    sh = gc.open(sheetname)
    wks1 = sh[0]
    wks1.set_dataframe(dataframe1,(1,1))

    dataframe2 = pd.read_sql('SELECT * FROM KillDetails', con=DW['connection'])
    wks2 = sh[1]
    wks2.set_dataframe(dataframe2,(1,1))
    
    logging.info("Load complete! Dashboard is now up-to-date!")


