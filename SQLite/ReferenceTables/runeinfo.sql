CREATE TABLE `fact.runeinfo` (
  `rune_id` int(11) NOT NULL,
  `rune_name` varchar(45) DEFAULT NULL,
  `rune_icon` varchar(80) DEFAULT NULL,
  `rune_tree_id` int(11) DEFAULT NULL,
  `rune_tree_name` varchar(45) DEFAULT NULL,
  `rune_tree_icon` varchar(80) DEFAULT NULL,
  PRIMARY KEY (`rune_id`)
);
