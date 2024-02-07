

USE appo_mgt_sys;

CREATE TABLE IF NOT EXISTS clients (
	client_id INT AUTO_INCREMENT PRIMARY KEY,
	user_name VARCHAR(128) NOT NULL,
       	first_name VARCHAR(228) NOT NULL,
       	last_name VARCHAR(228) NOT NULL,
       	phone_number VARCHAR(15) NOT NULL,
       	password VARCHAR(20) NOT NULL,
       	email VARCHAR(255) NOT NULL,
	UNIQUE (user_name)
);

CREATE TABLE IF NOT EXISTS providers (
	provider_id INT AUTO_INCREMENT PRIMARY KEY,
       	provider_name VARCHAR(128) NOT NULL,
       	provider_address VARCHAR(200) NOT NULL,
       	phone_number VARCHAR(15) NOT NULL,
       	password VARCHAR(20) NOT NULL,
       	email VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS services (
	service_id INT AUTO_INCREMENT PRIMARY KEY,
       	service_name VARCHAR(228) NOT NULL,
       	description VARCHAR(500) NOT NULL,
       	provider_id INT,
       	FOREIGN KEY(provider_id) REFERENCES providers(provider_id)
);

CREATE TABLE IF NOT EXISTS appointments (
	appointment_id INT AUTO_INCREMENT PRIMARY KEY,
       	service_name VARCHAR(228) NOT NULL,
	date_time DATETIME NOT NULL,
       	description VARCHAR(500) NOT NULL,
       	location VARCHAR(128),
	provider_id INT,
	client_id INT,
	service_id INT, 
       	FOREIGN KEY(provider_id) REFERENCES providers(provider_id),
       	FOREIGN KEY(client_id) REFERENCES clients(client_id),
       	FOREIGN KEY(service_id) REFERENCES services(service_id)
);
