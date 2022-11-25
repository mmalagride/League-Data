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

def ConnectDB(db):
    logging.info("Establishing Connection to SQL DB...")
    ReturnObject = dict()
    connection = pyodbc.connect('DRIVER=MySQL ODBC 8.0 ANSI Driver;''SERVER=localhost;''DATABASE=%s;''UID=root;''PWD=root;''charset=utf8mb4;' % db)
    cursor     = connection.cursor()
    ReturnObject['connection'] = connection
    ReturnObject['cursor']     = cursor
    logging.info("Connection Successful!")
    return ReturnObject

def LoadFreshData(sheetname, db):
    logging.info("Loading Game data into Googlesheets...")
    DW = ConnectDB(db)
    gc = pygsheets.authorize(service_file=os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) + "\\Secrets\\google-api-key.json")
    dataframe1 = pd.read_sql('SELECT * FROM fullgamedetails', con=DW['connection'])
    sh = gc.open(sheetname)
    wks1 = sh[0]
    wks1.clear()
    wks1.set_dataframe(dataframe1,(1,1))

    dataframe2 = pd.read_sql('SELECT * FROM killdetails', con=DW['connection'])
    wks2 = sh[1]
    wks2.clear()
    wks2.set_dataframe(dataframe2,(1,1))
    
    logging.info("Load complete! Dashboard is now up-to-date!")


