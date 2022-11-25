CREATE
VIEW `fullgamedetails` AS
    SELECT 
        `gi`.`gameId` AS `gameId`,
        (CASE
            WHEN (`gi`.`gameDuration` > 10000) THEN ROUND((`gi`.`gameDuration` / 1000), 0)
            ELSE `gi`.`gameDuration`
        END) AS `gameDuration`,
        `gi`.`gameStartTime` AS `gameStartTime`,
        `qi`.`queue_description` AS `queueDescription`,
        `gi`.`playerName` AS `playerName`,
        `gi`.`gameResult` AS `gameResult`,
        `gi`.`teamSide` AS `teamSide`,
        `gi`.`lane` AS `lane`,
        `gi`.`role` AS `role`,
        `gi`.`teamPosition` AS `teamPosition`,
        `gi`.`indivPosition` AS `indivPosition`,
        `gi`.`championName` AS `championName`,
        `gi`.`championLevel` AS `championLevel`,
        REPLACE(TRIM(',' FROM REPLACE(`teammates`.`teamArray`,
                    `gi`.`playerName`,
                    '')),
            ',,',
            ',') AS `teamArray`,
        SUBSTRING_INDEX(REPLACE(TRIM(',' FROM REPLACE(`teammates`.`teamArray`,
                            `gi`.`playerName`,
                            '')),
                    ',,',
                    ','),
                ',',
                1) AS `teamMate1`,
        (CASE
            WHEN
                (TRIM(',' FROM REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(REPLACE(TRIM(',' FROM REPLACE(`teammates`.`teamArray`,
                                                    `gi`.`playerName`,
                                                    '')),
                                            ',,',
                                            ','),
                                        ',',
                                        2),
                                ',',
                                2),
                        SUBSTRING_INDEX(REPLACE(TRIM(',' FROM REPLACE(`teammates`.`teamArray`,
                                            `gi`.`playerName`,
                                            '')),
                                    ',,',
                                    ','),
                                ',',
                                1),
                        '')) = '')
            THEN
                'Other'
            ELSE TRIM(',' FROM REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(REPLACE(TRIM(',' FROM REPLACE(`teammates`.`teamArray`,
                                                `gi`.`playerName`,
                                                '')),
                                        ',,',
                                        ','),
                                    ',',
                                    2),
                            ',',
                            2),
                    SUBSTRING_INDEX(REPLACE(TRIM(',' FROM REPLACE(`teammates`.`teamArray`,
                                        `gi`.`playerName`,
                                        '')),
                                ',,',
                                ','),
                            ',',
                            1),
                    ''))
        END) AS `teamMate2`,
        (CASE
            WHEN
                (TRIM(',' FROM REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(REPLACE(TRIM(',' FROM REPLACE(`teammates`.`teamArray`,
                                                    `gi`.`playerName`,
                                                    '')),
                                            ',,',
                                            ','),
                                        ',',
                                        -(2)),
                                ',',
                                2),
                        SUBSTRING_INDEX(REPLACE(TRIM(',' FROM REPLACE(`teammates`.`teamArray`,
                                            `gi`.`playerName`,
                                            '')),
                                    ',,',
                                    ','),
                                ',',
                                -(1)),
                        '')) = '')
            THEN
                'Other'
            ELSE TRIM(',' FROM REPLACE(SUBSTRING_INDEX(SUBSTRING_INDEX(REPLACE(TRIM(',' FROM REPLACE(`teammates`.`teamArray`,
                                                `gi`.`playerName`,
                                                '')),
                                        ',,',
                                        ','),
                                    ',',
                                    -(2)),
                            ',',
                            2),
                    SUBSTRING_INDEX(REPLACE(TRIM(',' FROM REPLACE(`teammates`.`teamArray`,
                                        `gi`.`playerName`,
                                        '')),
                                ',,',
                                ','),
                            ',',
                            -(1)),
                    ''))
        END) AS `teamMate3`,
        SUBSTRING_INDEX(REPLACE(TRIM(',' FROM REPLACE(`teammates`.`teamArray`,
                            `gi`.`playerName`,
                            '')),
                    ',,',
                    ','),
                ',',
                -(1)) AS `teamMate4`,
        `opponents`.`playerName` AS `opponentName`,
        `opponents`.`championName` AS `opponentChampion`,
        `si1`.`summonerspell_name` AS `summoner1Id`,
        `si2`.`summonerspell_name` AS `summoner2Id`,
        `gi`.`totalKills` AS `totalKills`,
        `gi`.`totalDeaths` AS `totalDeaths`,
        `gi`.`longestTimeAlive` AS `longestTimeAlive`,
        `gi`.`totalTimeDead` AS `totalTimeDead`,
        `gi`.`totalAssists` AS `totalAssists`,
        `gi`.`largestKillingSpree` AS `largestKillingSpree`,
        `gi`.`largestMultiKill` AS `largestMultiKill`,
        `gi`.`totalDoubleKills` AS `totalDoubleKills`,
        `gi`.`totalTripleKills` AS `totalTripleKills`,
        `gi`.`totalQuadraKills` AS `totalQuadraKills`,
        `gi`.`totalPentaKills` AS `totalPentaKills`,
        `gi`.`firstBloodAssist` AS `firstBloodAssist`,
        `gi`.`firstBloodKill` AS `firstBloodKill`,
        `gi`.`totalDamageDealt` AS `totalDamageDealt`,
        `gi`.`totalPhysicalDamageDealt` AS `totalPhysicalDamageDealt`,
        `gi`.`totalMagicDamageDealt` AS `totalMagicDamageDealt`,
        `gi`.`totalTrueDamageDealt` AS `totalTrueDamageDealt`,
        `gi`.`totalTowerDamage` AS `totalTowerDamage`,
        `gi`.`totalObjectiveDamage` AS `totalObjectiveDamage`,
        `gi`.`totalDamageTaken` AS `totalDamageTaken`,
        `gi`.`totalPhysicalDamageTaken` AS `totalPhysicalDamageTaken`,
        `gi`.`totalMagicDamageTaken` AS `totalMagicDamageTaken`,
        `gi`.`totalTrueDamageTaken` AS `totalTrueDamageTaken`,
        `gi`.`totalDamageMitigated` AS `totalDamageMitigated`,
        `gi`.`totalHealing` AS `totalHealing`,
        `gi`.`totalAllyHealing` AS `totalAllyHealing`,
        `gi`.`totalAllyShielding` AS `totalAllyShielding`,
        `gi`.`totalCCDuration` AS `totalCCDuration`,
        `gi`.`visionScore` AS `visionScore`,
        `iiv`.`item_name` AS `visionItem`,
        `gi`.`totalWards` AS `totalWards`,
        `gi`.`stealthWardsPlaced` AS `stealthWardsPlaced`,
        `gi`.`controlWardsPurchased` AS `controlWardsPurchased`,
        `gi`.`controlWardsPlaced` AS `controlWardsPlaced`,
        `gi`.`wardsKilled` AS `wardsKilled`,
        `gi`.`goldEarned` AS `goldEarned`,
        `gi`.`goldSpent` AS `goldSpent`,
        `gi`.`minionKills` AS `minionKills`,
        `gi`.`neutralKills` AS `neutralKills`,
        `gi`.`towerKills` AS `towerKills`,
        `gi`.`towerTakedowns` AS `towerTakedowns`,
        `gi`.`towerLost` AS `towerLost`,
        `gi`.`firstTowerKill` AS `firstTowerKill`,
        `gi`.`firstTowerAssist` AS `firstTowerAssist`,
        `gi`.`inhibitorKills` AS `inhibitorKills`,
        `gi`.`inhibitorTakedowns` AS `inhibitorTakedowns`,
        `gi`.`inhibitorLost` AS `inhibitorLost`,
        `gi`.`dragonKills` AS `dragonKills`,
        `gi`.`baronKills` AS `baronKills`,
        `gi`.`nexusKills` AS `nexusKills`,
        `gi`.`nexusTakedowns` AS `nexusTakedowns`,
        `gi`.`objectivesStolen` AS `objectivesStolen`,
        `gi`.`objectivesStolenAssist` AS `objectivesStolenAssist`,
        `ii1`.`item_name` AS `item1`,
        `ii2`.`item_name` AS `item2`,
        `ii3`.`item_name` AS `item3`,
        `ii4`.`item_name` AS `item4`,
        `ii5`.`item_name` AS `item5`,
        `ii6`.`item_name` AS `item6`,
        `gi`.`itemsPurchased` AS `itemsPurchased`,
        `rikey`.`rune_name` AS `runeKeystone`,
        `riprim`.`rune_tree_name` AS `runePrimary`,
        `ri1`.`rune_name` AS `runePrimary1`,
        `ri2`.`rune_name` AS `runePrimary2`,
        `ri3`.`rune_name` AS `runePrimary3`,
        `risec`.`rune_tree_name` AS `runeSecondary`,
        `ris1`.`rune_name` AS `runeSecondary1`,
        `ris2`.`rune_name` AS `runeSecondary2`,
        `tb1`.`champion_name` AS `teamBan1`,
        `tb2`.`champion_name` AS `teamBan2`,
        `tb3`.`champion_name` AS `teamBan3`,
        `tb4`.`champion_name` AS `teamBan4`,
        `tb5`.`champion_name` AS `teamBan5`,
        `eb1`.`champion_name` AS `enemyBan1`,
        `eb2`.`champion_name` AS `enemyBan2`,
        `eb3`.`champion_name` AS `enemyBan3`,
        `eb4`.`champion_name` AS `enemyBan4`,
        `eb5`.`champion_name` AS `enemyBan5`,
        `gi`.`teamFirstChampionKill` AS `teamFirstChampionKill`,
        `gi`.`teamChampionKills` AS `teamChampionKills`,
        `gi`.`enemyFirstChampionKill` AS `enemyFirstChampionKill`,
        `gi`.`enemyChampionKills` AS `enemyChampionKills`,
        `gi`.`teamFirstTowerKill` AS `teamFirstTowerKill`,
        `gi`.`teamTowerKills` AS `teamTowerKills`,
        `gi`.`enemyFirstTowerKill` AS `enemyFirstTowerKill`,
        `gi`.`enemyTowerKills` AS `enemyTowerKills`,
        `gi`.`teamFirstDragonKill` AS `teamFirstDragonKill`,
        `gi`.`teamDragonKills` AS `teamDragonKills`,
        `gi`.`enemyFirstDragonKill` AS `enemyFirstDragonKill`,
        `gi`.`enemyDragonKills` AS `enemyDragonKills`,
        `gi`.`teamFirstHeraldKill` AS `teamFirstHeraldKill`,
        `gi`.`teamHeraldKills` AS `teamHeraldKills`,
        `gi`.`enemyFirstHeraldKill` AS `enemyFirstHeraldKill`,
        `gi`.`enemyHeraldKills` AS `enemyHeraldKills`,
        `gi`.`teamFirstBaronKill` AS `teamFirstBaronKill`,
        `gi`.`teamBaronKills` AS `teamBaronKills`,
        `gi`.`enemyFirstBaronKill` AS `enemyFirstBaronKill`,
        `gi`.`enemyBaronKills` AS `enemyBaronKills`,
        `gi`.`teamFirstInhibitorKill` AS `teamFirstInhibitorKill`,
        `gi`.`teamInhibitorKills` AS `teamInhibitorKills`,
        `gi`.`enemyFirstInhibitorKill` AS `enemyFirstInhibitorKill`,
        `gi`.`enemyInhibitorKills` AS `enemyInhibitorKills`,
        `gi`.`summoner1Casts` AS `summoner1Casts`,
        `gi`.`summoner2Casts` AS `summoner2Casts`,
        `gi`.`spell1Casts` AS `spell1Casts`,
        `gi`.`spell2Casts` AS `spell2Casts`,
        `gi`.`spell3Casts` AS `spell3Casts`,
        `gi`.`spell4Casts` AS `spell4Casts`,
        `gi`.`earlySurrender` AS `earlySurrender`,
        `gi`.`lateSurrender` AS `lateSurrender`
    FROM
        ((((((((((((((((((((((((((((((`gameinfo` `gi`
        LEFT JOIN `queueinfo` `qi` ON ((`gi`.`gameMode` = `qi`.`queue_id`)))
        LEFT JOIN `summonerspellinfo` `si1` ON ((`gi`.`summoner1Id` = `si1`.`summonerspell_id`)))
        LEFT JOIN `summonerspellinfo` `si2` ON ((`gi`.`summoner2Id` = `si2`.`summonerspell_id`)))
        LEFT JOIN `iteminfo` `iiv` ON ((`gi`.`visionItem` = `iiv`.`item_id`)))
        LEFT JOIN `iteminfo` `ii1` ON ((`gi`.`item1` = `ii1`.`item_id`)))
        LEFT JOIN `iteminfo` `ii2` ON ((`gi`.`item2` = `ii2`.`item_id`)))
        LEFT JOIN `iteminfo` `ii3` ON ((`gi`.`item3` = `ii3`.`item_id`)))
        LEFT JOIN `iteminfo` `ii4` ON ((`gi`.`item4` = `ii4`.`item_id`)))
        LEFT JOIN `iteminfo` `ii5` ON ((`gi`.`item5` = `ii5`.`item_id`)))
        LEFT JOIN `iteminfo` `ii6` ON ((`gi`.`item6` = `ii6`.`item_id`)))
        LEFT JOIN `runeinfo` `rikey` ON ((`gi`.`runeKeyStone` = `rikey`.`rune_id`)))
        LEFT JOIN (SELECT DISTINCT
            `runeinfo`.`rune_tree_id` AS `rune_tree_id`,
                `runeinfo`.`rune_tree_name` AS `rune_tree_name`
        FROM
            `runeinfo`) `riprim` ON ((`gi`.`runePrimary` = `riprim`.`rune_tree_id`)))
        LEFT JOIN `runeinfo` `ri1` ON ((`gi`.`runePrimary1` = `ri1`.`rune_id`)))
        LEFT JOIN `runeinfo` `ri2` ON ((`gi`.`runePrimary2` = `ri2`.`rune_id`)))
        LEFT JOIN `runeinfo` `ri3` ON ((`gi`.`runePrimary3` = `ri3`.`rune_id`)))
        LEFT JOIN (SELECT DISTINCT
            `runeinfo`.`rune_tree_id` AS `rune_tree_id`,
                `runeinfo`.`rune_tree_name` AS `rune_tree_name`
        FROM
            `runeinfo`) `risec` ON ((`gi`.`runeSecondary` = `risec`.`rune_tree_id`)))
        LEFT JOIN `runeinfo` `ris1` ON ((`gi`.`runeSecondary1` = `ris1`.`rune_id`)))
        LEFT JOIN `runeinfo` `ris2` ON ((`gi`.`runeSecondary2` = `ris2`.`rune_id`)))
        LEFT JOIN `championinfo` `tb1` ON ((`gi`.`teamBan1` = `tb1`.`champion_id`)))
        LEFT JOIN `championinfo` `tb2` ON ((`gi`.`teamBan2` = `tb2`.`champion_id`)))
        LEFT JOIN `championinfo` `tb3` ON ((`gi`.`teamBan3` = `tb3`.`champion_id`)))
        LEFT JOIN `championinfo` `tb4` ON ((`gi`.`teamBan4` = `tb4`.`champion_id`)))
        LEFT JOIN `championinfo` `tb5` ON ((`gi`.`teamBan5` = `tb5`.`champion_id`)))
        LEFT JOIN `championinfo` `eb1` ON ((`gi`.`enemyBan1` = `eb1`.`champion_id`)))
        LEFT JOIN `championinfo` `eb2` ON ((`gi`.`enemyBan2` = `eb2`.`champion_id`)))
        LEFT JOIN `championinfo` `eb3` ON ((`gi`.`enemyBan3` = `eb3`.`champion_id`)))
        LEFT JOIN `championinfo` `eb4` ON ((`gi`.`enemyBan4` = `eb4`.`champion_id`)))
        LEFT JOIN `championinfo` `eb5` ON ((`gi`.`enemyBan5` = `eb5`.`champion_id`)))
        LEFT JOIN `gameinfo` `opponents` ON (((`gi`.`gameId` = `opponents`.`gameId`)
            AND (`gi`.`teamPosition` = `opponents`.`teamPosition`)
            AND (`gi`.`teamSide` <> `opponents`.`teamSide`))))
        LEFT JOIN (SELECT 
            `gameinfo`.`gameId` AS `gameId`,
                `gameinfo`.`teamSide` AS `teamSide`,
                GROUP_CONCAT((CASE
                    WHEN
                        `gameinfo`.`playerName` NOT IN (SELECT DISTINCT
                                `friendinfo`.`summoner_name`
                            FROM
                                `friendinfo`)
                    THEN
                        'Other'
                    ELSE `gameinfo`.`playerName`
                END)
                    SEPARATOR ',') AS `teamArray`
        FROM
            `gameinfo`
        GROUP BY `gameinfo`.`gameId` , `gameinfo`.`teamSide`) `teammates` ON (((`gi`.`gameId` = `teammates`.`gameId`)
            AND (`gi`.`teamSide` = `teammates`.`teamSide`))))
    WHERE
        `gi`.`playerName` IN (SELECT DISTINCT
                `friendinfo`.`summoner_name`
            FROM
                `friendinfo`)