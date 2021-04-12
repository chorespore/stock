create database summer;
use summer;
create table person
(
id int auto_increment primary key,
username varchar(64) unique not null,
email varchar(120) unique not null,
password_hash varchar(128) not null,
avatar varchar(128) not null
);
insert into person values(1, "zhangsan","test12345@qq.com","passwd","avaterpath");
insert into person values(2, "lisi","12345test@qq.com","passwd","avaterpath");