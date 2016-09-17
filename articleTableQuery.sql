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
CREATE TABLE information(PK_aid INT UNSIGNED PRIMARY KEY AUTO_INCREMENT, url varchar(250) UNIQUE KEY, high VARCHAR(20), low text, title varchar(200), content TEXT, click_num INT, a_type VARCHAR(20), k_group INT, p_date varchar(20), meta text)default character set utf8;
CREATE TABLE society(PK_aid INT UNSIGNED PRIMARY KEY AUTO_INCREMENT, url varchar(250) UNIQUE KEY, high VARCHAR(20), low text, title varchar(200), content TEXT, click_num INT, a_type VARCHAR(20), k_group INT, p_date varchar(20), meta text)default character set utf8;
CREATE TABLE jobs(PK_aid INT UNSIGNED PRIMARY KEY AUTO_INCREMENT, url varchar(250) UNIQUE KEY, high VARCHAR(20), low text, title varchar(200), content TEXT, click_num INT, a_type VARCHAR(20), k_group INT, p_date varchar(20), meta text)default character set utf8;
CREATE TABLE tags (high varchar(40), low varchar(40))default character set utf8;
set character_set_connection=utf8;
set names utf8;
DELETE FROM tags where high='IT';
DELETE FROM tags where low='CPI';
DELETE FROM tags where high='사회';
load data local infile 'D:\\Github\\PythonTelegram\\ITtags05.csv' into table tags fields terminated by ',' enclosed by '"' lines terminated by '\r\n';
load data local infile 'D:\\Github\\PythonTelegram\\Economy.csv' into table tags fields terminated by ',' enclosed by '"' lines terminated by '\r\n';
CREATE TABLE tags (high varchar(40), low varchar(40))default character set utf8;
select * from tags LIMIT 3000;
/*
========================================================================================
*/
CREATE TABLE users (PK_uid INT PRIMARY KEY NOT NULL, step INT, high INT, kgroupIT INT, kgroupEconomy INT);
SELECT * FROM users;
SET SQL_SAFE_UPDATES=0;
DELETE FROM users where step=0;
DELETE FROM information where k_group >= 0;
SELECT * FROM information;
SELECT * FROM jobs order by click_num DESC;
desc jobs;
/*
테스트 코드
//UPDATE users SET kgroupIT=5 WHERE PK_uid LIKE '2%';
*/

/*
========================================================================================
*/
SELECT * FROM jobs;
SELECT * FROM society;
SELECT * FROM jobs WHERE url = 'http://www.jobkorea.co.kr//Recruit/GI_Read/17169773?Oem_Code=C1&rPageCode=ST&PageGbn=ST' LIMIT 1;
SELECT * FROM jobs WHERE url = 'http://www.jobkorea.co.kr//Recruit/GI_Read/17169773?Oem_Code=C1' LIMIT 1;

/*
========================================================================================
*/
CREATE TABLE relationKeyword (PK_uid INT NOT NULL, keyword varchar(40), high varchar(40))default character set utf8;
SELECT * FROM relationKeyword;
SELECT * FROM tags WHERE high='경제' and low='영업관리';
Insert INTO tags(high, low) values ('경제','영업관리');
DELETE FROM tags WHERE high='경제';


CREATE TABLE relation (PK_uid INT NOT NULL, url VARCHAR(1000), k_group INT)default character set utf8;
CREATE TABLE relationIT (PK_uid INT NOT NULL, G1 INT, G2 INT, G3 INT, G4 INT, G5 INT, G6 INT, G7 INT, G8 INT, G9 INT, G10 INT, ETC INT)default character set utf8; 
CREATE TABLE relationEconomy (PK_uid INT NOT NULL, G1 INT, G2 INT, G3 INT, G4 INT, G5 INT, G6 INT, G7 INT, G8 INT, G9 INT, G10 INT, ETC INT)default character set utf8; 
CREATE TABLE shown (uid INT UNSIGNED NOT NULL, url VARCHAR(1000))default character set utf8; 
SELECT * FROM relationIT;
SELECT * FROM relationEconomy;
/*
========================================================================================
*/
SELECT * FROM information WHERE high = 'IT' ORDER BY click_num DESC, k_group ASC;
SELECT * FROM shown;
SELECT * FROM tags LIMIT 3000;

SET SQL_SAFE_UPDATES=0;
DELETE FROM shown where uid>0;
delete from jobs where url='http://www.jobkorea.co.kr//Recruit/GI_Read/18301865?Oem_Code=C1%26rPageCode=ST';


SELECT * from information;
SELECT * from information ORDER BY (k_group+10)%16 ASC,click_num DESC LIMIT 3000;
SELECT * from information ORDER BY click_num DESC LIMIT 1000;
UPDATE information SET click_num = 0 WHERE click_num > 0;
UPDATE jobs SET click_num = 0 WHERE click_num > 0;
UPDATE society SET click_num = 0 WHERE click_num > 0;


CREATE TABLE bot (name varchar(200))default character set utf8;
SELECT * from bot;

/* ALTER 대신 이걸 사용하자!!! */
desc information;
CREATE TABLE information_new (PK_aid INT UNSIGNED PRIMARY KEY AUTO_INCREMENT, url varchar(250) UNIQUE KEY, high VARCHAR(20), low text, title varchar(200), content TEXT, click_num INT, a_type VARCHAR(20), k_group INT, p_date varchar(20), meta text)default character set utf8;
INSERT INTO information_new (PK_aid, url, high, low, title, content, click_num, a_type, k_group, p_date, meta) SELECT * FROM information;
RENAME TABLE information TO information_old, information_new TO information;

SELECT * from jobs;
UPDATE society SET high = 'Society' WHERE high = ' Society ';
desc jobs;

