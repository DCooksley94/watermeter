SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL,ALLOW_INVALID_DATES';

drop schema if exists `capstoneHugh`;

create schema if not exists `capstoneHugh` default charset latin1;
use `capstoneHugh`;

Create table if not exists `capstoneHugh`.`water_Meter_Raw`
(
    `id` int not null auto_increment,
    `recordDate` datetime not null,
    `volume` double not null,
    primary key (`id`)
) engine = innodb;

Create table if not exists `capstoneHugh`.`day_Meter_Data`
(
    `id` int not null auto_increment,
    `recordDate` datetime not null,
    `volume` double not null,
    primary key (`id`)
) engine = innodb;

Create table if not exists `capstoneHugh`.`month_Meter_Data`
(
    `id` int not null auto_increment,
    `recordDate` datetime not null,
    `volume` double not null,
    primary key (`id`)
) engine = innodb;

Create table if not exists `capstoneHugh`.`User`
(
    `username` varchar(20) not null,
    `password` varchar(50) not null,
    `fName` varchar(20),
    `lName` varchar(20),
    `email` varchar(50),
    primary key (`username`)
) engine = innodb;

Create table if not exists `capstoneHugh`.`Report`
(
    `id` int not null auto_increment,
    `freq` enum("daily","weekly","bi-weekly","monthly","limit"),
    `user` varchar(20) not null,
    primary key (`id`),
    foreign key (`user`) references `capstoneHugh`.`User`(`username`) on delete cascade on update cascade
) engine = innodb;
