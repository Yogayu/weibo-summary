-- @author:youxinyu
-- CREATE SCHEMA `weibodb` DEFAULT CHARACTER SET utf8 ;
use weibodb;

CREATE TABLE `topic` (
  `name` varchar(80) DEFAULT NULL,
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name_UNIQUE` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8

CREATE TABLE `keywords` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `topic` varchar(120) CHARACTER SET utf8 DEFAULT NULL,
  `word` varchar(80) CHARACTER SET utf8 DEFAULT NULL,
  `weight` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `method` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(120) CHARACTER SET utf8 DEFAULT NULL,
  `intro` varchar(200) CHARACTER SET utf8 DEFAULT NULL,
  `comment` varchar(120) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `result` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `method` varchar(120) DEFAULT NULL,
  `topic` varchar(120) DEFAULT NULL,
  `percise` float DEFAULT NULL,
  `recall` float DEFAULT NULL,
  `f_mesure` float DEFAULT NULL,
  `sum_mesure` float DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `summary` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `topic` varchar(120) CHARACTER SET utf8 DEFAULT NULL,
  `content` varchar(200) CHARACTER SET utf8 DEFAULT NULL,
  `content_segment` varchar(400) CHARACTER SET utf8 DEFAULT NULL,
  `method` varchar(120) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `weibo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `topic` char(50) DEFAULT NULL,
  `content` varchar(200) CHARACTER SET utf8 DEFAULT NULL,
  `transfer` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `like` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `comment` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;