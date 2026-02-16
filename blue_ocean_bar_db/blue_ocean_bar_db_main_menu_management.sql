-- MySQL dump 10.13  Distrib 8.0.41, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: blue_ocean_bar_db
-- ------------------------------------------------------
-- Server version	8.0.41

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `main_menu_management`
--

DROP TABLE IF EXISTS `main_menu_management`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `main_menu_management` (
  `menu_id` int NOT NULL AUTO_INCREMENT,
  `menu_name` varchar(100) NOT NULL,
  `category` varchar(50) NOT NULL,
  `kitchen_printer` varchar(50) DEFAULT NULL,
  `unit_price` decimal(10,2) NOT NULL,
  `picture_url` varchar(250) DEFAULT NULL,
  PRIMARY KEY (`menu_id`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci	;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `main_menu_management`
--

LOCK TABLES `main_menu_management` WRITE;
/*!40000 ALTER TABLE `main_menu_management` DISABLE KEYS */;
INSERT INTO `main_menu_management` VALUES (3,' Cheeseburger',' Main Course',' Grill Station',120.50,'Employee_Image\\Screenshot_2025-04-03_192947.png'),(4,'Chocolate Cake','dessert','kitchen_1',120.00,'uploads/choco_cake.jpg'),(5,'Halo-Halo Special','dessert','kitchen_1',95.00,'uploads/halo_halo.jpg'),(6,'Grilled Chicken','main_menu','kitchen_1',250.00,'uploads/grilled_chicken.jpg'),(7,'Beef Tapa','main_menu','kitchen_1',180.00,'uploads/beef_tapa.jpg'),(8,'Iced Tea','beverages','bar_printer',45.00,'uploads/iced_tea.jpg'),(9,'Mango Shake','beverages','bar_printer',85.00,'uploads/mango_shake.jpg'),(10,' Cheeseburger',' Main Course',' Grill Station',120.50,'Menu_Image\\Screenshot_2025-04-03_192947.png');
/*!40000 ALTER TABLE `main_menu_management` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-02-14 22:19:09
