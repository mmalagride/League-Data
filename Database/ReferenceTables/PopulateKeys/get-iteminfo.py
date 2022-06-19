import requests
import pyodbc
import json

def Connect():
    ReturnObject = dict()
    connection = pyodbc.connect('DRIVER=MySQL ODBC 8.0 ANSI Driver;''SERVER=localhost;''DATABASE=league;''UID=root;''PWD=root;''charset=utf8mb4;')
    cursor     = connection.cursor()
    ReturnObject['connection'] = connection
    ReturnObject['cursor']     = cursor
    return ReturnObject

#Data from Data Dragon, API request Docs here: https://developer.riotgames.com/docs/lol#data-dragon_champions
DW = Connect()
item_raw = "http://ddragon.leagueoflegends.com/cdn/12.5.1/data/en_US/item.json"
sql = "INSERT INTO iteminfo Values(?,?,?,?,?,?,?)"
#Main
item_info = requests.get(item_raw).json()
for key in item_info['data']:
    item_key = key
    item_name = item_info['data'][key]['name']
    if 'into' in item_info['data'][key].keys():
        item_into = ','.join(item_info['data'][key]['into'])
    else:
        item_into = None
    if 'from' in item_info['data'][key].keys():
        item_from = ','.join(item_info['data'][key]['from'])
    else:
        item_from = None
    item_cost = item_info['data'][key]['gold']['total']
    item_tags = ','.join(item_info['data'][key]['tags'])
    item_image = item_info['data'][key]['image']['full']
    input = (item_key,item_name,item_into,item_from,item_cost,item_tags,item_image)
    try:
        DW['cursor'].execute(sql,input)
        DW['connection'].commit()  
    except:
        print("Primary Key: %s for Item Already Exists" % item_key)    




