SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;
CREATE TABLE IF NOT EXISTS `ec_classes_16_17_2` (`clsname` text,`day` int(11) DEFAULT NULL,`time` int(11) DEFAULT NULL,`teacher` text,`duration` text,`week` text,`location` text,`students` text,`id` varchar(50) NOT NULL,PRIMARY KEY (`id`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
CREATE TABLE IF NOT EXISTS `ec_students_16_17_2` (`xs0101id` varchar(40) NOT NULL,`name` text,`xh` varchar(40) NOT NULL,`classes` longtext,PRIMARY KEY (`xh`)) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
SET FOREIGN_KEY_CHECKS = 1;