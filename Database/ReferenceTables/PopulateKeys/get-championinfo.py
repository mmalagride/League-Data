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
champion_raw = "http://ddragon.leagueoflegends.com/cdn/12.5.1/data/en_US/champion.json"
sql = "INSERT INTO championinfo Values(?,?,?,?)"
#Main
champion_info = requests.get(champion_raw).json()
for key, value in champion_info['data'].items():
    champion_key = int(value['key'])
    champion_name = value['name']
    champion_tags = ','.join(value['tags'])
    #PNG for image can be found here: http://ddragon.leagueoflegends.com/cdn/10.19.1/img/champion/Ashe.png <- champion_image
    champion_image = value['image']['full']
    input = (champion_key,champion_name,champion_tags,champion_image)
    try:
        DW['cursor'].execute(sql,input)
        DW['connection'].commit()  
    except:
        print('Primary Key for Champion Already Exists')  
