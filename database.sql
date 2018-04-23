create database instagram;
use instagram;
create table Posts(
    id int auto_increment not null,
    user_id int,
    photo varchar(20),
    caption varchar (200),
    created_on date,
    primary key(id)
);
create table Users(
    id int auto_increment not null,
    username varchar(40),
    password varchar(40),
    firstname varchar(30),
    lastname varchar (30),
    email varchar (40),
    location varchar(40),
    biography varchar(40),
    profile_photo varchar(40),
    joined_on date,
    primary key (id)
);
 create table Likes(
    id int auto_increment not null,
    user_id int,
    post_id int,
    primary key (id)
 );
 create table Follows(
    id int auto_increment not null,
    user_id int,
    follower_id int,
    primary key(id)
 );
