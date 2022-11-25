CREATE TABLE `championinfo` (
  `champion_id` int(11) NOT NULL,
  `champion_name` varchar(45) NOT NULL,
  `champion_tags` varchar(60) NOT NULL,
  `champion_image` varchar(45) NOT NULL,
  PRIMARY KEY (`champion_id`),
  UNIQUE KEY `ChampionID_UNIQUE` (`champion_id`),
  UNIQUE KEY `champion_name_UNIQUE` (`champion_name`),
  UNIQUE KEY `Champion_Image_UNIQUE` (`champion_image`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
