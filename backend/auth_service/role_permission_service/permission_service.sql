create table permission(
    service varchar(255) not null,
    path varchar(255) not null,
    method varchar(255) not null,
    student boolean default true,
    teacher boolean default false,
    admin boolean default false
)