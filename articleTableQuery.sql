select version();
use telegramdb;
drop table article;
CREATE TABLE article (PK_aid INT UNSIGNED PRIMARY KEY AUTO_INCREMENT, url varchar(1000) NOT NULL, tag VARCHAR(40), content TEXT, click_num INT, aType VARCHAR(40), k_group INT, pDate char(8))default character set utf8;
INSERT INTO article (url, tag, content, click_num, aType, k_group, pDate) VALUES ('http://www.asiatoday.co.kr/view.php?key=20160503002218366','인공지능','이세돌 9단은 지난달 인공지능 `알파고`와 대결한 이후 6전 전승 무패 행진도 이어갔다. 이날 승리로 이세돌 9단은 원성진 9단에게 상대 전적 14승 11패로 더욱 앞서나갔다. 원성진 9단은 2국과 오는 18일 3국을 모두...',0,'IT',0,'20160503');
select * from article;
CREATE TABLE tags(high varchar(40), mid varchar(40), bottom varchar(40));
drop table tags;

/*
========================================================================================
*/
show global variables like 'c%'; 
set character_set_client = utf8;
set character_set_connection = utf8;
set character_set_database = utf8;
set character_set_results = utf8;
set character_set_server = utf8;
set collation_connection = utf8_general_ci;
set collation_database = utf8_general_ci;
set collation_server = utf8_general_ci;
/*
========================================================================================
*/
CREATE TABLE article (PK_aid INT UNSIGNED PRIMARY KEY AUTO_INCREMENT, url varchar(1000) NOT NULL, high VARCHAR(40), low VARCHAR(40), title TEXT, content TEXT, click_num INT, aType VARCHAR(40), k_group INT, pDate char(8))default character set utf8;
CREATE TABLE tags (high varchar(40), low varchar(40))default character set utf8;
set character_set_connection=utf8;
set names utf8;
load data local infile 'C:\\Users\\Administrator\\Documents\\GitHub\\PythonTelegram\\ITtags4.csv' into table tags fields terminated by ',' enclosed by '"' lines terminated by '\r\n';
load data local infile 'C:\\Users\\Administrator\\Documents\\GitHub\\PythonTelegram\\SocialTags.csv' into table tags fields terminated by ',' enclosed by '"' lines terminated by '\r\n';
CREATE TABLE tags (high varchar(40), low varchar(40))default character set utf8;
select * from tags;
/*
========================================================================================
*/
CREATE TABLE users (PK_uid INT UNSIGNED PRIMARY KEY NOT NULL, step INT UNSIGNED);
SELECT * FROM users;