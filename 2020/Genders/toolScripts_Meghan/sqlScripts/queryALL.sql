use gender;

#show all of the different genders in the database
SELECT DISTINCT gender_name FROM GENDER; 

#all nodes that have a particular gender
#I hard coded a value for a gender to look up as an example but when we have python it will make it interactive
SELECT DISTINCT n.node_name FROM NODE n JOIN CONFIGURATION c WHERE (n.node_name = c.node_name AND c.gender_name = "archive_zone" );

#all genders in a particular 
#gender is hard coded for now but will be changed to be interative later
SELECT DISTINCT g.gender_name FROM GENDER g JOIN CONFIGURATION c WHERE (g.gender_name = c.gender_name AND c.node_name = "test1");
