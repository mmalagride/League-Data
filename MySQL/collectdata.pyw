from DataCollector import friendinfo
from DataCollector import gameids
from DataCollector import gameinfo
from DataCollector import preparedata
from DataCollector import championkill
from DataCollector import __collectorFunctions
import database
import os
import json
import logging
import time

def getRiotApi():
    keyPath = os.path.dirname(os.path.dirname(__file__)) + "\\Secrets\\riot-api-key.json"
    key = open(keyPath, 'r')
    content = json.loads(key.read())
    return content['api_key']

if __name__ == "__main__":
    start_time = time.time()
    logging.basicConfig(filename=os.path.dirname(sys.argv[0])+os.sep+'mylog.log', level=logging.DEBUG)
    logging.basicConfig(level=logging.INFO)
    api_key = __collectorFunctions.getRiotApi()
    db = 'loldata'
    daysAgo = 1
    maxGames = 100
    database.refreshDatabase(db)
    friendinfo.CollectFriendInfo(api_key, db)
    gameids.CollectGameIds(api_key, db, daysAgo)
    gameinfo.CollectGameData(api_key, db, maxGames)
    championkill.CollectChampionKill(api_key, db, maxGames)
    preparedata.LoadFreshData('MySQL', db)
    logging.info("---Code has completed in %s seconds ---" % (time.time() - start_time))