--
-- Table structure for table `p_t`
--
DROP SCHEMA IF EXISTS `tracking`;
CREATE SCHEMA `tracking`;

ALTER USER root WITH DEFAULT_SCHEMA = `tracking`;


DROP TABLE IF EXISTS `p_t`;
CREATE TABLE `p_t` (
  `packetid` varchar(45) NOT NULL,
  `truckid` varchar(45) NOT NULL,
  `delivered` int(11) DEFAULT '0',
  PRIMARY KEY (`packetid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;


-- Dumping data for table `p_t`


INSERT INTO `p_t` VALUES ('20170508203317','1',0);

-- Table structure for table `packet`

DROP TABLE IF EXISTS `packet`;
CREATE TABLE `packet` (
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

--
-- Dumping data for table `packet`
--

INSERT INTO `packet` VALUES ('20170508203143','Giuseppe Garibaldi','Via Nizza','4','10100','Torino','1000','45.0190839','7.6627022'),('20170508203216','Marco Polo','Via Cigna','4','10100','Torino','1000','45.0798589','7.6771077'),('20170508203317','Francesco Totti','Via Roma','10','10100','Torino','1000','45.0703976','7.6844939'),('20170508203559','Francesco Totti','Via Roma','10','10100','Torino','1000','45.0703976','7.6844939'),('20170508203704','Francesco Totti','Via Roma','10','10100','Torino','1000','45.0703976','7.6844939'),('20170508203840','Francesco Totti','Via Roma','10','10100','Torino','1000','45.0703976','7.6844939'),('20171003160446','A','B','5','10136','Torino','3495674108','45.0737586','7.6843145'),('20171003162827','oi','rua grauna','379','04514001','sao paulo','666','-23.6014379','-46.6709769');
-- Dump completed on 2017-10-15  8:08:43
