drop table if exists docs;
create table docs (
	id integer primary key autoincrement,
	title text not null,
	content text not null,
	tag_id integer,
	upvote integer,
	downvote integer
);
drop table if exists tags;
create table tags (
	id integer primary key autoincrement,
	name text not null
);
drop table if exists comments;
create table comments (
	id integer primary key autoincrement,
	doc_id integer not null,
	comment text not null
);