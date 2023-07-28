-- Crear schema de la base de datos `easygraph`
CREATE SCHEMA IF NOT EXISTS `easygraph`;

-- Usar schema de la base de datos `easygraph`
USE `easygraph`;

-- Crear tabla `easygraoh`.`users`
CREATE TABLE IF NOT EXISTS `easygraph`.`users` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `first_name` VARCHAR(45) NOT NULL,
    `email` VARCHAR(45) NOT NULL,
    `password` VARCHAR(255) NOT NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    UNIQUE KEY `email_UNIQUE` (`email`)
);

-- Crear tabla `examen_3`.`graficos_creados `
CREATE TABLE IF NOT EXISTS `easygraph`.`graficos` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `user_id` INT DEFAULT NULL,
    `tipo` VARCHAR(255)    NOT NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    FOREIGN KEY(`user_id`) REFERENCES `easygraph`.`users` (`id`) ON DELETE CASCADE
);


-- Crear tabla `easygraph` `perfiles`
CREATE TABLE IF NOT EXISTS `easygraph`.`profile` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `user_id` INT NOT NULL,
    `profesion` VARCHAR(45) NOT NULL,
    `edad` INT NOT NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    FOREIGN KEY(`user_id`) REFERENCES `easygraph`.`users` (`id`) ON DELETE CASCADE
);

-- Crear tabla `easygraph` `Gantt`
CREATE TABLE IF NOT EXISTS `easygraph`.`Gantt` (
    `id` INT NOT NULL AUTO_INCREMENT,
    `user_id` INT NOT NULL,
    `tarea` VARCHAR(45) NOT NULL,
    `fecha_inicio` DATE NOT NULL,
    `fecha_termino` DATE NOT NULL,
    `color` VARCHAR(45) NOT NULL,
    `created_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    `updated_at` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
    PRIMARY KEY (`id`),
    FOREIGN KEY(`user_id`) REFERENCES `easygraph`.`users` (`id`) ON DELETE CASCADE
);


ALTER TABLE profile
DROP COLUMN user_id,
ADD COLUMN user_id INT,
ADD FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE;

