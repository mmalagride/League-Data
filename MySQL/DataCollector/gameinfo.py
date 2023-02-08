from DataCollector import __collectorFunctions
import logging
import os
import unidecode
import time
     
def CollectGameData(api_key, db, games):
    DW = __collectorFunctions.ConnectDB(db)
    root_url = 'https://americas.api.riotgames.com'
    sql_insert = "INSERT INTO gameinfo Values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)"
    DW['cursor'].execute("SELECT gameid FROM gameids order by gameid desc limit %s;" % games)
    gameids = DW['cursor'].fetchall()
    if gameids[0][0] == 'status':
        gameids.pop(0)
    for gameid in gameids:
        thing = '%s/lol/match/v5/matches/%s?api_key=%s' % (root_url,gameid[0],api_key)
        game_info = __collectorFunctions.PersistentRequest('%s/lol/match/v5/matches/%s?api_key=%s' % (root_url,gameid[0],api_key))
        gameId = game_info['metadata']['matchId']
        gameDuration = game_info['info']['gameDuration']
        gameStartTime = game_info['info']['gameStartTimestamp']
        gameMode = game_info['info']['queueId']
        if game_info['info']['queueId'] in [700,440,420,400]:
            logging.info('Inserting data for Game: ' + str(gameId))
            #End of Game Personal Stats
            for i in range(10):
                #Personal Information
                logging.info('Loading Personal Game information for player: %s' % game_info['info']['participants'][i]['summonerName'])
                playerName = unidecode.unidecode(game_info['info']['participants'][i]['summonerName'])
                playerId = game_info['info']['participants'][i]['summonerId']
                gameResult = game_info['info']['participants'][i]['win']
                teamId = game_info['info']['participants'][i]['teamId']
                teamSide = 'BLUE' if game_info['info']['participants'][i]['teamId'] == 100 else 'RED' 
                #Role Related Information
                teamPosition = game_info['info']['participants'][i]['teamPosition']
                individualPosition = game_info['info']['participants'][i]['individualPosition']
                lane = game_info['info']['participants'][i]['lane'] #Combined with the below field
                role = game_info['info']['participants'][i]['role'] #To help determine bot lane roles
                championId = game_info['info']['participants'][i]['championId']
                championName = game_info['info']['participants'][i]['championName']
                championLevel = game_info['info']['participants'][i]['champLevel']
                summoner1Id = game_info['info']['participants'][i]['summoner1Id']
                summoner2Id = game_info['info']['participants'][i]['summoner2Id']
                #Kill/Death/Assist Stats
                totalKills = game_info['info']['participants'][i]['kills']
                totalDeaths = game_info['info']['participants'][i]['deaths']
                longestTimeAlive = game_info['info']['participants'][i]['longestTimeSpentLiving']
                totalTimeDead = game_info['info']['participants'][i]['totalTimeSpentDead']
                totalAssists = game_info['info']['participants'][i]['assists']
                #MultiKills and First Blood
                largestKillingSpree = game_info['info']['participants'][i]['largestKillingSpree']
                largestMultiKill = game_info['info']['participants'][i]['largestMultiKill']
                totalDoubleKills = game_info['info']['participants'][i]['doubleKills']
                totalTripleKills = game_info['info']['participants'][i]['tripleKills']
                totalQuadraKills = game_info['info']['participants'][i]['quadraKills']
                totalPentaKills = game_info['info']['participants'][i]['pentaKills']
                firstBloodAssist = game_info['info']['participants'][i]['firstBloodAssist']
                firstBloodKill = game_info['info']['participants'][i]['firstBloodKill']
                #Damge Dealt
                totalDamageDealt = game_info['info']['participants'][i]['totalDamageDealtToChampions']
                totalPhysicalDamageDealt = game_info['info']['participants'][i]['physicalDamageDealtToChampions']
                totalMagicDamageDealt = game_info['info']['participants'][i]['magicDamageDealtToChampions']
                totalTrueDamageDealt = game_info['info']['participants'][i]['trueDamageDealtToChampions']
                totalTowerDamage = game_info['info']['participants'][i]['damageDealtToTurrets']
                totalObjectiveDamage = game_info['info']['participants'][i]['damageDealtToObjectives']
                #Damage Taken
                totalDamageTaken = game_info['info']['participants'][i]['totalDamageTaken']
                totalPhysicalDamageTaken = game_info['info']['participants'][i]['physicalDamageTaken']
                totalMagicDamageTaken = game_info['info']['participants'][i]['magicDamageTaken']
                totalTrueDamageTaken = game_info['info']['participants'][i]['trueDamageTaken']
                #Damage Mitigated and CC Related
                totalDamageMitigated = game_info['info']['participants'][i]['damageSelfMitigated']
                totalHealing = game_info['info']['participants'][i]['totalHeal']
                totalAllyHealing = game_info['info']['participants'][i]['totalHealsOnTeammates']
                totalAllyShielding = game_info['info']['participants'][i]['totalDamageShieldedOnTeammates']
                totalCCDuration = game_info['info']['participants'][i]['timeCCingOthers']
                #Vision Related and Wards
                visionScore = game_info['info']['participants'][i]['visionScore']
                visionItem = game_info['info']['participants'][i]['item6']
                totalWards = game_info['info']['participants'][i]['wardsPlaced']
                stealthWardsPlaced = totalWards - game_info['info']['participants'][i]['detectorWardsPlaced']
                controlWardsBought = game_info['info']['participants'][i]['visionWardsBoughtInGame']
                controlWardsPlaced = game_info['info']['participants'][i]['detectorWardsPlaced']
                wardsKilled = game_info['info']['participants'][i]['wardsKilled']
                #Gold Related and Minion/Jungle Kills
                goldEarned = game_info['info']['participants'][i]['goldEarned']
                goldSpent = game_info['info']['participants'][i]['goldSpent']
                minionKills = game_info['info']['participants'][i]['totalMinionsKilled']
                neutralKills = game_info['info']['participants'][i]['neutralMinionsKilled']
                #Tower and Building Objective Related
                towerKills = game_info['info']['participants'][i]['turretKills']
                towerTakedowns = game_info['info']['participants'][i]['turretTakedowns']
                towerLost = game_info['info']['participants'][i]['turretsLost']
                firstTowerKill = game_info['info']['participants'][i]['firstTowerKill']
                firstTowerAssist = game_info['info']['participants'][i]['firstTowerAssist']
                inhibitorKills = game_info['info']['participants'][i]['inhibitorKills']
                inhibitorTakedowns = game_info['info']['participants'][i]['inhibitorTakedowns']
                inhibitorLost = game_info['info']['participants'][i]['inhibitorsLost']
                dragonKills = game_info['info']['participants'][i]['dragonKills']
                baronKills = game_info['info']['participants'][i]['baronKills']
                nexusKills = game_info['info']['participants'][i]['nexusKills']
                nexusTakedowns = game_info['info']['participants'][i]['nexusTakedowns']
                objectivesStolen = game_info['info']['participants'][i]['objectivesStolen']
                objectivesStolenAssists = game_info['info']['participants'][i]['objectivesStolenAssists']
                #Item Information
                item0 = game_info['info']['participants'][i]['item0']
                item1 = game_info['info']['participants'][i]['item1']
                item2 = game_info['info']['participants'][i]['item2']
                item3 = game_info['info']['participants'][i]['item3']
                item4 = game_info['info']['participants'][i]['item4']
                item5 = game_info['info']['participants'][i]['item5']
                itemsPurchased = game_info['info']['participants'][i]['itemsPurchased']
                #Rune Information
                runeKeyStone = game_info['info']['participants'][i]['perks']['styles'][0]['selections'][0]['perk']
                runePrimary = game_info['info']['participants'][i]['perks']['styles'][0]['style']
                runePrimary1 = game_info['info']['participants'][i]['perks']['styles'][0]['selections'][1]['perk']
                runePrimary2 = game_info['info']['participants'][i]['perks']['styles'][0]['selections'][2]['perk']
                runePrimary3 = game_info['info']['participants'][i]['perks']['styles'][0]['selections'][3]['perk']
                runeSecondary = game_info['info']['participants'][i]['perks']['styles'][1]['style']
                runeSecondary1 = game_info['info']['participants'][i]['perks']['styles'][1]['selections'][0]['perk']
                runeSecondary2 = game_info['info']['participants'][i]['perks']['styles'][1]['selections'][1]['perk']
                statPerkDefence = game_info['info']['participants'][i]['perks']['statPerks']['defense']
                statPerkFlex = game_info['info']['participants'][i]['perks']['statPerks']['flex']
                statPerkOffence = game_info['info']['participants'][i]['perks']['statPerks']['offense']        
                #Team Information
                teamIndex = 0 if teamId == 100 else 1
                teamBan1 = game_info['info']['teams'][teamIndex]['bans'][0]['championId']
                teamBan2 = game_info['info']['teams'][teamIndex]['bans'][1]['championId']
                teamBan3 = game_info['info']['teams'][teamIndex]['bans'][2]['championId']
                teamBan4 = game_info['info']['teams'][teamIndex]['bans'][3]['championId']
                teamBan5 = game_info['info']['teams'][teamIndex]['bans'][4]['championId']
                enemyBan1 = game_info['info']['teams'][teamIndex-1]['bans'][0]['championId']
                enemyBan2 = game_info['info']['teams'][teamIndex-1]['bans'][1]['championId']
                enemyBan3 = game_info['info']['teams'][teamIndex-1]['bans'][2]['championId']
                enemyBan4 = game_info['info']['teams'][teamIndex-1]['bans'][3]['championId']
                enemyBan5 = game_info['info']['teams'][teamIndex-1]['bans'][4]['championId']
                teamChampionKills = game_info['info']['teams'][teamIndex]['objectives']['champion']['kills']
                teamFirstChampionKill = game_info['info']['teams'][teamIndex]['objectives']['champion']['first']
                enemyChampionKills = game_info['info']['teams'][teamIndex-1]['objectives']['champion']['kills']
                enemyFirstChampionKill = game_info['info']['teams'][teamIndex-1]['objectives']['champion']['first']
                teamTowerKills = game_info['info']['teams'][teamIndex]['objectives']['tower']['kills']
                teamFirstTowerKill = game_info['info']['teams'][teamIndex]['objectives']['tower']['first']
                enemyTowerKills = game_info['info']['teams'][teamIndex-1]['objectives']['tower']['kills']
                enemyFirstTowerKill = game_info['info']['teams'][teamIndex-1]['objectives']['tower']['first']
                teamDragonKills = game_info['info']['teams'][teamIndex]['objectives']['dragon']['kills']
                teamFirstDragonKill = game_info['info']['teams'][teamIndex]['objectives']['dragon']['first']
                enemyDragonKills = game_info['info']['teams'][teamIndex-1]['objectives']['dragon']['kills']
                enemyFirstDragonKill = game_info['info']['teams'][teamIndex-1]['objectives']['dragon']['first']
                teamHeraldKills = game_info['info']['teams'][teamIndex]['objectives']['riftHerald']['kills']
                teamFirstHeraldKill = game_info['info']['teams'][teamIndex]['objectives']['riftHerald']['first']
                enemyHeraldKills = game_info['info']['teams'][teamIndex-1]['objectives']['riftHerald']['kills']
                enemyFirstHeraldKill = game_info['info']['teams'][teamIndex-1]['objectives']['riftHerald']['first']
                teamBaronKills = game_info['info']['teams'][teamIndex]['objectives']['baron']['kills']
                teamFirstBaronKill = game_info['info']['teams'][teamIndex]['objectives']['baron']['first']
                enemyBaronKills = game_info['info']['teams'][teamIndex-1]['objectives']['baron']['kills']
                enemyFirstBaronKill = game_info['info']['teams'][teamIndex-1]['objectives']['baron']['first']
                teamInhibitorKills = game_info['info']['teams'][teamIndex]['objectives']['inhibitor']['kills']
                teamFirstInhibitorKill = game_info['info']['teams'][teamIndex]['objectives']['inhibitor']['first']
                enemyInhibitorKills = game_info['info']['teams'][teamIndex-1]['objectives']['inhibitor']['kills']
                enemyFirstInhibitorKill = game_info['info']['teams'][teamIndex-1]['objectives']['inhibitor']['first']
                #Spell Cast Metrics
                summoner1Casts = game_info['info']['participants'][i]['summoner1Casts']
                summoner2Casts = game_info['info']['participants'][i]['summoner2Casts']
                spell1Casts = game_info['info']['participants'][i]['spell1Casts']
                spell2Casts = game_info['info']['participants'][i]['spell2Casts']
                spell3Casts = game_info['info']['participants'][i]['spell3Casts']
                spell4Casts = game_info['info']['participants'][i]['spell4Casts']
                #Surrender Results
                earlySurrender = game_info['info']['participants'][i]['gameEndedInEarlySurrender']
                lateSurrender = game_info['info']['participants'][i]['gameEndedInSurrender']

                input = (gameId,gameDuration,gameStartTime,gameMode,playerName,playerId,gameResult,teamId,teamSide,teamPosition,individualPosition,lane,role,championId,championName,championLevel,summoner1Id,summoner2Id,totalKills,totalDeaths,longestTimeAlive,
                totalTimeDead,totalAssists,largestKillingSpree,largestMultiKill,totalDoubleKills,totalTripleKills,totalQuadraKills,totalPentaKills,firstBloodAssist,firstBloodKill,totalDamageDealt,totalPhysicalDamageDealt,totalMagicDamageDealt,
                totalTrueDamageDealt,totalTowerDamage,totalObjectiveDamage,totalDamageTaken,totalPhysicalDamageTaken,totalMagicDamageTaken,totalTrueDamageTaken,totalDamageMitigated,totalHealing,totalAllyHealing,totalAllyShielding,totalCCDuration,
                visionScore,visionItem,totalWards,stealthWardsPlaced,controlWardsBought,controlWardsPlaced,wardsKilled,goldEarned,goldSpent,minionKills,neutralKills,towerKills,towerTakedowns,towerLost,firstTowerKill,firstTowerAssist,inhibitorKills,
                inhibitorTakedowns,inhibitorLost,dragonKills,baronKills,nexusKills,nexusTakedowns,objectivesStolen,objectivesStolenAssists,item0,item1,item2,item3,item4,item5,itemsPurchased,runeKeyStone,runePrimary,runePrimary1,runePrimary2,runePrimary3,
                runeSecondary,runeSecondary1,runeSecondary2,statPerkDefence,statPerkFlex,statPerkOffence,teamBan1,teamBan2,teamBan3,teamBan4,teamBan5,enemyBan1,enemyBan2,enemyBan3,enemyBan4,enemyBan5,teamChampionKills,teamFirstChampionKill,enemyChampionKills,
                enemyFirstChampionKill,teamTowerKills,teamFirstTowerKill,enemyTowerKills,enemyFirstTowerKill,teamDragonKills,teamFirstDragonKill,enemyDragonKills,enemyFirstDragonKill,teamHeraldKills,teamFirstHeraldKill,enemyHeraldKills,enemyFirstHeraldKill,
                teamBaronKills,teamFirstBaronKill,enemyBaronKills,enemyFirstBaronKill,teamInhibitorKills,teamFirstInhibitorKill,enemyInhibitorKills,enemyFirstInhibitorKill,summoner1Casts,summoner2Casts,spell1Casts,spell2Casts,spell3Casts,spell4Casts,earlySurrender,lateSurrender)
                try:
                    DW['cursor'].execute(sql_insert,input)
                    DW['connection'].commit()
                except:
                    logging.info('Game information already captured for player!')
        else:
            logging.info("Game type not of interest! Aborting data collection for game.") 
