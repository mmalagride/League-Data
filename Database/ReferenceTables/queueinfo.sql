CREATE TABLE `queueinfo` (
  `queue_id` int(11) NOT NULL,
  `queue_map` varchar(45) NOT NULL,
  `queue_description` varchar(45) NOT NULL,
  PRIMARY KEY (`queue_id`),
  UNIQUE KEY `queue_id_UNIQUE` (`queue_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
