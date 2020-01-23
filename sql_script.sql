DROP DATABASE IF EXISTS off_db;
CREATE DATABASE off_db
CHARACTER SET 'utf8mb4';
USE off_db;

CREATE TABLE category(
	id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
	category VARCHAR(150) NOT NULL UNIQUE,
	my_category BOOLEAN DEFAULT 0)
ENGINE=InnoDB;

CREATE TABLE store(
	id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
	store VARCHAR(50) NOT NULL UNIQUE)
ENGINE=InnoDB;


CREATE TABLE product(
	id INT UNSIGNED	PRIMARY KEY AUTO_INCREMENT,
	code VARCHAR(15) NOT NULL UNIQUE,
	url VARCHAR(150) NOT NULL UNIQUE,
	brands VARCHAR(100),
	product_name VARCHAR(170) NOT NULL UNIQUE,
	product_quantity VARCHAR(20),
	nutrition_grade_fr CHAR(1))
ENGINE=InnoDB;

CREATE TABLE product_save(
	id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
	product_id INT UNSIGNED NOT NULL,
	product_replace_id INT UNSIGNED NOT NULL) 
ENGINE=InnoDB;

CREATE TABLE stores_t(
	id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
	product_id INT UNSIGNED NOT NULL,
	store_id INT UNSIGNED NOT NULL)
ENGINE=InnoDB;

CREATE TABLE categories_t(
	id INT UNSIGNED PRIMARY KEY AUTO_INCREMENT,
	product_id INT UNSIGNED NOT NULL,
	category_id INT UNSIGNED NOT NULL)
ENGINE=InnoDB;
	

ALTER TABLE product_save
	ADD CONSTRAINT fk_product_save_1 FOREIGN KEY(product_id) REFERENCES product(id),
	ADD CONSTRAINT fk_product_save_2 FOREIGN KEY(product_replace_id) REFERENCES product(id);
	
ALTER TABLE stores_t
	ADD CONSTRAINT fk_pst_1 FOREIGN KEY(product_id) REFERENCES product(id),
	ADD CONSTRAINT fk_pst_2 FOREIGN KEY(store_id) REFERENCES store(id);
	
ALTER TABLE categories_t
	ADD CONSTRAINT fk_pct_1 FOREIGN KEY(product_id) REFERENCES product(id),
	ADD CONSTRAINT fk_pct_2 FOREIGN KEY(category_id) REFERENCES category(id);
	
CREATE UNIQUE INDEX product_stores ON stores_t(product_id, store_id);
CREATE UNIQUE INDEX product_categories ON categories_t(product_id, category_id);



