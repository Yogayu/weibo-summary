-- MySQL dump 10.13  Distrib 5.7.17, for macos10.12 (x86_64)
--
-- Host: localhost    Database: weibodb
-- ------------------------------------------------------
-- Server version	5.7.10

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
-- Table structure for table `method`
--

DROP TABLE IF EXISTS `method`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!40101 SET character_set_client = utf8 */;
CREATE TABLE `method` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(120) DEFAULT NULL,
  `intro` varchar(800) DEFAULT NULL,
  `comment` varchar(120) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `method`
--

LOCK TABLES `method` WRITE;
/*!40000 ALTER TABLE `method` DISABLE KEYS */;
INSERT INTO `method` VALUES (1,'随机算法 Random Algorithm ','随机算法从一个微博话题数据集中，随机的抽取K条微博作为摘要。考虑到Python生成的是伪随机数，将多次进行随机算法实验以取得平均值。选择该算法的原因是，为了提供一个对比下限，以供其他算法比较。','基线算法'),(2,'最近摘要算法 MostRecent Algorithm','最近摘要算法选取微博话题数据集中，排在最前的K条微博作为摘要。这种个算法，类似于在新闻文章中，选取第一段作为文本摘要。有时候复杂的算法，反而没有这种简单算法效果好。','基线算法'),(3,' TF-IDF算法 TF-IDF Algorithm ','TF-IDF(Term Frequency-Inverse Document Frequency)算法即词频-逆向文档词频算法。它是一种特征项权重计算方法，已被应用于许多信息检索问题，例如，自动索引，文档查询匹配和自动文摘。其中，TF（Term Frequency）即为词频，是指一个特定的词汇在给定的一份文档中出现的频率。一个词的TF越大，即说明其在文档中更重要，因为重要的词经常被重复使用。但是，一个词如果仅使用其在文档中的频率判断重要性，是不科学的。诸如停等词之类的词，会反复在文本中出现，但这些词不能够帮助区分一个句子或文档。在处理停等词时，如果直接进行过滤，那么就需要一份停等词词典。如果之后词汇扩充，就需要对停等词词典的修改和补充。这种情况下，人为干扰因素会很大。所以，现在大多会加入IDF(Inverse Document Frequency)即逆向文档频率，进行处理。在一个文档集合中，某一个特征项出现的文档数，称为DF（Document Frequency）即文档频率。IDF即DF的倒数。IDF值越大，说明文档中该词的出现越为集中，区分文档的能力越好。 ','基于词频统计的算法'),(4,'混合TF-IDF算法 Hybrid TF-IDF Algorithm','在TF-IDF算法中，将一个微博定义为一个文档，这样IDF部分的定义也很清楚。但是TF部分，有着明显的问题。因为一个微博只包含了少数单词，所以每一个帖子中词的TF值将会很小。另一种方法是，将话题微博数据集合作为一个文档，但是这样IDF部分将会丢失。 	为了处理上述情况，我们使用改进的混合TF-IDF算法。首先，在计算IDF时，将一个微博作为一个文档；然后，在计算TF值时，将整个话题微博数据集作为一个文档。这种定一下，TF-IDF的两个部分都能有效作用。此外，该算法将句子的权重除以归一化因子来归一化。','基于词频统计的算法'),(5,'TextRank算法 TextRank Algorithm','TextRank算法是一种使用PageRank的基于图模型的算法。该算法将文档中的句子作为图的结点，计算出每两个结点之间的文本相似度作为边，形成初始图模型。之后，使用PageRank对初始图模型不断的迭代直到收敛。最后，将与结点相连的每条边的权重相加，排序得到前K个结点，作为最终的摘要输出。','基于图的算法');
/*!40000 ALTER TABLE `method` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2017-06-08 22:05:54
