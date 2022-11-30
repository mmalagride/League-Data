from DataCollector import __collectorFunctions
import logging
import os
import unidecode
import time
import sqlite3

def CollectGameIds(api_key, daysAgo):        
    end_date = int(round(time.time()))
    unix_day  = 86400
    start_date = end_date - (daysAgo * (unix_day))
    root_url = 'https://americas.api.riotgames.com'
    DW = __collectorFunctions.ConnectDB()
    sql = "INSERT INTO 'data.gameids' Values(?)"
    #Main
    DW['cursor'].execute("SELECT summoner_puuid FROM 'data.friendinfo' order by summoner_puuid")
    accountids = DW['cursor'].fetchall()
    for query_end_date in range(end_date, start_date, -unix_day):
        query_start_date = query_end_date - unix_day
        if query_start_date < start_date:
            query_start_date = start_date   
        for accountid in accountids:
            game_list = __collectorFunctions.PersistentRequest('%s/lol/match/v5/matches/by-puuid/%s/ids?startTime=%s&endTime=%s&start=0&count=100&api_key=%s' % (root_url,accountid['summoner_puuid'],str(query_start_date),str(query_end_date),api_key))
            if len(game_list) < 1:
                logging.info('No games played by user: ' + str(accountid['summoner_puuid']))
            for game_id in game_list:
                try:
                    DW['cursor'].execute(sql,(game_id,))
                    DW['connection'].commit()
                    logging.info('GameId captured: ' + str(game_id))
                except:
                    logging.info('GameId has already been captured. Likely game was played with a friend.')
