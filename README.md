### League-Data

Data collection scripts for collecting information on list of players through the Riot API.  
As well as database setup to initialize a MySQL storage solution, or SQLite storage.  

A MySQL DB can be installed here: https://dev.mysql.com/downloads/installer/  
However for beginners I recommend just going with the SQLite configuration as its easier to get started.  

A fresh Riot API will be required to run most of the scripts found here: https://developer.riotgames.com/  
This will need to be updated daily, as it times-out after 24hours. Once the new key is generated save the file here: /Secrets/riot-api-key.json  
- (Key-Value pair of "api-key": "GENERATED_KEY")  

Before utilizing the google end of the project the following steps must be followed:  
- 1. Create a Project here: https://console.cloud.google.com/  
- 2. Next the following API's need to be enabled:  
    +     +  Google Drive: https://console.cloud.google.com/apis/api/drive.googleapis.com/  
    +     +  Google Sheets: https://console.cloud.google.com/marketplace/product/google/sheets.googleapis.com/  
- 3. Service Account must be created: https://console.cloud.google.com/apis/credentials  
    +     +  a. + Create Credentials -> Service Account -> Fill in whatever name/details  
    +     +  b. Service Account -> Edit Service Account -> Keys -> Add Key -> Create New -> Save as JSON  
    +     +  c. Save this as /Secrets/google-api-key.json  
- 4. Create the relevant workbooks in google sheets/google drive: https://docs.google.com/spreadsheets/  
    +     +  (Ensure each workbook has ample row counts for large data sets -> around 100,000+ should be sufficient)  
- 5. Share each workbook to the service account as an editor (email found in google-api-key)  

All data to be visualized in google DataStudio/LookerStudio, with the current final product at: https://datastudio.google.com/  

Next create a list of playernames that you'd like to collect data on then save this as /Secrets/summoners.txt  
- (Write the file in the format:  Name1   ) (New-line seperated)  
    +     +     +     +     +     +     +     +     + Name2  
    +     +     +     +     +     +     +     +     + Name3  

Finally the begin running the data collection scripts run either of the "collectdata.py" in the database folder of choice.  