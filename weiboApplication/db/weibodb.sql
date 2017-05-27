use weibodb;

CREATE TABLE `keywords` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `topic` varchar(120) CHARACTER SET utf8 DEFAULT NULL,
  `word` varchar(80) CHARACTER SET utf8 DEFAULT NULL,
  `weight` int(11) DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `topic` (`topic`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;


CREATE TABLE `method` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(120) CHARACTER SET utf8 DEFAULT NULL,
  `intro` varchar(200) CHARACTER SET utf8 DEFAULT NULL,
  `comment` varchar(120) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8

CREATE TABLE `result` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `method` varchar(120) DEFAULT NULL,
  `topic` varchar(120) DEFAULT NULL,
  `percise` float DEFAULT NULL,
  `recall` float DEFAULT NULL,
  `f_mesure` float DEFAULT NULL,
  `sum_mesure` float DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `method` (`method`),
  UNIQUE KEY `recall` (`recall`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `summary` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `topic` varchar(120) CHARACTER SET utf8 DEFAULT NULL,
  `content` varchar(200) CHARACTER SET utf8 DEFAULT NULL,
  `method` varchar(120) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `topic` (`topic`),
  UNIQUE KEY `method` (`method`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `weibo` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `topic` char(50) DEFAULT NULL,
  `content` varchar(200) CHARACTER SET utf8 DEFAULT NULL,
  `transfer` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `like` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  `comment` varchar(50) CHARACTER SET utf8 DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `topic` (`topic`)
) ENGINE=InnoDB AUTO_INCREMENT=6 DEFAULT CHARSET=utf8;