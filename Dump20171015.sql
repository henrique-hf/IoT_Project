DROP TABLE IF EXISTS `p_t`;
CREATE TABLE `p_t` (
  `packetid` varchar(45) NOT NULL,
  `truckid` varchar(45) NOT NULL,
  `delivered` int(11) DEFAULT '0',
  PRIMARY KEY (`packetid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
DROP TABLE IF EXISTS `packet`;
CREATE TABLE `packet`(
  `packetid` varchar(45) NOT NULL,
  `name` varchar(45) NOT NULL,
  `address` varchar(45) NOT NULL,
  `n_address` varchar(45) NOT NULL,
  `zip` varchar(45) NOT NULL,
  `city` varchar(45) NOT NULL,
  `telephone` varchar(45) NOT NULL,
  `lat` varchar(45) NOT NULL,
  `long` varchar(45) NOT NULL,
  PRIMARY KEY (`packetid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
