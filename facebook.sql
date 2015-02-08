-- MySQL dump 10.13  Distrib 5.6.16, for osx10.6 (x86_64)
--
-- Host: localhost    Database: facebook
-- ------------------------------------------------------
-- Server version	5.6.16

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
-- Table structure for table `Apps`
--
CREATE DATABASE facebook;
USE facebook;
DROP TABLE IF EXISTS `Apps`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Apps` (
  `ID` bigint(20) NOT NULL,
  `Name` varchar(255) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Apps`
--

LOCK TABLES `Apps` WRITE;
/*!40000 ALTER TABLE `Apps` DISABLE KEYS */;
/*!40000 ALTER TABLE `Apps` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Apps_Users`
--

DROP TABLE IF EXISTS `Apps_Users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Apps_Users` (
  `App_ID` bigint(20) NOT NULL,
  `User_ID` bigint(20) NOT NULL,
  PRIMARY KEY (`App_ID`,`User_ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Apps_Users`
--

LOCK TABLES `Apps_Users` WRITE;
/*!40000 ALTER TABLE `Apps_Users` DISABLE KEYS */;
/*!40000 ALTER TABLE `Apps_Users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `City`
--

DROP TABLE IF EXISTS `City`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `City` (
  `ID` bigint(20) NOT NULL,
  `Name` varchar(255) NOT NULL,
  `State` varchar(255) NOT NULL,
  PRIMARY KEY (`ID`),
  UNIQUE KEY `Name` (`Name`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `City`
--

LOCK TABLES `City` WRITE;
/*!40000 ALTER TABLE `City` DISABLE KEYS */;
INSERT INTO `City` VALUES (0,'\'Vadodara - Baroda\'','\'\''),(106282486076109,'\'Bengaluru\'','\'\''),(106306812739694,'\'Jaipur\'','\'Rajasthan\''),(106487939387579,'\'Gurgaon\'','\'Haryana\''),(106517799384578,'\'New Delhi\'','\'India\''),(110753475619095,'\'Gandhinagar\'','\'Gujarat\''),(114574285221912,'\'Lalitpur\'','\'Uttar Pradesh\''),(115200305158163,'\'Hyderabad\'','\'Andhra Pradesh\''),(115440481803904,'\'Ahmedabad\'','\'India\'');
/*!40000 ALTER TABLE `City` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Comment_likes`
--

DROP TABLE IF EXISTS `Comment_likes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Comment_likes` (
  `Comment_id` bigint(20) NOT NULL,
  `User_id` bigint(20) NOT NULL,
  PRIMARY KEY (`Comment_id`,`User_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Comment_likes`
--

LOCK TABLES `Comment_likes` WRITE;
/*!40000 ALTER TABLE `Comment_likes` DISABLE KEYS */;
/*!40000 ALTER TABLE `Comment_likes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Comments`
--

DROP TABLE IF EXISTS `Comments`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Comments` (
  `ID` bigint(20) NOT NULL AUTO_INCREMENT,
  `Content` longtext NOT NULL,
  `Timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `User_id` bigint(20) NOT NULL,
  `Parent_id` bigint(20) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=19 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Comments`
--

LOCK TABLES `Comments` WRITE;
/*!40000 ALTER TABLE `Comments` DISABLE KEYS */;
INSERT INTO `Comments` VALUES (1,'\'lots of creativity inside\'','2011-01-26 17:14:00',100001003840953,173843512659109),(2,'\'lots of creativity inside\'','2011-01-26 17:14:00',100001003840953,173843512659109),(3,'\'lots of creativity inside\'','2011-01-26 17:14:00',100001003840953,173843512659109),(4,'\'lots of creativity inside\'','2011-01-26 17:14:00',100001003840953,173843512659109),(5,'\'lots of creativity inside\'','2011-01-26 17:14:00',100001003840953,173843512659109),(6,'\'lots of creativity inside\'','2011-01-26 17:14:00',100001003840953,173843512659109),(7,'\'lots of creativity inside\'','2011-01-26 17:14:00',100001003840953,173843512659109),(8,'\'lots of creativity inside\'','2011-01-26 17:14:00',100001003840953,173843512659109),(9,'\'cute :3\'','2014-10-08 19:36:00',100001003840953,768112653245456),(10,'\'Amrit Khanna bauji kisko taad rahe hoo...\'','2014-10-08 19:36:00',100001003840953,10152451092522568),(11,'\'Congo bro... :)\'','2014-10-08 19:36:00',100001003840953,707239365990784),(12,'\'Congo bro... :)\'','2014-10-08 19:36:00',100001003840953,707239365990784),(13,'\'nice click!!\'','2014-10-08 19:36:00',100001003840953,692410970823013),(14,'\'nice click!!\'','2014-10-08 19:36:00',100001003840953,692410970823013),(15,'\'~~nyc photogrphy~~\'','2014-10-08 19:36:00',100001003840953,4167888168029),(16,'\'~~nyc photogrphy~~\'','2014-10-08 19:36:00',100001003840953,4167888168029),(17,'\'thanku..will be waiting !!!!!!\'','2014-10-08 19:36:00',100001003840953,245429972167129),(18,'\'thanku..will be waiting !!!!!!\'','2014-10-08 19:36:00',100001003840953,245429972167129);
/*!40000 ALTER TABLE `Comments` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Entities`
--

DROP TABLE IF EXISTS `Entities`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Entities` (
  `ID` bigint(20) NOT NULL AUTO_INCREMENT,
  `Type` varchar(255) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Entities`
--

LOCK TABLES `Entities` WRITE;
/*!40000 ALTER TABLE `Entities` DISABLE KEYS */;
INSERT INTO `Entities` VALUES (8,'\'User\''),(9,'\'User\''),(10,'\'User\''),(11,'\'User\''),(12,'\'User\''),(13,'\'User\''),(14,'\'User\''),(15,'\'User\''),(16,'\'User\''),(17,'\'User\''),(18,'\'User\''),(19,'\'User\''),(20,'\'User\''),(21,'\'User\''),(22,'\'User\''),(23,'\'User\''),(24,'\'User\''),(25,'\'User\''),(26,'\'User\''),(27,'\'User\''),(28,'\'User\''),(29,'\'User\''),(30,'\'User\''),(31,'\'User\''),(32,'\'User\''),(33,'\'User\''),(34,'\'User\''),(35,'\'User\''),(36,'\'User\''),(37,'\'User\''),(38,'\'User\''),(39,'\'User\''),(40,'\'User\''),(41,'\'User\''),(42,'\'User\''),(43,'\'User\''),(44,'\'User\''),(45,'\'User\''),(46,'\'User\''),(47,'\'User\''),(48,'\'User\'');
/*!40000 ALTER TABLE `Entities` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `FB_events`
--

DROP TABLE IF EXISTS `FB_events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `FB_events` (
  `ID` bigint(20) NOT NULL,
  `Name` varchar(255) NOT NULL,
  `Desc` varchar(255) NOT NULL,
  `Place` bigint(20) NOT NULL,
  `Time` datetime NOT NULL,
  `Host` bigint(20) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `FB_events`
--

LOCK TABLES `FB_events` WRITE;
/*!40000 ALTER TABLE `FB_events` DISABLE KEYS */;
/*!40000 ALTER TABLE `FB_events` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `FB_events_attendees`
--

DROP TABLE IF EXISTS `FB_events_attendees`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `FB_events_attendees` (
  `User_id` bigint(20) NOT NULL,
  `Event_id` bigint(20) NOT NULL,
  `Type` varchar(255) NOT NULL,
  PRIMARY KEY (`User_id`,`Event_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `FB_events_attendees`
--

LOCK TABLES `FB_events_attendees` WRITE;
/*!40000 ALTER TABLE `FB_events_attendees` DISABLE KEYS */;
/*!40000 ALTER TABLE `FB_events_attendees` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Feed`
--

DROP TABLE IF EXISTS `Feed`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Feed` (
  `ID` bigint(20) NOT NULL,
  `Type` varchar(255) NOT NULL,
  `Content` longtext NOT NULL,
  `Caption` longtext NOT NULL,
  `Timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `User_id` bigint(20) NOT NULL,
  `Entity_id` bigint(20) NOT NULL,
  `City_id` bigint(20) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Feed`
--

LOCK TABLES `Feed` WRITE;
/*!40000 ALTER TABLE `Feed` DISABLE KEYS */;
INSERT INTO `Feed` VALUES (1654182684534,'\'Photo\'','\'\'','\'\'','2010-11-04 18:30:00',1536084283,0,0),(1655278711934,'\'Photo\'','\'\'','\'treat!!!!!!!!\'','2010-11-05 18:30:00',0,0,0),(2123348335811,'\'Photo\'','\'\'','\'\'','2011-08-10 18:30:00',0,0,0),(3757999101028,'\'Photo\'','\'\'','\'\'','2012-06-05 18:30:00',1008022400,0,0),(4167888168029,'\'Photo\'','\'\'','\'Courtesy: Sahil Shah\'','2012-09-08 18:30:00',1608944161,0,0),(159728370737290,'\'Photo\'','\'\'','\'\'','2010-11-29 18:30:00',100001003840953,30,0),(173843512659109,'\'Video\'','\'\'','\'Say something about this video...\'','2011-01-25 18:30:00',100001003840953,14,0),(173847259325401,'\'Video\'','\'Spoof\'','\'Awesome Spoof of Harry Potterrrrrrrrrrrrrrrrrrrrr..........................................\'','2011-01-25 18:30:00',100001003840953,14,0),(175896382453822,'\'Video\'','\'kudhte fudhte chinese chore\'','\'Amazinnnnnnnnnnnnnnnnnnng vediooooooooooooooooooooooo       never ever in your life you have seen thing like thissssssssssssssssssssssss\'','2011-02-02 18:30:00',100001003840953,14,0),(176287039081423,'\'Video\'','\'\'','\'NICE VIDEO--fIREWORK BY KATY PERRY\'','2011-02-04 18:30:00',100001003840953,14,0),(211635768879883,'\'Photo\'','\'\'','\'My cousins\'','2011-06-29 18:30:00',100001003840953,30,0),(245429972167129,'\'Photo\'','\'\'','\'Create yours @ http://apps.facebook.com/fgiftbox/\'','2011-09-08 18:30:00',100001003840953,30,0),(271635836213209,'\'Photo\'','\'\'','\'\'','2011-11-07 18:30:00',100001003840953,30,0),(345438075499651,'\'Photo\'','\'\'','\'\'','2012-03-07 18:30:00',100001003840953,30,0),(635647963145326,'\'Photo\'','\'\'','\'\'','2013-11-15 18:30:00',0,0,0),(645365355506920,'\'Photo\'','\'\'','\'\'','2013-12-06 18:30:00',0,0,0),(692409700823140,'\'Photo\'','\'\'','\'\'','2014-04-05 18:30:00',100001623508973,0,0),(692410217489755,'\'Photo\'','\'\'','\'\'','2014-04-05 18:30:00',100001623508973,0,0),(692410417489735,'\'Photo\'','\'\'','\'\'','2014-04-05 18:30:00',100001623508973,0,0),(692410517489725,'\'Photo\'','\'\'','\'\'','2014-04-05 18:30:00',100001623508973,0,0),(692410970823013,'\'Photo\'','\'\'','\'\'','2014-04-05 18:30:00',100001623508973,0,0),(692411307489646,'\'Photo\'','\'\'','\'\'','2014-04-05 18:30:00',100001623508973,0,0),(692411450822965,'\'Photo\'','\'\'','\'\'','2014-04-05 18:30:00',100001623508973,0,0),(692411564156287,'\'Photo\'','\'\'','\'\'','2014-04-05 18:30:00',100001623508973,0,0),(692411680822942,'\'Photo\'','\'\'','\'\'','2014-04-05 18:30:00',100001623508973,0,0),(692411774156266,'\'Photo\'','\'\'','\'\'','2014-04-05 18:30:00',100001623508973,0,0),(692411887489588,'\'Photo\'','\'\'','\'\'','2014-04-05 18:30:00',100001623508973,0,0),(692411910822919,'\'Photo\'','\'\'','\'\'','2014-04-05 18:30:00',100001623508973,0,0),(692412307489546,'\'Photo\'','\'\'','\'\'','2014-04-05 18:30:00',100001623508973,0,0),(707239365990784,'\'Photo\'','\'\'','\'Ready to pull the throttle until thrill of speed overcomes the fear of crashing... @140 kmph At last I brought the combination of speed power comfort and those stunning looks... Pulsar 200ns...\'','2014-08-30 18:30:00',100001141815129,0,0),(727012750675513,'\'Photo\'','\'\'','\'\'','2014-05-18 18:30:00',100001003840953,30,0),(768112653245456,'\'Photo\'','\'\'','\'\'','2014-09-08 18:30:00',100001401840843,0,0),(778297645547023,'\'Photo\'','\'\'','\'thanks Dhruv Patel for taking this awesome pic \'','2014-09-01 18:30:00',100001003840953,30,0),(10152451092522568,'\'Photo\'','\'\'','\'\'','2014-10-08 18:30:00',657762567,0,0),(10200349817521509,'\'Photo\'','\'\'','\'\'','2013-04-06 18:30:00',0,0,0),(10203888832651314,'\'Photo\'','\'\'','\'sorry Prashu Chaudhary I know we won\'t upload pics but this one is damn awesome!!!!! pic courtesy: Prerna Garg\'','2014-05-18 18:30:00',0,0,0);
/*!40000 ALTER TABLE `Feed` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Feeds_tags`
--

DROP TABLE IF EXISTS `Feeds_tags`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Feeds_tags` (
  `Photo_id` bigint(20) NOT NULL,
  `User_id` bigint(20) NOT NULL,
  PRIMARY KEY (`Photo_id`,`User_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Feeds_tags`
--

LOCK TABLES `Feeds_tags` WRITE;
/*!40000 ALTER TABLE `Feeds_tags` DISABLE KEYS */;
/*!40000 ALTER TABLE `Feeds_tags` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Friends`
--

DROP TABLE IF EXISTS `Friends`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Friends` (
  `User_id1` bigint(20) NOT NULL,
  `User_id2` bigint(20) NOT NULL,
  PRIMARY KEY (`User_id1`,`User_id2`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Friends`
--

LOCK TABLES `Friends` WRITE;
/*!40000 ALTER TABLE `Friends` DISABLE KEYS */;
/*!40000 ALTER TABLE `Friends` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Group_members`
--

DROP TABLE IF EXISTS `Group_members`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Group_members` (
  `Group_id` bigint(20) NOT NULL,
  `User_id` bigint(20) NOT NULL,
  PRIMARY KEY (`Group_id`,`User_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Group_members`
--

LOCK TABLES `Group_members` WRITE;
/*!40000 ALTER TABLE `Group_members` DISABLE KEYS */;
/*!40000 ALTER TABLE `Group_members` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Groups`
--

DROP TABLE IF EXISTS `Groups`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Groups` (
  `ID` bigint(20) NOT NULL,
  `Desc` longtext NOT NULL,
  `Entity_id` bigint(20) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Groups`
--

LOCK TABLES `Groups` WRITE;
/*!40000 ALTER TABLE `Groups` DISABLE KEYS */;
/*!40000 ALTER TABLE `Groups` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Jobs`
--

DROP TABLE IF EXISTS `Jobs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Jobs` (
  `ID` bigint(20) NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) NOT NULL,
  `Description` varchar(255) NOT NULL,
  `User_id` bigint(20) NOT NULL,
  `Place_id` bigint(20) NOT NULL,
  `Timestamp_start` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  `Timestamp_end` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00',
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Jobs`
--

LOCK TABLES `Jobs` WRITE;
/*!40000 ALTER TABLE `Jobs` DISABLE KEYS */;
/*!40000 ALTER TABLE `Jobs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Life_events`
--

DROP TABLE IF EXISTS `Life_events`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Life_events` (
  `ID` bigint(20) NOT NULL AUTO_INCREMENT,
  `User_id` bigint(20) NOT NULL,
  `Desc` varchar(255) NOT NULL,
  `Place_id` bigint(20) NOT NULL,
  `Timestamp` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Life_events`
--

LOCK TABLES `Life_events` WRITE;
/*!40000 ALTER TABLE `Life_events` DISABLE KEYS */;
/*!40000 ALTER TABLE `Life_events` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Page_likes`
--

DROP TABLE IF EXISTS `Page_likes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Page_likes` (
  `Page_id` varchar(255) NOT NULL,
  `User_id` bigint(20) NOT NULL,
  PRIMARY KEY (`Page_id`,`User_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Page_likes`
--

LOCK TABLES `Page_likes` WRITE;
/*!40000 ALTER TABLE `Page_likes` DISABLE KEYS */;
/*!40000 ALTER TABLE `Page_likes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Pages`
--

DROP TABLE IF EXISTS `Pages`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Pages` (
  `ID` varchar(255) NOT NULL,
  `Type` varchar(255) NOT NULL,
  `Name` longtext NOT NULL,
  `Owner` bigint(20) NOT NULL,
  `Entity_id` bigint(20) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Pages`
--

LOCK TABLES `Pages` WRITE;
/*!40000 ALTER TABLE `Pages` DISABLE KEYS */;
/*!40000 ALTER TABLE `Pages` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Photos_likes`
--

DROP TABLE IF EXISTS `Photos_likes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Photos_likes` (
  `Photo_id` bigint(20) NOT NULL,
  `User_id` bigint(20) NOT NULL,
  PRIMARY KEY (`Photo_id`,`User_id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Photos_likes`
--

LOCK TABLES `Photos_likes` WRITE;
/*!40000 ALTER TABLE `Photos_likes` DISABLE KEYS */;
INSERT INTO `Photos_likes` VALUES (3757999101028,100001003840953),(692409700823140,100001003840953),(692410217489755,100001003840953),(692410417489735,100001003840953),(692410517489725,100001003840953),(692411307489646,100001003840953),(692411450822965,100001003840953),(692411564156287,100001003840953),(692411680822942,100001003840953),(692411774156266,100001003840953),(692411887489588,100001003840953),(692411910822919,100001003840953),(692412307489546,100001003840953),(10152451092522568,100001003840953);
/*!40000 ALTER TABLE `Photos_likes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Place`
--

DROP TABLE IF EXISTS `Place`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Place` (
  `ID` bigint(20) NOT NULL AUTO_INCREMENT,
  `Name` varchar(255) NOT NULL,
  `City` bigint(20) NOT NULL,
  PRIMARY KEY (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=234 DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Place`
--

LOCK TABLES `Place` WRITE;
/*!40000 ALTER TABLE `Place` DISABLE KEYS */;
INSERT INTO `Place` VALUES (15,'\'TIFAC\'',106517799384578),(16,'\'ISRO\'',0),(17,'\'TIFAC\'',106517799384578),(18,'\'ISRO\'',0),(19,'\'DA-IICT\'',0),(20,'\'Jaipuria Vidyalaya\'',106306812739694),(21,'\'Dhirubhai Ambani Institute of Information and Communication Technology (DA-IICT), Gandhinagar\'',110753475619095),(22,'\'DA-IICT\'',110753475619095),(23,'\'TIFAC\'',106517799384578),(24,'\'ISRO\'',0),(25,'\'DA-IICT\'',0),(26,'\'Jaipuria Vidyalaya\'',0),(27,'\'Dhirubhai Ambani Institute of Information and Communication Technology (DA-IICT), Gandhinagar\'',110753475619095),(28,'\'DA-IICT\'',110753475619095),(29,'\'TIFAC\'',106517799384578),(30,'\'ISRO\'',0),(31,'\'DA-IICT\'',0),(32,'\'Jaipuria Vidyalaya\'',106306812739694),(33,'\'Dhirubhai Ambani Institute of Information and Communication Technology (DA-IICT), Gandhinagar\'',0),(34,'\'DA-IICT\'',110753475619095),(35,'\'TIFAC\'',0),(36,'\'ISRO\'',0),(37,'\'DA-IICT\'',0),(38,'\'Jaipuria Vidyalaya\'',0),(39,'\'Dhirubhai Ambani Institute of Information and Communication Technology (DA-IICT), Gandhinagar\'',110753475619095),(40,'\'DA-IICT\'',110753475619095),(41,'\'TIFAC\'',106517799384578),(42,'\'ISRO\'',0),(43,'\'DA-IICT\'',0),(44,'\'Jaipuria Vidyalaya\'',106306812739694),(45,'\'Dhirubhai Ambani Institute of Information and Communication Technology (DA-IICT), Gandhinagar\'',110753475619095),(46,'\'DA-IICT\'',110753475619095),(47,'\'TIFAC\'',106517799384578),(48,'\'ISRO\'',0),(49,'\'DA-IICT\'',0),(50,'\'Jaipuria Vidyalaya\'',106306812739694),(51,'\'Dhirubhai Ambani Institute of Information and Communication Technology (DA-IICT), Gandhinagar\'',110753475619095),(52,'\'DA-IICT\'',110753475619095),(53,'\'TIFAC\'',106517799384578),(54,'\'ISRO\'',0),(55,'\'DA-IICT\'',0),(56,'\'Jaipuria Vidyalaya\'',106306812739694),(57,'\'Dhirubhai Ambani Institute of Information and Communication Technology (DA-IICT), Gandhinagar\'',110753475619095),(58,'\'DA-IICT\'',110753475619095),(59,'\'TIFAC\'',106517799384578),(60,'\'ISRO\'',0),(61,'\'DA-IICT\'',0),(62,'\'Jaipuria Vidyalaya\'',106306812739694),(63,'\'Dhirubhai Ambani Institute of Information and Communication Technology (DA-IICT), Gandhinagar\'',110753475619095),(64,'\'DA-IICT\'',110753475619095),(65,'\'TIFAC\'',106517799384578),(66,'\'ISRO\'',0),(67,'\'DA-IICT\'',0),(68,'\'Jaipuria Vidyalaya\'',106306812739694),(69,'\'Dhirubhai Ambani Institute of Information and Communication Technology (DA-IICT), Gandhinagar\'',110753475619095),(70,'\'DA-IICT\'',110753475619095),(71,'\'TIFAC\'',106517799384578),(72,'\'ISRO\'',0),(73,'\'DA-IICT\'',0),(74,'\'Jaipuria Vidyalaya\'',106306812739694),(75,'\'Dhirubhai Ambani Institute of Information and Communication Technology (DA-IICT), Gandhinagar\'',110753475619095),(76,'\'DA-IICT\'',110753475619095),(77,'\'TIFAC\'',106517799384578),(78,'\'ISRO\'',0),(79,'\'DA-IICT\'',0),(80,'\'Jaipuria Vidyalaya\'',0),(81,'\'Dhirubhai Ambani Institute of Information and Communication Technology (DA-IICT), Gandhinagar\'',110753475619095),(82,'\'DA-IICT\'',110753475619095),(83,'\'TIFAC\'',106517799384578),(84,'\'ISRO\'',0),(85,'\'DA-IICT\'',0),(86,'\'Jaipuria Vidyalaya\'',106306812739694),(87,'\'Dhirubhai Ambani Institute of Information and Communication Technology (DA-IICT), Gandhinagar\'',110753475619095),(88,'\'DA-IICT\'',110753475619095),(89,'\'TIFAC\'',106517799384578),(90,'\'ISRO\'',0),(91,'\'DA-IICT\'',0),(92,'\'Jaipuria Vidyalaya\'',106306812739694),(93,'\'Dhirubhai Ambani Institute of Information and Communication Technology (DA-IICT), Gandhinagar\'',110753475619095),(94,'\'DA-IICT\'',110753475619095),(95,'\'TIFAC\'',106517799384578),(96,'\'ISRO\'',0),(97,'\'DA-IICT\'',0),(98,'\'Jaipuria Vidyalaya\'',106306812739694),(99,'\'Dhirubhai Ambani Institute of Information and Communication Technology (DA-IICT), Gandhinagar\'',110753475619095),(100,'\'DA-IICT\'',110753475619095),(101,'\'TIFAC\'',106517799384578),(102,'\'ISRO\'',0),(103,'\'DA-IICT\'',0),(104,'\'Jaipuria Vidyalaya\'',0),(105,'\'Dhirubhai Ambani Institute of Information and Communication Technology (DA-IICT), Gandhinagar\'',110753475619095),(106,'\'DA-IICT\'',0),(107,'\'TIFAC\'',106517799384578),(108,'\'ISRO\'',0),(109,'\'DA-IICT\'',0),(110,'\'Jaipuria Vidyalaya\'',106306812739694),(111,'\'Dhirubhai Ambani Institute of Information and Communication Technology (DA-IICT), Gandhinagar\'',110753475619095),(112,'\'DA-IICT\'',110753475619095),(113,'\'TIFAC\'',106517799384578),(114,'\'ISRO\'',0),(115,'\'DA-IICT\'',0),(116,'\'Jaipuria Vidyalaya\'',106306812739694),(117,'\'Dhirubhai Ambani Institute of Information and Communication Technology (DA-IICT), Gandhinagar\'',110753475619095),(118,'\'DA-IICT\'',110753475619095),(119,'\'TIFAC\'',106517799384578),(120,'\'ISRO\'',0),(121,'\'DA-IICT\'',0),(122,'\'Jaipuria Vidyalaya\'',106306812739694),(123,'\'Dhirubhai Ambani Institute of Information and Communication Technology (DA-IICT), Gandhinagar\'',110753475619095),(124,'\'DA-IICT\'',110753475619095),(125,'\'TIFAC\'',106517799384578),(126,'\'ISRO\'',0),(127,'\'DA-IICT\'',0),(128,'\'Jaipuria Vidyalaya\'',106306812739694),(129,'\'Dhirubhai Ambani Institute of Information and Communication Technology (DA-IICT), Gandhinagar\'',110753475619095),(130,'\'DA-IICT\'',110753475619095),(131,'\'TIFAC\'',106517799384578),(132,'\'ISRO\'',0),(133,'\'DA-IICT\'',0),(134,'\'Jaipuria Vidyalaya\'',106306812739694),(135,'\'Dhirubhai Ambani Institute of Information and Communication Technology (DA-IICT), Gandhinagar\'',110753475619095),(136,'\'DA-IICT\'',110753475619095),(137,'\'TIFAC\'',106517799384578),(138,'\'ISRO\'',0),(139,'\'DA-IICT\'',0),(140,'\'Jaipuria Vidyalaya\'',0),(141,'\'Dhirubhai Ambani Institute of Information and Communication Technology (DA-IICT), Gandhinagar\'',110753475619095),(142,'\'DA-IICT\'',110753475619095),(143,'\'TIFAC\'',106517799384578),(144,'\'ISRO\'',0),(145,'\'DA-IICT\'',0),(146,'\'Jaipuria Vidyalaya\'',106306812739694),(147,'\'Dhirubhai Ambani Institute of Information and Communication Technology (DA-IICT), Gandhinagar\'',110753475619095),(148,'\'DA-IICT\'',110753475619095),(149,'\'TIFAC\'',106517799384578),(150,'\'ISRO\'',0),(151,'\'DA-IICT\'',0),(152,'\'Jaipuria Vidyalaya\'',106306812739694),(153,'\'Dhirubhai Ambani Institute of Information and Communication Technology (DA-IICT), Gandhinagar\'',110753475619095),(154,'\'DA-IICT\'',110753475619095),(155,'\'TIFAC\'',106517799384578),(156,'\'ISRO\'',0),(157,'\'DA-IICT\'',0),(158,'\'Jaipuria Vidyalaya\'',106306812739694),(159,'\'Dhirubhai Ambani Institute of Information and Communication Technology (DA-IICT), Gandhinagar\'',110753475619095),(160,'\'DA-IICT\'',110753475619095),(161,'\'TIFAC\'',106517799384578),(162,'\'ISRO\'',0),(163,'\'DA-IICT\'',0),(164,'\'Jaipuria Vidyalaya\'',106306812739694),(165,'\'Dhirubhai Ambani Institute of Information and Communication Technology (DA-IICT), Gandhinagar\'',110753475619095),(166,'\'DA-IICT\'',110753475619095),(167,'\'TIFAC\'',106517799384578),(168,'\'ISRO\'',0),(169,'\'DA-IICT\'',0),(170,'\'Jaipuria Vidyalaya\'',106306812739694),(171,'\'Dhirubhai Ambani Institute of Information and Communication Technology (DA-IICT), Gandhinagar\'',0),(172,'\'DA-IICT\'',110753475619095),(173,'\'TIFAC\'',106517799384578),(174,'\'ISRO\'',0),(175,'\'DA-IICT\'',0),(176,'\'Jaipuria Vidyalaya\'',106306812739694),(177,'\'Dhirubhai Ambani Institute of Information and Communication Technology (DA-IICT), Gandhinagar\'',110753475619095),(178,'\'DA-IICT\'',110753475619095),(179,'\'TIFAC\'',106517799384578),(180,'\'ISRO\'',0),(181,'\'DA-IICT\'',0),(182,'\'Jaipuria Vidyalaya\'',106306812739694),(183,'\'Dhirubhai Ambani Institute of Information and Communication Technology (DA-IICT), Gandhinagar\'',110753475619095),(184,'\'DA-IICT\'',110753475619095),(185,'\'TIFAC\'',106517799384578),(186,'\'TIFAC\'',106517799384578),(187,'\'Indusface\'',0),(188,'\'DA-IICT\'',0),(189,'\'TIFAC - Department of Science and Technology (DST)\'',0),(190,'\'Delhi Public School, Ahmedabad\'',115440481803904),(191,'\'Dhirubhai Ambani Institute of Information and Communication Technology\'',110753475619095),(192,'\'DA-IICT\'',110753475619095),(193,'\'TIFAC\'',106517799384578),(194,'\'Indusface\'',0),(195,'\'DA-IICT\'',0),(196,'\'TIFAC - Department of Science and Technology (DST)\'',0),(197,'\'Delhi Public School, Ahmedabad\'',115440481803904),(198,'\'Dhirubhai Ambani Institute of Information and Communication Technology\'',110753475619095),(199,'\'DA-IICT\'',110753475619095),(200,'\'TIFAC\'',106517799384578),(201,'\'Indusface\'',0),(202,'\'DA-IICT\'',0),(203,'\'TIFAC - Department of Science and Technology (DST)\'',0),(204,'\'Delhi Public School, Ahmedabad\'',115440481803904),(205,'\'Dhirubhai Ambani Institute of Information and Communication Technology\'',110753475619095),(206,'\'DA-IICT\'',110753475619095),(207,'\'TIFAC\'',106517799384578),(208,'\'Indusface\'',0),(209,'\'DA-IICT\'',0),(210,'\'TIFAC - Department of Science and Technology (DST)\'',0),(211,'\'Delhi Public School, Ahmedabad\'',115440481803904),(212,'\'Dhirubhai Ambani Institute of Information and Communication Technology\'',110753475619095),(213,'\'DA-IICT\'',0),(214,'\'TIFAC\'',106517799384578),(215,'\'Indusface\'',0),(216,'\'DA-IICT\'',0),(217,'\'TIFAC - Department of Science and Technology (DST)\'',0),(218,'\'Delhi Public School, Ahmedabad\'',115440481803904),(219,'\'Dhirubhai Ambani Institute of Information and Communication Technology\'',110753475619095),(220,'\'DA-IICT\'',110753475619095),(221,'\'TIFAC\'',106517799384578),(222,'\'Indusface\'',0),(223,'\'DA-IICT\'',0),(224,'\'TIFAC - Department of Science and Technology (DST)\'',0),(225,'\'Delhi Public School, Ahmedabad\'',115440481803904),(226,'\'Dhirubhai Ambani Institute of Information and Communication Technology\'',110753475619095),(227,'\'DA-IICT\'',110753475619095),(228,'\'Bharatiya Vidya Bhavans Hyderabad\'',115200305158163),(229,'\'Meridian School For Boys And Girls\'',115200305158163),(230,'\'Bharatiya Vidya Bhavans Hyderabad\'',115200305158163),(231,'\'Meridian School For Boys And Girls\'',115200305158163),(232,'\'Bharatiya Vidya Bhavans Hyderabad\'',0),(233,'\'Meridian School For Boys And Girls\'',115200305158163);
/*!40000 ALTER TABLE `Place` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `Relationships`
--

DROP TABLE IF EXISTS `Relationships`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `Relationships` (
  `User_id1` bigint(20) NOT NULL,
  `User_id2` bigint(20) NOT NULL,
  `type` varchar(255) NOT NULL,
  PRIMARY KEY (`User_id1`,`User_id2`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `Relationships`
--

LOCK TABLES `Relationships` WRITE;
/*!40000 ALTER TABLE `Relationships` DISABLE KEYS */;
INSERT INTO `Relationships` VALUES (709299000,0,'\'couple\''),(709299000,831702575,'\'\''),(1695117164,1403873261,'\'couple\'');
/*!40000 ALTER TABLE `Relationships` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `User`
--

DROP TABLE IF EXISTS `User`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `User` (
  `ID` bigint(20) NOT NULL,
  `Name` varchar(255) NOT NULL,
  `Username` varchar(255) NOT NULL,
  `DOB` date NOT NULL,
  `Gender` varchar(255) NOT NULL,
  `Bio` mediumtext NOT NULL,
  `Relationship_status` varchar(255) NOT NULL,
  `Current_city` bigint(20) NOT NULL,
  `Current_work` bigint(20) NOT NULL,
  `Hometown` bigint(20) NOT NULL,
  `email` varchar(255) NOT NULL,
  `phone` varchar(255) NOT NULL,
  `Entity_id` bigint(20) NOT NULL,
  PRIMARY KEY (`ID`),
  KEY `Username` (`Username`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `User`
--

LOCK TABLES `User` WRITE;
/*!40000 ALTER TABLE `User` DISABLE KEYS */;
INSERT INTO `User` VALUES (709299000,'\'Anand Mudgerikar\'','\'anand.mudgerikar\'','0000-00-00','\'None\'','\'\'','\'In relationship\'',106517799384578,227,115440481803904,'\'\'','\'\'',46),(1403873261,'\'Krati Gupta\'','\'Amory09\'','0000-00-00','\'Female\'','\'\'','\'\'',0,0,0,'\'\'','\'\'',47),(1695117164,'\'Prithvi Guntur\'','\'gksprithvi\'','0000-00-00','\'Male\'','\'\'','\'In relationship\'',106282486076109,233,106487939387579,'\'\'','\'\'',48),(100001003840953,'\'Prashu Chaudhary\'','\'prashu.chaudhary\'','0000-00-00','\'Male\'','\'I love Classics   !!! Music Is my Medicine  !!!\'','\'\'',106306812739694,100,114574285221912,'\'\'','\'\'',30);
/*!40000 ALTER TABLE `User` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2014-10-15 20:49:21
