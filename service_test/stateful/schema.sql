CREATE TABLE player
(
    id bigserial PRIMARY KEY,
    name varchar(100),
    email varchar(100) UNIQUE
);

INSERT INTO player (name, email) values ('vasya', 'vasya@tut.by');
INSERT INTO player (name, email) values ('petya', 'petya@tut.by');
INSERT INTO player (name, email) values ('lesha', 'lesha@tut.by');
