from DataCollector import friendinfo
from DataCollector import gameids
from DataCollector import gameinfo
from DataCollector import preparedata
from DataCollector import championkill
from DataCollector import __collectorFunctions
from datetime import datetime
import database
import os
import json
import logging
import time

if __name__ == "__main__":
    start_time = time.time()
    logging.basicConfig(filename=os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/Logs/SQLite.log', level=logging.DEBUG, filemode='w')
    logging.info("Execution time: " + datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    api_key = __collectorFunctions.getRiotApi()
    daysAgo = 1
    maxGames = 50
    database.refreshDatabase()
    friendinfo.CollectFriendInfo(api_key)
    gameids.CollectGameIds(api_key, daysAgo)
    gameinfo.CollectGameData(api_key, maxGames)
    championkill.CollectChampionKill(api_key, maxGames)
    preparedata.LoadFreshData('SQLite')
    logging.info("---Code has completed in %s seconds ---" % (time.time() - start_time))