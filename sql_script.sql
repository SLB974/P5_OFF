DROP DATABASE IF EXISTS off_db ;
CREATE DATABASE off_db CHARACTER SET 'utf8';
USE off_db;

CREATE TABLE category (
	id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
	categories_fr VARCHAR(250) NOT NULL)
ENGINE=InnoDB;

CREATE TABLE product (
	id INT UNSIGNED	PRIMARY KEY AUTO_INCREMENT,
	code INT(10) ZEROFILL UNSIGNED,
	url VARCHAR(250) NOT NULL,
	brands VARCHAR(100) NOT NULL,
	product_name_fr VARCHAR(200) NOT NULL,
	category_id INT UNSIGNED NOT NULL UNIQUE,
	product_quantity VARCHAR(20),
	nutrition_grade_fr CHAR(1) NOT NULL,
	stores VARCHAR(100),
	CONSTRAINT fk_category_id FOREIGN KEY(category_id) REFERENCES category(id))
ENGINE=InnoDB;

CREATE TABLE product_save (
	id INT UNSIGNED	PRIMARY KEY AUTO_INCREMENT,
	date DATETIME NOT NULL,
	product_id INT UNSIGNED NOT NULL,
	product_replace_id INT UNSIGNED NOT NULL, 
	CONSTRAINT fk_product_save_1 FOREIGN KEY(product_id) REFERENCES product(id))
ENGINE=InnoDB;

ALTER TABLE product_save
	ADD CONSTRAINT fk_product_save_2 FOREIGN KEY(product_replace_id) REFERENCES product(id);
	
CREATE UNIQUE INDEX index_product_code ON product(code);
CREATE INDEX index_product_product_name_fr ON product(product_name_fr);
CREATE INDEX index_product_nutrition_grade_fr ON product(nutrition_grade_fr);
CREATE INDEX index_product_save_product_id ON product_save(product_id);
CREATE INDEX index_product_save_product_replace_id ON product_save(product_replace_id);

