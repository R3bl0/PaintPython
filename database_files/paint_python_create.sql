-- Created by Vertabelo (http://vertabelo.com)
-- Last modification date: 2024-06-02 16:28:37.488

-- tables
-- Table: Players
CREATE TABLE Players (
    Id int  NOT NULL AUTO_INCREMENT,
    Nick nvarchar(20)  NOT NULL,
    Points int  NOT NULL DEFAULT 0,
    CONSTRAINT Players_pk PRIMARY KEY (Id)
);

-- Table: Topics
CREATE TABLE Topics (
    Id int  NOT NULL AUTO_INCREMENT,
    Name nvarchar(20)  NOT NULL,
    CONSTRAINT Topics_pk PRIMARY KEY (Id)
);

INSERT INTO Topics(Name) VALUES ('Cat');
INSERT INTO Topics(Name) VALUES ('Dog');
INSERT INTO Topics(Name) VALUES ('Fish');
INSERT INTO Topics(Name) VALUES ('Tomato');
INSERT INTO Topics(Name) VALUES ('Onion');
INSERT INTO Topics(Name) VALUES ('Potato');
INSERT INTO Topics(Name) VALUES ('Apple');
INSERT INTO Topics(Name) VALUES ('Pear');
INSERT INTO Topics(Name) VALUES ('Watermelon');
INSERT INTO Topics(Name) VALUES ('Car');
INSERT INTO Topics(Name) VALUES ('Plane');
INSERT INTO Topics(Name) VALUES ('Ship');

INSERT INTO Players(nick, points) VALUES ('R3bl0', 0);
INSERT INTO Players(nick, points) VALUES ('Jbbib', 0);
INSERT INTO Players(nick, points) VALUES ('Padrino', 0);

COMMIT;

-- End of file.

