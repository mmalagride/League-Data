SELECT 
gi.gameId,
case when gi.gameDuration > 10000 then ROUND(gi.gameDuration/1000) else gi.gameDuration end as gameDuration,
gi.gameStartTime,
qi.queue_description as queueDescription,
gi.playerName,
gi.gameResult,
gi.teamSide,
gi.lane,
gi.role,
gi.teamPosition,
gi.indivPosition,
gi.championName,
gi.championLevel,
REPLACE(TRIM(',' FROM REPLACE(teammates.teamArray, gi.playerName, '')), ',,', ',') as teamArray,
SUBSTRING_INDEX(REPLACE(TRIM(',' FROM REPLACE(teammates.teamArray, gi.playerName, '')), ',,', ','),',',1) AS teamMate1,
case when TRIM(',' FROM REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(REPLACE(TRIM(',' FROM REPLACE(teammates.teamArray, gi.playerName, '')), ',,', ','),',',2),',',2), SUBSTRING_INDEX(REPLACE(TRIM(',' FROM REPLACE(teammates.teamArray, gi.playerName, '')), ',,', ','),',',1), ''))='' then 'Other' else TRIM(',' FROM REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(REPLACE(TRIM(',' FROM REPLACE(teammates.teamArray, gi.playerName, '')), ',,', ','),',',2),',',2), SUBSTRING_INDEX(REPLACE(TRIM(',' FROM REPLACE(teammates.teamArray, gi.playerName, '')), ',,', ','),',',1), '')) end  AS teamMate2,
case when TRIM(',' FROM REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(REPLACE(TRIM(',' FROM REPLACE(teammates.teamArray, gi.playerName, '')), ',,', ','),',',-2),',',2), SUBSTRING_INDEX(REPLACE(TRIM(',' FROM REPLACE(teammates.teamArray, gi.playerName, '')), ',,', ','),',',-1), ''))='' then 'Other' else TRIM(',' FROM REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(REPLACE(TRIM(',' FROM REPLACE(teammates.teamArray, gi.playerName, '')), ',,', ','),',',-2),',',2), SUBSTRING_INDEX(REPLACE(TRIM(',' FROM REPLACE(teammates.teamArray, gi.playerName, '')), ',,', ','),',',-1), '')) end AS teamMate3,
SUBSTRING_INDEX(REPLACE(TRIM(',' FROM REPLACE(teammates.teamArray, gi.playerName, '')), ',,', ','),',',-1)  AS teamMate4,
opponents.playerName as opponentName,
opponents.championName as opponentChampion,
si1.summonerspell_name as summoner1Id,
si2.summonerspell_name as summoner2Id,
gi.totalKills,
gi.totalDeaths,
gi.longestTimeAlive,
gi.totalTimeDead,
gi.totalAssists,
gi.largestKillingSpree,
gi.largestMultiKill,
gi.totalDoubleKills,
gi.totalTripleKills,
gi.totalQuadraKills,
gi.totalPentaKills,
gi.firstBloodAssist,
gi.firstBloodKill,
gi.totalDamageDealt,
gi.totalPhysicalDamageDealt,
gi.totalMagicDamageDealt,
gi.totalTrueDamageDealt,
gi.totalTowerDamage,
gi.totalObjectiveDamage,
gi.totalDamageTaken,
gi.totalPhysicalDamageTaken,
gi.totalMagicDamageTaken,
gi.totalTrueDamageTaken,
gi.totalDamageMitigated,
gi.totalHealing,
gi.totalAllyHealing,
gi.totalAllyShielding,
gi.totalCCDuration,
gi.visionScore,
iiV.item_name as visionItem,
gi.totalWards,
gi.stealthWardsPlaced,
gi.controlWardsPurchased,
gi.controlWardsPlaced,
gi.wardsKilled,
gi.goldEarned,
gi.goldSpent,
gi.minionKills,
gi.neutralKills,
gi.towerKills,
gi.towerTakedowns,
gi.towerLost,
gi.firstTowerKill,
gi.firstTowerAssist,
gi.inhibitorKills,
gi.inhibitorTakedowns,
gi.inhibitorLost,
gi.dragonKills,
gi.baronKills,
gi.nexusKills,
gi.nexusTakedowns,
gi.objectivesStolen,
gi.objectivesStolenAssist,
ii1.item_name as item1,
ii2.item_name as item2,
ii3.item_name as item3,
ii4.item_name as item4,
ii5.item_name as item5,
ii6.item_name as item6,
gi.itemsPurchased,
rikey.rune_name as runeKeystone,
riprim.rune_tree_name as runePrimary,
ri1.rune_name as runePrimary1,
ri2.rune_name as runePrimary2,
ri3.rune_name as runePrimary3,
risec.rune_tree_name as runeSecondary,
ris1.rune_name as runeSecondary1,
ris2.rune_name as runeSecondary2,
tb1.champion_Name as teamBan1,
tb2.champion_Name as teamBan2,
tb3.champion_Name as teamBan3,
tb4.champion_Name as teamBan4,
tb5.champion_Name as teamBan5,
eb1.champion_Name as enemyBan1,
eb2.champion_Name as enemyBan2,
eb3.champion_Name as enemyBan3,
eb4.champion_Name as enemyBan4,
eb5.champion_Name as enemyBan5,
gi.teamFirstChampionKill,
gi.teamChampionKills,
gi.enemyFirstChampionKill,
gi.enemyChampionKills,
gi.teamFirstTowerKill,
gi.teamTowerKills,
gi.enemyFirstTowerKill,
gi.enemyTowerKills,
gi.teamFirstDragonKill,
gi.teamDragonKills,
gi.enemyFirstDragonKill,
gi.enemyDragonKills,
gi.teamFirstHeraldKill,
gi.teamHeraldKills,
gi.enemyFirstHeraldKill,
gi.enemyHeraldKills,
gi.teamFirstBaronKill,
gi.teamBaronKills,
gi.enemyFirstBaronKill,
gi.enemyBaronKills,
gi.teamFirstInhibitorKill,
gi.teamInhibitorKills,
gi.enemyFirstInhibitorKill,
gi.enemyInhibitorKills,
gi.summoner1Casts,
gi.summoner2Casts,
gi.spell1Casts,
gi.spell2Casts,
gi.spell3Casts,
gi.spell4Casts,
gi.earlySurrender,
gi.lateSurrender
FROM league.gameinfo as gi
left join queueinfo qi on gi.gameMode = qi.queue_id
left join summonerspellinfo si1 on gi.summoner1id = si1.summonerspell_id
left join summonerspellinfo si2 on gi.summoner2id = si2.summonerspell_id
left join iteminfo iiV on gi.visionItem = iiV.item_id
left join iteminfo ii1 on gi.item1 = ii1.item_id
left join iteminfo ii2 on gi.item2 = ii2.item_id
left join iteminfo ii3 on gi.item3 = ii3.item_id
left join iteminfo ii4 on gi.item4 = ii4.item_id
left join iteminfo ii5 on gi.item5 = ii5.item_id
left join iteminfo ii6 on gi.item6 = ii6.item_id
left join runeinfo rikey  on gi.runeKeyStone = rikey.rune_id
left join (select distinct rune_tree_id, rune_tree_name from runeinfo) riprim on gi.runePrimary  = riprim.rune_tree_id
left join runeinfo ri1 on gi.runePrimary1 = ri1.rune_id
left join runeinfo ri2 on gi.runePrimary2 = ri2.rune_id
left join runeinfo ri3 on gi.runePrimary3 = ri3.rune_id
left join (select distinct rune_tree_id, rune_tree_name from runeinfo) risec on gi.runeSecondary  = risec.rune_tree_id
left join runeinfo ris1 on gi.runeSecondary1 = ris1.rune_id
left join runeinfo ris2 on gi.runeSecondary2 = ris2.rune_id
left join championinfo tb1 on gi.teamBan1 = tb1.champion_Id
left join championinfo tb2 on gi.teamBan2 = tb2.champion_Id
left join championinfo tb3 on gi.teamBan3 = tb3.champion_Id
left join championinfo tb4 on gi.teamBan4 = tb4.champion_Id
left join championinfo tb5 on gi.teamBan5 = tb5.champion_Id
left join championinfo eb1 on gi.enemyBan1 = eb1.champion_Id
left join championinfo eb2 on gi.enemyBan2 = eb2.champion_Id
left join championinfo eb3 on gi.enemyBan3 = eb3.champion_Id
left join championinfo eb4 on gi.enemyBan4 = eb4.champion_Id
left join championinfo eb5 on gi.enemyBan5 = eb5.champion_Id
left join gameinfo opponents on gi.gameId = opponents.gameId AND gi.teamPosition = opponents.teamPosition AND gi.teamSide != opponents.teamSide
left join (select gameId, teamSide, GROUP_CONCAT(CASE WHEN playerName not in (select distinct summoner_name from friendsinfo) then 'Other' else playerName end SEPARATOR ',') as teamArray from gameinfo group by gameId, teamSide) as teammates on gi.gameId = teammates.gameId and gi.teamSide = teammates.teamSide
where gi.playerName in (select distinct summoner_name from friendsinfo)