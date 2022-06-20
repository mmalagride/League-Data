CREATE TABLE `fact.championinfo` (
  `champion_id` int(11) NOT NULL,
  `champion_name` varchar(45) NOT NULL,
  `champion_tags` varchar(60) NOT NULL,
  `champion_image` varchar(45) NOT NULL,
  PRIMARY KEY (`champion_id`),
  UNIQUE (`champion_id`,`champion_name`,`champion_image`)
);
