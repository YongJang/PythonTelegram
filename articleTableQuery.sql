use telegramdb;
drop table article;
CREATE TABLE article (PK_aid INT UNSIGNED PRIMARY KEY AUTO_INCREMENT, url varchar(1000) NOT NULL, tag VARCHAR(40), content TEXT, click_num INT, type VARCHAR(40), k_group INT, pDate char(8));