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
    #logging.basicConfig(filename=os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + '/Logs/MySQL.log', level=logging.DEBUG, filemode='w')
    logging.basicConfig(level=logging.INFO)
    logging.info("Execution time: " + datetime.now().strftime("%Y/%m/%d %H:%M:%S"))
    api_key = __collectorFunctions.getRiotApi()
    db = 'loldata'
    daysAgo = 525
    maxGames = 100000
    database.refreshDatabase(db)
    friendinfo.CollectFriendInfo(api_key, db)
    gameids.CollectGameIds(api_key, db, daysAgo)
    gameinfo.CollectGameData(api_key, db, maxGames)
    championkill.CollectChampionKill(api_key, db, maxGames)
    preparedata.LoadFreshData('MySQL', db)
    logging.info("---Code has completed in %s seconds ---" % (time.time() - start_time))