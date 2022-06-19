import friendinfo
import gameids
import gameinfo
import preparedata
api_key = 'RGAPI-4d4bf600-7424-4080-a5be-93649eb9754b'
weeksAgo = 2
friendinfo.CollectFriendInfo(api_key)
gameids.CollectGameIds(api_key, weeksAgo)
gameinfo.CollectGameData(api_key, 100)
preparedata.LoadFreshData('TheBoys 2022')