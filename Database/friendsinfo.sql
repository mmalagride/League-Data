CREATE TABLE `friendsinfo` (
  `summoner_accountid` varchar(60) NOT NULL,
  `summoner_name` varchar(45) NOT NULL,
  `summoner_level` int(11) NOT NULL,
  `summoner_image` varchar(45) NOT NULL,
  `summoner_puuid` varchar(90) NOT NULL,
  `summoner_lastupdate` bigint(32) NOT NULL,
  PRIMARY KEY (`summoner_name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
