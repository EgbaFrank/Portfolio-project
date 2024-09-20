-- Prepares a MySQL server for the project development
CREATE DATABASE IF NOT EXISTS grochub_test_db;
CREATE USER IF NOT EXISTS 'grochub_test'@'localhost' IDENTIFIED BY 'GH_test_pwd_1';
GRANT ALL PRIVILEGES ON `grochub_test_db`.* TO 'grochub_test'@'localhost';
GRANT SELECT ON `performance_schema`.* TO 'grochub_test'@'localhost';
