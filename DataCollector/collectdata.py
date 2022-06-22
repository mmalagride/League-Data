import friendinfo
import gameids
import gameinfo
import preparedata
import os
import json

def getRiotApi():
    keyPath = os.path.dirname(os.path.dirname(__file__)) + "\\Secrets\\riot-api-key.json"
    key = open(keyPath, 'r')
    content = json.loads(key.read())
    return content['api_key']

if __name__ == "__main__":
        logging.basicConfig(level=logging.INFO)
        api_key = getRiotApi()
        weeksAgo = 1
        maxGames = 100
        friendinfo.CollectFriendInfo(api_key)
        gameids.CollectGameIds(api_key, weeksAgo)
        gameinfo.CollectGameData(api_key, maxGames)
        preparedata.LoadFreshData('Data Import')