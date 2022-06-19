import requests
import pyodbc
import json
import time
import unidecode
import pygsheets
import pandas as pd

def Connect():
    ReturnObject = dict()
    connection = pyodbc.connect('DRIVER=MySQL ODBC 8.0 ANSI Driver;''SERVER=localhost;''DATABASE=league;''UID=root;''PWD=root;''charset=utf8mb4;')
    cursor     = connection.cursor()
    ReturnObject['connection'] = connection
    ReturnObject['cursor']     = cursor
    return ReturnObject
def LoadFreshData(sheetname):
    print("Loading Game data into Googlesheets...")
    DW = Connect()
    gc = pygsheets.authorize(service_file='lgb-kpi-94ff2e9b67d4.json')
    dataframe = pd.read_sql('SELECT * FROM league.fullgamedetails', con=DW['connection'])
    sh = gc.open(sheetname)
    wks = sh[0]
    wks.set_dataframe(dataframe,(1,1))
    print("Load complete! Dashboard is now up-to-date!")

