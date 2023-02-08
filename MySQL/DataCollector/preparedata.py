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
    logging.info("Loading data for complete datset...")
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
    logging.info("Load complete!")
    logging.info("Loading data for 3 month subset...")
    logging.info("Executing fullgamedetails query...")
    dataframe1 = pd.read_sql('SELECT * FROM fullgamedetails where gameStartTime > ((unix_timestamp() * 1000) - 7776000000);', con=DW['connection'])
    sh3 = gc.open(sheetname + " - 3 Months")
    wks1 = sh3[0]
    wks1.clear()
    wks1.set_dataframe(dataframe1,(1,1))
    logging.info("Executing killdetails query...")
    dataframe2 = pd.read_sql('select distinct kd.* from killdetails kd left join fullgamedetails fgd on kd.gameID = fgd.gameID where fgd.gameStartTime > ((unix_timestamp() * 1000) - 7776000000);', con=DW['connection'])
    wks2 = sh3[1]
    wks2.clear()
    wks2.set_dataframe(dataframe2,(1,1))   
    logging.info("Load complete! Dashboard is now up-to-date!")


