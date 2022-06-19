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
queue_raw = "http://static.developer.riotgames.com/docs/lol/queues.json"
sql = "INSERT INTO gamemode Values(?,?,?)"
#Main
queue_info = requests.get(queue_raw).json()
for value in queue_info:
    if not value['description']:
        print('Insufficient Data for Queue Type')
    elif not value['notes']:
        queue_id = value['queueId']
        queue_map = value['map']
        queue_description = value['description']
        input = (queue_id,queue_map,queue_description)
        try:
            DW['cursor'].execute(sql,input)
            DW['connection'].commit()  
        except:
            print('Primary Key for Queue Already Exists')  
    elif 'Deprecated' in value['notes'] or 'deprecated' in value['notes']:
        print('Queue type has been deprecated')


