sudo psql -U rim99 -d BlogDatabase -c "CREATE USER blog WITH PASSWORD 'password';"
sudo psql -U rim99 -d BlogDatabase -c "CREATE DATABASE BlogDatabase OWNER blog;"
sudo psql -U rim99 -d BlogDatabase -c "CREATE TABLE blogposts (
title varchar NOT NULL,
tag1 varchar NOT NULL,
tag2 varchar,
tag3 varchar,
content text NOT NULL,
blogID varchar NOT NULL PRIMARY KEY,
postdate timestamp,
url varchar NOT NULL);"
sudo psql -U rim99 -d BlogDatabase -c "CREATE TABLE tagInfo (
tag varchar NOT NULL PRIMARY KEY,
content text NOT NULL);"
