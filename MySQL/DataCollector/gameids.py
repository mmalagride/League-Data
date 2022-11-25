import requests
import pyodbc
import json
import time
import logging
import os

def ConnectDB(db):
    logging.info("Establishing Connection to SQL DB...")
    ReturnObject = dict()
    connection = pyodbc.connect('DRIVER=MySQL ODBC 8.0 ANSI Driver;''SERVER=localhost;''DATABASE=%s;''UID=root;''PWD=root;''charset=utf8mb4;' % db)
    cursor     = connection.cursor()
    ReturnObject['connection'] = connection
    ReturnObject['cursor']     = cursor
    logging.info("Connection Successful!")
    return ReturnObject

def CollectGameIds(api_key, db, weeksAgo):        
    end_date = int(round(time.time()))
    unix_day  = 86400
    unix_week = (7*unix_day)
    start_date = end_date - (weeksAgo * (unix_week))
    root_url = 'https://americas.api.riotgames.com'
    DW = ConnectDB(db)
    sql = "INSERT INTO gameids Values(?)"
    #Main
    DW['cursor'].execute('SELECT summoner_puuid FROM friendinfo order by summoner_puuid')
    accountids = DW['cursor'].fetchall()
    for query_end_date in range(end_date, start_date, -unix_week):
        query_start_date = query_end_date - unix_week
        if query_start_date < start_date:
            query_start_date = start_date   
        for accountid in accountids:
            while True:
                try:
                    logging.info('Requesting GameIDs list from Riot API...')
                    response = requests.get('%s/lol/match/v5/matches/by-puuid/%s/ids?startTime=%s&endTime=%s&start=0&count=100&api_key=%s' % (root_url,accountid[0],str(query_start_date),str(query_end_date),api_key))
                    if response.status_code not in (429, 404):
                        break
                    else:
                        logging.warning('Maximum API requests made, please wait...')
                        time.sleep(60)                        
                except:
                    logging.warning('Maximum API requests made, please wait...')
                    time.sleep(60)
            game_list = response.json()
            if len(game_list) < 1:
                logging.info('No games played by user: ' + str(accountid[0]))
            for game_id in game_list:
                try:
                    DW['cursor'].execute(sql,(game_id,))
                    DW['connection'].commit()
                    logging.info('GameId captured: ' + str(game_id))
                except:
                    logging.info('GameId already captured: '  + str(game_id) +'. Likely game was played with a friend.')
