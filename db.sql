DROP DATABASE IF EXISTS `trails`;
CREATE DATABASE `trails`;
USE `trails`;


CREATE TABLE `users` (
    `id` INT PRIMARY KEY AUTO_INCREMENT, 
    `name` VARCHAR(1000),
    `email` VARCHAR(1000),
    `password` VARCHAR(225)
);


CREATE TABLE cloths (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `name` VARCHAR(500),
    `category` VARCHAR(500),
    `cost` INT,
    `img` VARCHAR(1000)
);


CREATE TABLE cart (
    `id` INT PRIMARY KEY AUTO_INCREMENT,
    `product_id` INT,
    `status` VARCHAR(225)
);