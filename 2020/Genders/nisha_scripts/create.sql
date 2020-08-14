create database gender;
use gender;

create table NODE(
node_name varchar(30) unique not null,
node_num int,
cluster varchar(30),
PRIMARY KEY (node_name)
);

create table GENDER(
gender_name varchar(100) unique not null, 
descrip varchar(255),
PRIMARY KEY (gender_name)
);

create table CONFIGURATION(
config_id varchar(30) unique not null,
val varchar(30),
node_name varchar(30),
gender_name varchar(100),
PRIMARY KEY(config_id),
FOREIGN KEY (node_name)
REFERENCES NODE (node_name)
ON DELETE CASCADE,
FOREIGN KEY (gender_name)
REFERENCES GENDER (gender_name)
ON DELETE CASCADE
);

