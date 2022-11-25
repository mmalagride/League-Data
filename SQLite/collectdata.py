from DataCollector import friendinfo
from DataCollector import gameids
from DataCollector import gameinfo
from DataCollector import preparedata
from DataCollector import championkill
import database
import os
import json
import logging

def getRiotApi():
    keyPath = os.path.dirname(os.path.dirname(__file__)) + "\\Secrets\\riot-api-key.json"
    key = open(keyPath, 'r')
    content = json.loads(key.read())
    return content['api_key']

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    api_key = getRiotApi()
    weeksAgo = 1
    maxGames = 1000000
    database.refreshDatabase()
    friendinfo.CollectFriendInfo(api_key)
    gameids.CollectGameIds(api_key, weeksAgo)
    gameinfo.CollectGameData(api_key, maxGames)
    championkill.CollectChampionKill(api_key, maxGames)
    preparedata.LoadFreshData('SQLite')