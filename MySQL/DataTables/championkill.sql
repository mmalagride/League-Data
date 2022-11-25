CREATE TABLE `championkill` (
  `event_gameid` varchar(45) NOT NULL,
  `event_type` varchar(45) NOT NULL,
  `event_timestamp` varchar(45) NOT NULL,
  `event_killerid` varchar(120) DEFAULT NULL,
  `event_victimid` varchar(120) DEFAULT NULL,
  `event_assist1` varchar(120) DEFAULT NULL,
  `event_assist2` varchar(120) DEFAULT NULL,
  `event_assist3` varchar(120) DEFAULT NULL,
  `event_assist4` varchar(120) DEFAULT NULL,
  `event_killedby` varchar(45) DEFAULT NULL,
  `event_posx` varchar(45) DEFAULT NULL,
  `event_posy` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`event_gameid`,`event_type`,`event_timestamp`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
