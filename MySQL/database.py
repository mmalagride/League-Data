import logging
import pyodbc
import os
import requests
import json
import mysql.connector

def ConnectDB(database):    
    ReturnObject = dict()
    while True:
        try:
            connection = pyodbc.connect('DRIVER=MySQL ODBC 8.0 ANSI Driver;''SERVER=localhost;''DATABASE=%s;''UID=root;''PWD=root;''charset=utf8mb4;' % database)
            logging.info("Establishing Connection to SQL DB...")
            cursor     = connection.cursor()
            ReturnObject['connection'] = connection
            ReturnObject['cursor']     = cursor
            logging.info("Connection Successful!")
            break
        except:
            logging.info("Database of name '%s' not found! Creating new one under that name..." % database)
            connection = mysql.connector.connect(host="localhost",user="root",password="root")
            cursor     = connection.cursor()
            cursor.execute("CREATE DATABASE %s" % database)
            logging.info("New Database Creation Successful!")
    return ReturnObject

def initDB(DW):
    logging.info("Creating Fact Tables...")
    for query in os.listdir(os.path.dirname(__file__) + "\\ReferenceTables"):
        if query.endswith('.sql'):
            sqlPath = os.path.join(os.path.dirname(__file__) + "\\ReferenceTables", query)
            sql = open(sqlPath, 'r')
            SQLfile = sql.read()
            try:
                DW['cursor'].execute(SQLfile)
            except:
                DW['cursor'].execute("DROP TABLE %s" % (query[:query.find(".")]))
                DW['cursor'].execute(SQLfile)
    logging.info("Fact Tables created!")

    logging.info("Creating Data Table structures...")
    for query in os.listdir(os.path.dirname(__file__) + "\\DataTables"):
            sqlPath = os.path.join(os.path.dirname(__file__) + "\\DataTables", query)
            sql = open(sqlPath, 'r')
            SQLfile = sql.read()
            try:
                DW['cursor'].execute(SQLfile)
            except:
                pass
    logging.info("Data Tables created!")

    logging.info("Creating Views...")
    for query in os.listdir(os.path.dirname(__file__) + "\\Views"):
            sqlPath = os.path.join(os.path.dirname(__file__) + "\\Views", query)
            sql = open(sqlPath, 'r')
            SQLfile = sql.read()
            try:
                DW['cursor'].execute(SQLfile)
            except:
                DW['cursor'].execute("DROP VIEW %s" % query[:query.find(".")])
                DW['cursor'].execute(SQLfile)
    logging.info("Views created!")

def populateDB(DW):
    logging.info("Populating Fact Tables with reference keys...")
    version = getLatestVersion()
    getChampionFacts(version,DW)
    getItemFacts(version,DW)
    getQueueFacts(DW)
    getRuneFacts(version,DW)
    getSummonderSpellFacts(version,DW)
    logging.info("Reference Tables ready.")

def getLatestVersion():
    endpoint = "https://ddragon.leagueoflegends.com/api/versions.json"
    endpointInfo = requests.get(endpoint).json()
    logging.info('Now Loading Data Tables to patch %s' % endpointInfo[0])
    return endpointInfo[0]

def getChampionFacts(version,DW):
    endpoint = "http://ddragon.leagueoflegends.com/cdn/%s/data/en_US/champion.json" % version
    endpointInfo = requests.get(endpoint).json()
    for key, value in endpointInfo['data'].items():
        champion_key = int(value['key'])
        champion_name = value['name']
        champion_tags = ','.join(value['tags'])
        champion_image = value['image']['full']
        input = (champion_key,champion_name,champion_tags,champion_image)
        DW['cursor'].execute("INSERT INTO championinfo VALUES (?,?,?,?)", input)
        DW['connection'].commit()
    logging.info('Champion Facts updated!')

def getItemFacts(version,DW):
    endpoint = "http://ddragon.leagueoflegends.com/cdn/%s/data/en_US/item.json" % version
    endpointInfo = requests.get(endpoint).json()
    for key in endpointInfo['data']:
        item_key = key        
        item_name = endpointInfo['data'][key]['name']
        if '<' in item_name:
            pass
        else:
            if 'into' in endpointInfo['data'][key].keys():
                item_into = ','.join(endpointInfo['data'][key]['into'])
            else:
                item_into = None
            if 'from' in endpointInfo['data'][key].keys():
                item_from = ','.join(endpointInfo['data'][key]['from'])
            else:
                item_from = None
            item_cost = endpointInfo['data'][key]['gold']['total']
            item_tags = ','.join(endpointInfo['data'][key]['tags'])
            item_image = endpointInfo['data'][key]['image']['full']
            input = (item_key,item_name,item_into,item_from,item_cost,item_tags,item_image)
            DW['cursor'].execute("INSERT INTO iteminfo VALUES (?,?,?,?,?,?,?)",input)
            DW['connection'].commit()     
    logging.info('Item Facts updated!')  

def getQueueFacts(DW):
    endpoint = "http://static.developer.riotgames.com/docs/lol/queues.json"
    endpointInfo = requests.get(endpoint).json()   
    for value in endpointInfo:
        if not value['description']:
            pass #Bad/Deprecated Queue type
        elif not value['notes']:
            queue_id = value['queueId']
            queue_map = value['map']
            queue_description = value['description']
            input = (queue_id,queue_map,queue_description)
            DW['cursor'].execute("INSERT INTO queueinfo Values(?,?,?)", input)
            DW['connection'].commit()
    logging.info('Queue Facts updated!')

def getRuneFacts(version,DW):
    endpoint = "http://ddragon.leagueoflegends.com/cdn/%s/data/en_US/runesReforged.json" % version
    endpointInfo = requests.get(endpoint).json()
    for tree in endpointInfo:
        rune_tree_id = tree['id']
        rune_tree_name = tree['name']
        rune_tree_icon = tree['icon']
        for tier in tree['slots']:
            for rune in tier['runes']:
                rune_id = rune['id']
                rune_name = rune['name']
                rune_icon = rune['icon']
                input = (rune_id,rune_name,rune_icon,rune_tree_id,rune_tree_name,rune_tree_icon)
                DW['cursor'].execute("INSERT INTO runeinfo Values(?,?,?,?,?,?)",input)
                DW['connection'].commit()
    logging.info('Rune Facts updated!')

def getSummonderSpellFacts(version,DW):
    endpoint = "http://ddragon.leagueoflegends.com/cdn/%s/data/en_US/summoner.json" % version
    endpointInfo = requests.get(endpoint).json()  
    for value in  endpointInfo['data']:
        summonerspell_key = endpointInfo['data'][value]['key']
        summonerspell_name = endpointInfo['data'][value]['name']
        summonerspell_icon = endpointInfo['data'][value]['image']['full']
        input = (summonerspell_key,summonerspell_name,summonerspell_icon)
        DW['cursor'].execute("INSERT INTO summonerspellinfo Values(?,?,?)",input)
        DW['connection'].commit()
    logging.info('SummonerSpell Facts updated!')

def refreshDatabase(database):
    logging.basicConfig(level=logging.INFO)
    DW = ConnectDB(database)
    initDB(DW)
    populateDB(DW)
