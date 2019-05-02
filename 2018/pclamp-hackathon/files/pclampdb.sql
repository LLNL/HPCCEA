DROP TABLE IF EXISTS papers;
CREATE TABLE papers
(
    paperid    INT NOT NULL AUTO_INCREMENT PRIMARY KEY, 
    pubmedid   VARCHAR(30),    # pubmed record ID
    authors    TEXT,           # list of authors of the paper
    papertext  TEXT            # text of the paper
);

INSERT INTO papers (pubmedid, authors, papertext) VALUES ('283456','A. Jones, B. Smith', 'This is the paper test for the first paper' );
INSERT INTO papers (pubmedid, authors, papertext) VALUES ('324312','S. Smith, C. Crabtree', 'Test of 2nd paper' );
INSERT INTO papers (pubmedid, authors, papertext) VALUES ('443212','J. Tolkien, T. Odinson', 'Paper number 3' );

DROP TABLE IF EXISTS pclamps;
CREATE TABLE pclamps
(
    pclamPid    INT NOT NULL AUTO_INCREMENT PRIMARY KEY, 
    fk_paperid  INT,            # foregin key to paper
    figurenum   INT,            # figure number in the paper
    species     VARCHAR(20),           
    sex         varchar(8),           
    graphpath   TEXT            # path in the file system on server to the graph image
);

INSERT INTO pclamps (fk_paperid, figurenum, species, sex, graphpath) VALUES (1 , 1, 'rat', 'male', 'pclamps/pclamp1-1.png' );
INSERT INTO pclamps (fk_paperid, figurenum, species, sex, graphpath) VALUES (1 , 2, 'mouse', 'female', 'pclamps/pclamp1-2.png' );
INSERT INTO pclamps (fk_paperid, figurenum, species, sex, graphpath) VALUES (2 , 1, 'frog', 'female', 'pclamps/pclamp2-1.png' );
INSERT INTO pclamps (fk_paperid, figurenum, species, sex, graphpath) VALUES (3 , 1, 'dog', 'male', 'pclamps/pclamp3-1.png' );
INSERT INTO pclamps (fk_paperid, figurenum, species, sex, graphpath) VALUES (3 , 2, 'dog', 'female', 'pclamps/pclamp3-2.png' );
