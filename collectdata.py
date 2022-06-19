import friendinfo
import gameids
import gameinfo
import preparedata

# To run script and collect new data, obtain a new API Key from the riot API portal
# As well as configure the time interval you'd like to crawl for data for, and max number of games to scan

api_key = 'RGAPI-4d4bf600-7424-4080-a5be-93649eb9754b'
weeksAgo = 2
maxGames = 100
friendinfo.CollectFriendInfo(api_key)
gameids.CollectGameIds(api_key, weeksAgo)
gameinfo.CollectGameData(api_key, maxGames)
preparedata.LoadFreshData('TheBoys 2022')