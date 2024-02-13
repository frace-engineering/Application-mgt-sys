

USE appo_mgt_sys;

CREATE TABLE IF NOT EXISTS users (
	id INT AUTO_INCREMENT PRIMARY KEY,
       	username VARCHAR(128) NOT NULL,
       	email VARCHAR(255) NOT NULL,
       	password VARCHAR(20) NOT NULL,
       	phone_number VARCHAR(15) NOT NULL
);

CREATE TABLE IF NOT EXISTS providers (
	id INT AUTO_INCREMENT PRIMARY KEY,
	username VARCHAR(128) NOT NULL,
       	provider_name VARCHAR(128),
       	provider_address VARCHAR(200),
       	email VARCHAR(255) NOT NULL,
       	password VARCHAR(20) NOT NULL,
	appointment VARCHAR(500), 
       	phone_number VARCHAR(15) NOT NULL,
	user_id INT,
	FOREIGN KEY(user_id) REFERENCES users(id)

);


CREATE TABLE IF NOT EXISTS clients (
	id INT AUTO_INCREMENT PRIMARY KEY,
	username VARCHAR(128) NOT NULL,
       	first_name VARCHAR(228),
       	last_name VARCHAR(228),
       	email VARCHAR(255) NOT NULL,
       	password VARCHAR(20) NOT NULL,
	appointment VARCHAR(500), 
       	phone_number VARCHAR(15) NOT NULL,
	user_id INT,
	provider_id INT,
	FOREIGN KEY(user_id) REFERENCES users(id),
       	FOREIGN KEY(provider_id) REFERENCES providers(id)
);

CREATE TABLE IF NOT EXISTS services (
	id INT AUTO_INCREMENT PRIMARY KEY,
       	service_name VARCHAR(228) NOT NULL,
       	description VARCHAR(500) NOT NULL,
	appointment VARCHAR(500), 
       	provider_id INT,
       	FOREIGN KEY(provider_id) REFERENCES providers(id)
);

CREATE TABLE IF NOT EXISTS appointments (
	id INT AUTO_INCREMENT PRIMARY KEY,
       	service_name VARCHAR(228) NOT NULL,
	date_time DATETIME NOT NULL,
       	description VARCHAR(500) NOT NULL,
       	location VARCHAR(128),
	provider_id INT,
	client_id INT,
	service_id INT, 
       	FOREIGN KEY(provider_id) REFERENCES providers(id),
       	FOREIGN KEY(client_id) REFERENCES clients(id),
       	FOREIGN KEY(service_id) REFERENCES services(id)
);
