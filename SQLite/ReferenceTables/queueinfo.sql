CREATE TABLE `fact.queueinfo` (
  `queue_id` int(11) NOT NULL,
  `queue_map` varchar(45) NOT NULL,
  `queue_description` varchar(45) NOT NULL,
  PRIMARY KEY (`queue_id`),
  UNIQUE (`queue_id`)
);
