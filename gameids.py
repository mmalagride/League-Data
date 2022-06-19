import requests
import pyodbc
import json
import time

def Connect():
    ReturnObject = dict()
    connection = pyodbc.connect('DRIVER=MySQL ODBC 8.0 ANSI Driver;''SERVER=localhost;''DATABASE=league;''UID=root;''PWD=root;''charset=utf8mb4;')
    cursor     = connection.cursor()
    ReturnObject['connection'] = connection
    ReturnObject['cursor']     = cursor
    return ReturnObject
def CollectGameIds(api_key, weeksAgo):        
    end_date = int(round(time.time()))
    unix_day  = 86400
    unix_week = (7*unix_day)
    #Change the below value to batch load since certain date
    start_date = end_date - (weeksAgo * (unix_week))
    root_url = 'https://americas.api.riotgames.com'
    DW = Connect()
    sql = "INSERT INTO gameIds Values(?)"
    #Main
    DW['cursor'].execute('SELECT summoner_puuid FROM league.friendsinfo order by summoner_puuid')
    accountids = DW['cursor'].fetchall()
    for query_end_date in range(end_date, start_date, -unix_week):
        query_start_date = query_end_date - unix_week
        if query_start_date < start_date:
            query_start_date = start_date   
        for accountid in accountids:
            time.sleep(1)
            response = requests.get('%s/lol/match/v5/matches/by-puuid/%s/ids?startTime=%s&endTime=%s&start=0&count=100&api_key=%s' % (root_url,accountid[0],str(query_start_date),str(query_end_date),api_key))
            while response.status_code != 200:
                if response.status_code == 404:
                    break
                print('Maximum API requests made, please wait...')
                time.sleep(60)
                response = requests.get('%s/lol/match/v5/matches/by-puuid/%s/ids?startTime=%s&endTime=%s&start=0&count=100&api_key=%s' % (root_url,accountid[0],str(query_start_date),str(query_end_date),api_key))
            game_list = response.json()
            for game_id in game_list:
                input = (game_id)
                try:
                    DW['cursor'].execute(sql,input)
                    DW['connection'].commit()
                    print('GameId captured: ' + str(game_id))
                except:
                    print('GameId has already been captured. Likely game was played with a friend.')
