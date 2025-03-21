create table users
(
	user_id SMALLSERIAL primary key,
	passwrd varchar(128) not null,
	status varchar(128) not null,
	first_name varchar(128),
	phone_number varchar(128),
	mail varchar(128)
);

create table teacher
(
	teacher_id SMALLSERIAL primary key,
	user_id SMALLSERIAL,
	foreign key (user_id) references users(user_id)
);

create table global_mark
(
	global_mark_id SMALLSERIAL primary key,
	mark varchar(128),
	dates date
);

create table pz
(
	pz_id SMALLSERIAL primary key,
	state text
);

create table rspz
(
	rspz_id SMALLSERIAL primary key,
	state text
);

create table works
(
	work_id SMALLSERIAL primary key,
	pz_id SMALLSERIAL,
	rspz_id SMALLSERIAL,
	comm text,
	mark varchar(128),
	foreign key (pz_id) references pz(pz_id),
	foreign key (rspz_id) references rspz(rspz_id)
);

create table task
(
	task_id SMALLSERIAL primary key,
	global_mark_id SMALLSERIAL,
	work_id SMALLSERIAL,
	state text not null,
	foreign key (global_mark_id) references global_mark(global_mark_id),
	foreign key (work_id) references works(work_id)
);

create table student
(
	student_id SMALLSERIAL primary key,
	user_id SMALLSERIAL,
	teacher_id SMALLSERIAL,
	task_id SMALLSERIAL,
	number_group varchar(128),
	foreign key (user_id) references users(user_id),
	foreign key (teacher_id) references teacher(teacher_id),
	foreign key (task_id) references task(task_id)
);

create table admins
(
	admin_id SMALLSERIAL primary key,
	user_id SMALLSERIAL,
	foreign key (user_id) references users(user_id)
);

