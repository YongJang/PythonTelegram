select version();
use telegramdb;
drop table article;
CREATE TABLE testjob (PK_aid INT UNSIGNED PRIMARY KEY AUTO_INCREMENT, url varchar(1000) NOT NULL, tag VARCHAR(40), content TEXT, click_num INT, aType VARCHAR(40), k_group INT, pDate char(8))default character set utf8;
INSERT INTO jobs (url, high , low , title, content, click_num, aType, k_group, pDate ,meta) VALUES ('http://www.asiatoday.co.kr/view.php?key=20160503002218366','IT','인공지능','이세돌',' 9단은 지난달 인공지능 `알파고`와 대결한 이후 6전 전승 무패 행진도 이어갔다. 이날 승리로 이세돌 9단은 원성진 9단에게 상대 전적 14승 11패로 더욱 앞서나갔다. 원성진 9단은 2국과 오는 18일 3국을 모두...',0,'IT',0,'20160503','<meta content=\"한국 바이켐 연구직 경력 및 신입사원 모집 - 잡코리아\" name=\"title\"/><meta content=\"한국 바이켐 연구직 경력 및 신입사원 모집 경력 : 신입·경력, 학력 : 대졸이상, 급여 : 2,500~3,000만원, 고용형태 : 정규직, 성별 : 남자, 나이 : , 마감일 : 2016.06.02\" name=\"description\"/>');
select * from testjob;

CREATE TABLE tags (high varchar(40), low varchar(40))default character set utf8;
select * from tags;
show global variables like 'c%'; 
set character_set_client = utf8;
set character_set_connection = utf8;
set character_set_database = utf8;
set character_set_results = utf8;
set character_set_server = utf8;
set collation_connection = utf8_general_ci;
set collation_database = utf8_general_ci;
set collation_server = utf8_general_ci;
CREATE TABLE jobs(PK_aid INT UNSIGNED PRIMARY KEY AUTO_INCREMENT, url varchar(1000) NOT NULL, high VARCHAR(40), low VARCHAR(300), title TEXT, content TEXT, click_num INT, aType VARCHAR(40), k_group INT, pDate char(8), meta TEXT)default character set utf8;

CREATE TABLE society(PK_aid INT UNSIGNED PRIMARY KEY AUTO_INCREMENT, url varchar(1000) NOT NULL, high VARCHAR(40), low VARCHAR(300), title TEXT, content TEXT, click_num INT, aType VARCHAR(40), k_group INT, pDate char(8), meta TEXT)default character set utf8;

set character_set_connection=utf8;
set names utf8;
load data local infile 'E:\\PythonTelegram\\ITtags4.csv' into table tags fields terminated by ',' enclosed by '"' lines terminated by '\r\n';
load data local infile 'E:\\PythonTelegram\\SocialTags.csv' into table tags fields terminated by ',' enclosed by '"' lines terminated by '\r\n';
CREATE TABLE tags (high varchar(40), low varchar(40))default character set utf8;
select * from jobs;
select * from information;
delete from jobs where aType = 'Job';
SET SQL_SAFE_UPDATES=0;
desc jobs;


SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='TRADITIONAL';

#아래껀 아님!
DROP SCHEMA IF EXISTS `mydb` ;
CREATE SCHEMA IF NOT EXISTS `mydb` DEFAULT CHARACTER SET utf8 COLLATE utf8_general_ci ;
USE `mydb` ;
                   
SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;