use gender;

ALTER TABLE CONFIGURATION
ADD CONSTRAINT deletegender
    FOREIGN KEY (gender_name)
    REFERENCES GENDER (gender_name) 
    ON DELETE CASCADE;
