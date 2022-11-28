from DataCollector import __collectorFunctions
import logging
import os
import unidecode

def CollectFriendInfo(api_key,db):
    #Data from LoL API, request Docs here: https://developer.riotgames.com/apis#summoner-v4/GET_getBySummonerName  
    DW = __collectorFunctions.ConnectDB(db)
    root_url = 'https://na1.api.riotgames.com'
    sql = "INSERT INTO friendinfo Values(?,?,?,?,?,?)"
    sql_update = "UPDATE friendinfo SET summoner_accountid=?,summoner_level=?,summoner_image=?,summoner_puuid=?,summoner_lastupdate=? WHERE summoner_name=?"    #Main
    file = open(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) + "\\Secrets\\summoners.txt", "r")
    summoners = [line.strip() for line in file.readlines()]
    for summoner in summoners:
        summoner_info = __collectorFunctions.PersistentRequest('%s/lol/summoner/v4/summoners/by-name/%s?api_key=%s' % (root_url,summoner,api_key))
        summoner_key = summoner_info['accountId']
        summoner_name = summoner_info['name']
        summoner_level = summoner_info['summonerLevel']
        #PNG for image can be found here: http://ddragon.leagueoflegends.com/cdn/10.19.1/img/profileicon/588.png <- summoner_image   
        summoner_image = str(summoner_info['profileIconId']) + '.png'
        summoner_puuid = summoner_info['puuid']
        summoner_lastupdate = summoner_info['revisionDate'] #Unix epoch miliseconds
        input = (summoner_key,summoner_name,summoner_level,summoner_image,summoner_puuid,summoner_lastupdate)
        try:        
            DW['cursor'].execute(sql,input)
            DW['connection'].commit()
            logging.info('New Summoner info added for: ' + summoner_name)
        except:        
            updater = (summoner_key,summoner_level,summoner_image,summoner_puuid,summoner_lastupdate,summoner_name)
            DW['cursor'].execute(sql_update,updater)
            DW['connection'].commit()
            logging.info('Updated Summoner info added for: ' + summoner_name)

