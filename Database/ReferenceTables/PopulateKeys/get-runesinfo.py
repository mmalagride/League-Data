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
runes_raw = "http://ddragon.leagueoflegends.com/cdn/12.5.1/data/en_US/runesReforged.json"
sql = "INSERT INTO runeinfo Values(?,?,?,?,?,?)"
#Main
runes_info = requests.get(runes_raw).json()
for tree in runes_info:
    rune_tree_id = tree['id']
    rune_tree_name = tree['name']
    rune_tree_icon = tree['icon']
    for tier in tree['slots']:
        for rune in tier['runes']:
            rune_id = rune['id']
            rune_name = rune['name']
            rune_icon = rune['icon']
            input = (rune_id,rune_name,rune_icon,rune_tree_id,rune_tree_name,rune_tree_icon)
            try:
                DW['cursor'].execute(sql,input)
                DW['connection'].commit() 
            except:        
                print('Primary Key: ' +str(rune_id)+ ' for Rune Already Exists') 



