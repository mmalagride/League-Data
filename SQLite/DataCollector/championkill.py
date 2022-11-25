import requests
import pyodbc
import json
import time
import unidecode
import logging
import sqlite3
import os
import sys

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

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def CollectChampionKill(api_key, games):
    DW = ConnectDB()
    sql = "INSERT INTO 'data.championkill' Values(?,?,?,?,?,?,?,?,?,?,?,?)"
    root_url = 'https://americas.api.riotgames.com'
    DW['cursor'].execute("SELECT distinct gameid FROM 'fullgamedetails' order by gameid desc limit %s;" % games)
    gameids = DW['cursor'].fetchall()
    for gameid in gameids:
        while True:
            try:
                logging.info('Requesting Game Event Info list from Riot API...')
                response = requests.get('%s/lol/match/v5/matches/%s/timeline?api_key=%s' % (root_url,gameid['gameId'],api_key))
                if response.status_code not in (429, 404):
                    break
                else:
                    logging.warning('Maximum API requests made, please wait...')
                    time.sleep(60) 
            except:
                logging.warning('Maximum API requests made, please wait...')
                time.sleep(60)
        game_info = response.json()
        participants = {}
        for player in game_info['info']['participants']:
            participants[player['participantId']] = player['puuid']
        for frame in game_info['info']['frames']:
            for event in frame['events']:
                if event['type'] == 'CHAMPION_KILL':
                    event_gameid = gameid['gameId']
                    event_type = event['type']
                    event_timestamp = event['timestamp']
                    if event['killerId'] == 0:
                        event_killerid = event['victimDamageReceived'][0]['type']
                    else:
                        event_killerid = participants[event['killerId']]
                    event_victimid = participants[event['victimId']]
                    if 'assistingParticipantIds' in event.keys():
                        event_assist1 = participants[event['assistingParticipantIds'][0]] if (len(event['assistingParticipantIds']) >= 1) else None
                        event_assist2 = participants[event['assistingParticipantIds'][1]] if (len(event['assistingParticipantIds']) >= 2) else None
                        event_assist3 = participants[event['assistingParticipantIds'][2]] if (len(event['assistingParticipantIds']) >= 3) else None
                        event_assist4 = participants[event['assistingParticipantIds'][3]] if (len(event['assistingParticipantIds']) >= 4) else None
                    else:
                        event_assist1 = None
                        event_assist2 = None
                        event_assist3 = None
                        event_assist4 = None
                    event_posx = event['position']['x']
                    event_posy = event['position']['y']
                    listofDamage = []
                    for types in event['victimDamageReceived']:
                        if types['participantId'] == event['killerId']:
                            listofDamage.append(types)
                    event_killedby = '' if (listofDamage == []) else listofDamage[-1]['spellName']
                    input = (event_gameid,event_type,event_timestamp,event_killerid,event_victimid,event_assist1,event_assist2,event_assist3,event_assist4,event_killedby,event_posx,event_posy)
                    try:
                        DW['cursor'].execute(sql,input)
                        DW['connection'].commit()
                    except sqlite3.IntegrityError as err:
                        logging.info(err.args[0].split(':')[0] +" event information likely captured.")
        logging.info('Game Event Info list captured!')