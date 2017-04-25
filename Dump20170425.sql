CREATE DATABASE  IF NOT EXISTS `tracking` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `tracking`;
-- MySQL dump 10.13  Distrib 5.7.17, for Linux (x86_64)
--
-- Host: 127.0.0.1    Database: tracking
-- ------------------------------------------------------
-- Server version	5.5.5-10.1.21-MariaDB

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `p_t`
--

DROP TABLE IF EXISTS `p_t`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `p_t` (
  `packetid` varchar(45) NOT NULL,
  `truckid` varchar(45) NOT NULL,
  PRIMARY KEY (`packetid`,`truckid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `p_t`
--

LOCK TABLES `p_t` WRITE;
/*!40000 ALTER TABLE `p_t` DISABLE KEYS */;
INSERT INTO `p_t` VALUES ('171602042017','1');
/*!40000 ALTER TABLE `p_t` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `packet`
--

DROP TABLE IF EXISTS `packet`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `packet` (
  `packetid` varchar(45) NOT NULL,
  `name` varchar(45) DEFAULT NULL,
  `address` varchar(45) DEFAULT NULL,
  `zip` varchar(45) DEFAULT NULL,
  `city` varchar(45) DEFAULT NULL,
  `telephone` varchar(45) DEFAULT NULL,
  `n_address` varchar(45) DEFAULT NULL,
  PRIMARY KEY (`packetid`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `packet`
--

LOCK TABLES `packet` WRITE;
/*!40000 ALTER TABLE `packet` DISABLE KEYS */;
INSERT INTO `packet` VALUES ('051602042017','Matteo Nisi','Corso Vittorio Emanuele II','10121','Torino','','62'),('151602042017','Henrique da Fonseca','Corso Re Umberto','10128','Torino','','23'),('161602042017','Carla Trejo','Corso Stati Uniti','10128','Torino','','32'),('171602042017','Stefano Calleris','Corso Duca degli Abruzzi','10129','Torino','','24');
/*!40000 ALTER TABLE `packet` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-04-25 17:58:01
