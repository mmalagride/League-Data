import logging
import sqlite3
import os
import requests
import json

def dict_factory(cursor, row):
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d

def ConnectDB():
        logging.info("Establishing Connection to SQL DB...")
        ReturnObject = dict()
        connection = sqlite3.connect(os.path.dirname(os.path.realpath(__file__)) + "\\db.db")
        connection.row_factory = dict_factory
        cursor     = connection.cursor()
        ReturnObject['connection'] = connection
        ReturnObject['cursor']     = cursor
        logging.info("Connection Successful!")
        return ReturnObject

def initDB():
    logging.info("Creating Fact Tables...")
    for query in os.listdir(os.path.dirname(__file__) + "\\ReferenceTables"):
        if query.endswith('.sql'):
            sqlPath = os.path.join(os.path.dirname(__file__) + "\\ReferenceTables", query)
            sql = open(sqlPath, 'r')
            SQLfile = sql.read()
            try:
                DW['cursor'].execute(SQLfile)
            except:
                DW['cursor'].execute("DROP TABLE '%s'" % ("fact." + query[:query.find(".")]))
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
                DW['cursor'].execute("DROP TABLE '%s'" % ("data." + query[:query.find(".")]))
                DW['cursor'].execute(SQLfile)
    logging.info("Data Tables created!")

    logging.info("Creating Views...")
    for query in os.listdir(os.path.dirname(__file__) + "\\Views"):
            sqlPath = os.path.join(os.path.dirname(__file__) + "\\Views", query)
            sql = open(sqlPath, 'r')
            SQLfile = sql.read()
            try:
                DW['cursor'].execute(SQLfile)
            except:
                DW['cursor'].execute("DROP VIEW 'fullgamedetails'")
                DW['cursor'].execute(SQLfile)
    logging.info("Views created!")

def populateDB():
    logging.info("Populating Fact Tables with reference keys...")
    version = getLatestVersion()
    getChampionFacts(version)
    getItemFacts(version)
    getQueueFacts()
    getRuneFacts(version)
    getSummonderSpellFacts(version)
    logging.info("Reference Tables ready.")

def getLatestVersion():
    endpoint = "https://ddragon.leagueoflegends.com/api/versions.json"
    endpointInfo = requests.get(endpoint).json()
    return endpointInfo[0]

def getChampionFacts(version):
    endpoint = "http://ddragon.leagueoflegends.com/cdn/%s/data/en_US/champion.json" % version
    endpointInfo = requests.get(endpoint).json()
    for key, value in endpointInfo['data'].items():
        champion_key = int(value['key'])
        champion_name = value['name']
        champion_tags = ','.join(value['tags'])
        champion_image = value['image']['full']
        input = (champion_key,champion_name,champion_tags,champion_image)
        DW['cursor'].execute("INSERT INTO 'fact.championinfo' VALUES (?,?,?,?)", input)
        DW['connection'].commit()
    logging.info('Champion Facts updated!')

def getItemFacts(version):
    endpoint = "http://ddragon.leagueoflegends.com/cdn/%s/data/en_US/item.json" % version
    endpointInfo = requests.get(endpoint).json()
    for key in endpointInfo['data']:
        item_key = key
        item_name = endpointInfo['data'][key]['name']
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
        DW['cursor'].execute("INSERT INTO 'fact.iteminfo' VALUES (?,?,?,?,?,?,?)",input)
        DW['connection'].commit()     
    logging.info('Item Facts updated!')  

def getQueueFacts():
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
            DW['cursor'].execute("INSERT INTO 'fact.queueinfo' Values(?,?,?)", input)
            DW['connection'].commit()
    logging.info('Queue Facts updated!')

def getRuneFacts(version):
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
                DW['cursor'].execute("INSERT INTO 'fact.runeinfo' Values(?,?,?,?,?,?)",input)
                DW['connection'].commit()
    logging.info('Rune Facts updated!')

def getSummonderSpellFacts(version):
    endpoint = "http://ddragon.leagueoflegends.com/cdn/%s/data/en_US/summoner.json" % version
    endpointInfo = requests.get(endpoint).json()  
    for value in  endpointInfo['data']:
        summonerspell_key = endpointInfo['data'][value]['key']
        summonerspell_name = endpointInfo['data'][value]['name']
        summonerspell_icon = endpointInfo['data'][value]['image']['full']
        input = (summonerspell_key,summonerspell_name,summonerspell_icon)
        DW['cursor'].execute("INSERT INTO 'fact.summonerspellinfo' Values(?,?,?)",input)
        DW['connection'].commit()
    logging.info('SummonerSpell Facts updated!')

if __name__ == "__main__":
        logging.basicConfig(level=logging.INFO)
        DW = ConnectDB()
        initDB()
        populateDB()
