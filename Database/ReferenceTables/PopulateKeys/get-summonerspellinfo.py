import requests
import pyodbc
import json

def Connect():
    ReturnObject = dict()
    connection = pyodbc.connect('DRIVER=MySQL ODBC 8.0 ANSI Driver;''SERVER=localhost;''DATABASE=info;''UID=root;''PWD=root;''charset=utf8mb4;')
    cursor     = connection.cursor()
    ReturnObject['connection'] = connection
    ReturnObject['cursor']     = cursor
    return ReturnObject

#Data from Data Dragon, API request Docs here: https://developer.riotgames.com/docs/lol#data-dragon_champions
DW = Connect()
summonerspell_raw = "http://ddragon.leagueoflegends.com/cdn/11.8.1/data/en_US/summoner.json"
sql = "INSERT INTO summonerspells Values(?,?,?)"
#Main
summonerspell_info = requests.get(summonerspell_raw).json()
for value in summonerspell_info['data']:
    summonerspell_key = summonerspell_info['data'][value]['key']
    summonerspell_name = summonerspell_info['data'][value]['name']
    summonerspell_icon = summonerspell_info['data'][value]['image']['full']
    input = (summonerspell_key,summonerspell_name,summonerspell_icon)
    try:
        DW['cursor'].execute(sql,input)
        DW['connection'].commit() 
    except:        
        print('Primary Key: ' +str(summonerspell_key)+ ' for Item Already Exists') 



