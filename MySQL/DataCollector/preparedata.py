from DataCollector import __collectorFunctions
import logging
import os
import unidecode
import time
import pygsheets
import pandas as pd

def LoadFreshData(sheetname, db):
    logging.info("Loading Game data into Googlesheets...")
    DW = __collectorFunctions.ConnectDB(db)
    gc = pygsheets.authorize(service_file=os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) + "\\Secrets\\google-api-key.json")
    logging.info("Executing fullgamedetails query...")
    dataframe1 = pd.read_sql('SELECT * FROM fullgamedetails', con=DW['connection'])
    sh = gc.open(sheetname)
    wks1 = sh[0]
    wks1.clear()
    wks1.set_dataframe(dataframe1,(1,1))
    logging.info("Executing killdetails query...")
    dataframe2 = pd.read_sql('SELECT * FROM killdetails', con=DW['connection'])
    wks2 = sh[1]
    wks2.clear()
    wks2.set_dataframe(dataframe2,(1,1))    
    logging.info("Load complete! Dashboard is now up-to-date!")


