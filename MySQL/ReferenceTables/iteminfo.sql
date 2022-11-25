CREATE TABLE `iteminfo` (
  `item_id` int(11) NOT NULL,
  `item_name` varchar(90) DEFAULT NULL,
  `item_into` varchar(150) DEFAULT NULL,
  `item_from` varchar(90) DEFAULT NULL,
  `item_cost` int(11) DEFAULT NULL,
  `item_tags` varchar(150) DEFAULT NULL,
  `item_image` varchar(90) DEFAULT NULL,
  PRIMARY KEY (`item_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
