CREATE TABLE `runeinfo` (
  `rune_id` int(11) NOT NULL,
  `rune_name` varchar(45) DEFAULT NULL,
  `rune_icon` varchar(80) DEFAULT NULL,
  `rune_tree_id` int(11) DEFAULT NULL,
  `rune_tree_name` varchar(45) DEFAULT NULL,
  `rune_tree_icon` varchar(80) DEFAULT NULL,
  PRIMARY KEY (`rune_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
