import requests
import pyodbc
import json
import logging
import sqlite3
import os

def ConnectDB():
    logging.info("Establishing Connection to SQL DB...")
    ReturnObject = dict()  
    connection = sqlite3.connect(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "\\db.db")
    connection.row_factory = dict_factory
    cursor     = connection.cursor()
    ReturnObject['connection'] = connection
    ReturnObject['cursor']     = cursor
    logging.info("Connection Successful!")
    return ReturnObject

def PersistentRequest(endpoint):
    while True:
        try:
            logging.info("Requesting information from Riot API...") 
            response = requests.get(endpoint,headers={"User-Agent": "Mozilla/5.0 (X11; CrOS x86_64 12871.102.0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.141 Safari/537.36"},timeout=2)
            if response.status_code not in (429, 404):
                break
            else:
                logging.warning('Maximum API requests made, please wait...')
                time.sleep(90)
        except:
            logging.warning('Server is taking a long time to respond...')
    game_info = response.json()
    return game_info

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def CollectFriendInfo(api_key):
    #Data from LoL API, request Docs here: https://developer.riotgames.com/apis#summoner-v4/GET_getBySummonerName  
    DW = ConnectDB()    
    root_url = 'https://na1.api.riotgames.com'
    sql = "INSERT INTO 'data.friendinfo' Values(?,?,?,?,?,?)"
    sql_update = "UPDATE 'data.friendinfo' SET summoner_accountid=?,summoner_level=?,summoner_image=?,summoner_puuid=?,summoner_lastupdate=? WHERE summoner_name=?"
    #Main
    file = open(os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__)))) + "\\Secrets\\summoners.txt", "r")
    summoners = [line.strip() for line in file.readlines()]
    for summoner in summoners:
        logging.info('Requesting PlayerInfo from Riot API...')
        summoner_info = PersistentRequest('%s/lol/summoner/v4/summoners/by-name/%s?api_key=%s' % (root_url,summoner,api_key))
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

