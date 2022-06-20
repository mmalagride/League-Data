import requests
import pyodbc
import json
import logging
import sqlite3
import os

def ConnectDB():
        logging.info("Establishing Connection to SQL DB...")
        ReturnObject = dict()
        connection = sqlite3.connect(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "\\Database\\db.db")
        connection.row_factory = dict_factory
        cursor     = connection.cursor()
        ReturnObject['connection'] = connection
        ReturnObject['cursor']     = cursor
        logging.info("Connection Successful!")
        return ReturnObject

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
    file = open(os.path.dirname(os.path.dirname(os.path.realpath(__file__))) + "\\Secrets\\summoners.txt", "r")
    summoners = [line.strip() for line in file.readlines()]
    for summoner in summoners:
        summoner_info = requests.get('%s/lol/summoner/v4/summoners/by-name/%s?api_key=%s' % (root_url,summoner,api_key)).json()
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
            print('New Summoner info added for: ' + summoner_name)
        except:        
            updater = (summoner_key,summoner_level,summoner_image,summoner_puuid,summoner_lastupdate,summoner_name)
            DW['cursor'].execute(sql_update,updater)
            DW['connection'].commit()
            print('Updated Summoner info added for: ' + summoner_name)

