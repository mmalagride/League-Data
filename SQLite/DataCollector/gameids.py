import requests
import pyodbc
import json
import time
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

def CollectGameIds(api_key, weeksAgo):        
    end_date = int(round(time.time()))
    unix_day  = 86400
    unix_week = (7*unix_day)
    #Change the below value to batch load since certain date
    start_date = end_date - (weeksAgo * (unix_week))
    root_url = 'https://americas.api.riotgames.com'
    DW = ConnectDB()
    sql = "INSERT INTO 'data.gameids' Values(?)"
    #Main
    DW['cursor'].execute("SELECT summoner_puuid FROM 'data.friendinfo' order by summoner_puuid")
    accountids = DW['cursor'].fetchall()
    for query_end_date in range(end_date, start_date, -unix_week):
        query_start_date = query_end_date - unix_week
        if query_start_date < start_date:
            query_start_date = start_date   
        for accountid in accountids:
            game_list = PersistentRequest('%s/lol/match/v5/matches/by-puuid/%s/ids?startTime=%s&endTime=%s&start=0&count=100&api_key=%s' % (root_url,accountid['summoner_puuid'],str(query_start_date),str(query_end_date),api_key))
            if len(game_list) < 1:
                logging.info('No games played by user: ' + str(accountid['summoner_puuid']))
            for game_id in game_list:
                try:
                    DW['cursor'].execute(sql,(game_id,))
                    DW['connection'].commit()
                    logging.info('GameId captured: ' + str(game_id))
                except:
                    logging.info('GameId has already been captured. Likely game was played with a friend.')
