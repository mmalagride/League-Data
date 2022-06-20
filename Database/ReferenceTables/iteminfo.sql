CREATE TABLE `fact.iteminfo` (
  `item_id` int(11) NOT NULL,
  `item_name` varchar(45) DEFAULT NULL,
  `item_into` varchar(150) DEFAULT NULL,
  `item_from` varchar(45) DEFAULT NULL,
  `item_cost` int(11) DEFAULT NULL,
  `item_tags` varchar(150) DEFAULT NULL,
  `item_image` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`item_id`)
);
