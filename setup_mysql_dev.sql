-- Prepares a MySQL server for the project development
CREATE DATABASE IF NOT EXISTS grochub_dev_db;
CREATE USER IF NOT EXISTS 'grochub_dev'@'localhost' IDENTIFIED BY 'GH_dev_pwd_1';
GRANT ALL PRIVILEGES ON `grochub_dev_db`.* TO 'grochub_dev'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'grochub_dev'@'localhost';
