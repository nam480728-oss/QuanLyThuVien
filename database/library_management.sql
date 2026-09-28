-- MySQL dump 10.13  Distrib 8.4.0, for Win64 (x86_64)
--
-- Host: 127.0.0.1    Database: library_management
-- ------------------------------------------------------
-- Server version	8.4.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Current Database: `library_management`
--

CREATE DATABASE /*!32312 IF NOT EXISTS*/ `library_management` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci */ /*!80016 DEFAULT ENCRYPTION='N' */;

USE `library_management`;

--
-- Table structure for table `alembic_version`
--

DROP TABLE IF EXISTS `alembic_version`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `alembic_version` (
  `version_num` varchar(32) COLLATE utf8mb4_unicode_ci NOT NULL,
  PRIMARY KEY (`version_num`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `alembic_version`
--

LOCK TABLES `alembic_version` WRITE;
/*!40000 ALTER TABLE `alembic_version` DISABLE KEYS */;
INSERT INTO `alembic_version` VALUES ('2a3b0b38577d');
/*!40000 ALTER TABLE `alembic_version` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `authors`
--

DROP TABLE IF EXISTS `authors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `authors` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) COLLATE utf8mb4_unicode_ci NOT NULL,
  `biography` text COLLATE utf8mb4_unicode_ci,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_authors_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `authors`
--

LOCK TABLES `authors` WRITE;
/*!40000 ALTER TABLE `authors` DISABLE KEYS */;
INSERT INTO `authors` VALUES (1,'Paulo Coelho',NULL),(2,'Haruki Murakami',NULL),(3,'Stephen Hawking',NULL),(4,'Daniel Kahneman',NULL),(5,'Dan Senor',NULL),(6,'Saul Singer',NULL),(7,'Robert C. Martin',NULL),(8,'Luciano Ramalho',NULL),(9,'Dale Carnegie',NULL),(10,'James Clear',NULL);
/*!40000 ALTER TABLE `authors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `book_authors`
--

DROP TABLE IF EXISTS `book_authors`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `book_authors` (
  `book_id` int NOT NULL,
  `author_id` int NOT NULL,
  PRIMARY KEY (`book_id`,`author_id`),
  KEY `author_id` (`author_id`),
  CONSTRAINT `book_authors_ibfk_1` FOREIGN KEY (`author_id`) REFERENCES `authors` (`id`) ON DELETE CASCADE,
  CONSTRAINT `book_authors_ibfk_2` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`) ON DELETE CASCADE
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `book_authors`
--

LOCK TABLES `book_authors` WRITE;
/*!40000 ALTER TABLE `book_authors` DISABLE KEYS */;
INSERT INTO `book_authors` VALUES (1,1),(2,2),(3,3),(4,3),(5,4),(6,5),(6,6),(7,7),(8,8),(9,9),(10,10);
/*!40000 ALTER TABLE `book_authors` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `books`
--

DROP TABLE IF EXISTS `books`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `books` (
  `id` int NOT NULL AUTO_INCREMENT,
  `isbn` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `title` varchar(220) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` text COLLATE utf8mb4_unicode_ci,
  `publisher` varchar(150) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `published_year` int DEFAULT NULL,
  `location` varchar(50) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `cover_url` varchar(500) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `total_copies` int NOT NULL,
  `available_copies` int NOT NULL,
  `category_id` int DEFAULT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_books_isbn` (`isbn`),
  KEY `ix_books_available_copies` (`available_copies`),
  KEY `ix_books_category_id` (`category_id`),
  KEY `ix_books_title` (`title`),
  CONSTRAINT `books_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`id`) ON DELETE SET NULL
) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `books`
--

LOCK TABLES `books` WRITE;
/*!40000 ALTER TABLE `books` DISABLE KEYS */;
INSERT INTO `books` VALUES (1,'9786043497244','Nhà giả kim','Một tựa sách nổi bật thuộc thể loại văn học, được tuyển chọn cho kho sách LibraHub.','Nhã Nam',1988,'A-01',NULL,5,5,1,'2026-09-28 01:19:56','2026-09-28 01:19:56'),(2,'9786049631468','Rừng Na Uy','Một tựa sách nổi bật thuộc thể loại văn học, được tuyển chọn cho kho sách LibraHub.','Hội Nhà Văn',1987,'A-02',NULL,4,4,1,'2026-09-28 01:19:56','2026-09-28 01:19:56'),(3,'9786041077615','Lược sử thời gian','Một tựa sách nổi bật thuộc thể loại khoa học, được tuyển chọn cho kho sách LibraHub.','Trẻ',1988,'B-01',NULL,3,3,2,'2026-09-28 01:19:56','2026-09-28 01:19:56'),(4,'9786041126585','Vũ trụ trong vỏ hạt dẻ','Một tựa sách nổi bật thuộc thể loại khoa học, được tuyển chọn cho kho sách LibraHub.','Trẻ',2001,'B-02',NULL,3,3,2,'2026-09-28 01:19:56','2026-09-28 01:19:56'),(5,'9786045555386','Tư duy nhanh và chậm','Một tựa sách nổi bật thuộc thể loại kinh tế, được tuyển chọn cho kho sách LibraHub.','Thế Giới',2011,'C-01',NULL,6,6,3,'2026-09-28 01:19:56','2026-09-28 01:19:56'),(6,'9786049858209','Quốc gia khởi nghiệp','Một tựa sách nổi bật thuộc thể loại kinh tế, được tuyển chọn cho kho sách LibraHub.','Thế Giới',2009,'C-02',NULL,4,4,3,'2026-09-28 01:19:56','2026-09-28 01:19:56'),(7,'9780132350884','Clean Code','Một tựa sách nổi bật thuộc thể loại công nghệ, được tuyển chọn cho kho sách LibraHub.','Prentice Hall',2008,'D-01',NULL,5,5,4,'2026-09-28 01:19:56','2026-09-28 01:19:56'),(8,'9781492056355','Fluent Python','Một tựa sách nổi bật thuộc thể loại công nghệ, được tuyển chọn cho kho sách LibraHub.','O\'Reilly',2022,'D-02',NULL,3,3,4,'2026-09-28 01:19:56','2026-09-28 01:19:56'),(9,'9786045675251','Đắc nhân tâm','Một tựa sách nổi bật thuộc thể loại kỹ năng, được tuyển chọn cho kho sách LibraHub.','Tổng hợp TP.HCM',1936,'E-01',NULL,7,7,5,'2026-09-28 01:19:56','2026-09-28 01:19:56'),(10,'9786045896106','Atomic Habits','Một tựa sách nổi bật thuộc thể loại kỹ năng, được tuyển chọn cho kho sách LibraHub.','Thế Giới',2018,'E-02',NULL,6,6,5,'2026-09-28 01:19:56','2026-09-28 01:19:56');
/*!40000 ALTER TABLE `books` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) COLLATE utf8mb4_unicode_ci NOT NULL,
  `description` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_categories_name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES (1,'Văn học','Tiểu thuyết, truyện ngắn và tác phẩm văn chương'),(2,'Khoa học','Khoa học tự nhiên và khám phá thế giới'),(3,'Kinh tế','Quản trị, tài chính và khởi nghiệp'),(4,'Công nghệ','Lập trình, dữ liệu và chuyển đổi số'),(5,'Kỹ năng','Phát triển bản thân và kỹ năng sống');
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `loans`
--

DROP TABLE IF EXISTS `loans`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `loans` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `book_id` int NOT NULL,
  `status` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `requested_at` datetime NOT NULL,
  `borrowed_at` datetime DEFAULT NULL,
  `due_at` datetime DEFAULT NULL,
  `returned_at` datetime DEFAULT NULL,
  `renew_count` int NOT NULL,
  `fine_amount` int NOT NULL,
  `fine_paid` tinyint(1) NOT NULL,
  `notes` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `processed_by` int DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `processed_by` (`processed_by`),
  KEY `ix_loans_book_id` (`book_id`),
  KEY `ix_loans_status` (`status`),
  KEY `ix_loans_status_due` (`status`,`due_at`),
  KEY `ix_loans_user_id` (`user_id`),
  CONSTRAINT `loans_ibfk_1` FOREIGN KEY (`book_id`) REFERENCES `books` (`id`) ON DELETE RESTRICT,
  CONSTRAINT `loans_ibfk_2` FOREIGN KEY (`processed_by`) REFERENCES `users` (`id`) ON DELETE SET NULL,
  CONSTRAINT `loans_ibfk_3` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE RESTRICT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `loans`
--

LOCK TABLES `loans` WRITE;
/*!40000 ALTER TABLE `loans` DISABLE KEYS */;
/*!40000 ALTER TABLE `loans` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `id` int NOT NULL AUTO_INCREMENT,
  `full_name` varchar(120) COLLATE utf8mb4_unicode_ci NOT NULL,
  `email` varchar(190) COLLATE utf8mb4_unicode_ci NOT NULL,
  `password_hash` varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
  `role` varchar(20) COLLATE utf8mb4_unicode_ci NOT NULL,
  `phone` varchar(20) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `address` varchar(255) COLLATE utf8mb4_unicode_ci DEFAULT NULL,
  `active` tinyint(1) NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `ix_users_email` (`email`),
  KEY `ix_users_role` (`role`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'Quản trị LibraHub','admin@librahub.vn','scrypt:32768:8:1$5opSC6f8lGruCyTi$2c26c7bd763aca373c8b6deca2ec3478387a421526ca535fbdd9236cee40f5fa4d2371176cb4cd7c73257ee9217a79f9665098eadb75b676c879b9c91e2f2ba8','admin',NULL,NULL,1,'2026-09-28 01:19:56','2026-09-28 01:19:56'),(2,'Thủ thư LibraHub','thuthu@librahub.vn','scrypt:32768:8:1$RqfyeAJ0jdB0Taue$814f586f40ea5bac19f60522ce02e45219683f755bc8896770c7f1ca8bc1ef2b545791e08215db8608e0bda086114545267933ed9e7d4d35be48567d2b73db7c','librarian',NULL,NULL,1,'2026-09-28 01:19:56','2026-09-28 01:19:56'),(3,'Nguyễn Minh An','docgia@librahub.vn','scrypt:32768:8:1$3REEH0i3qQ27zXvw$76f6ca30780d5feeea2f44c35ae0158340abd042f305a6e8b3547247356460c963556b49f41cfcd17bbdb1408877249d264802d6bc45415958cc58808658fbe3','reader',NULL,NULL,1,'2026-09-28 01:19:56','2026-09-28 01:19:56');
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Dumping events for database 'library_management'
--

--
-- Dumping routines for database 'library_management'
--
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2026-09-28  8:22:43
