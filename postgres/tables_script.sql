create table class
(
    cid       serial
        constraint cid
            primary key,
    cname     varchar,
    ccode     varchar,
    cdesc     varchar,
    term      varchar,
    years     varchar,
    cred      integer,
    csyllabus varchar
);

alter table class
    owner to excel;

create table meeting
(
    mid       serial
        constraint mid
            primary key,
    ccode     varchar,
    starttime timestamp,
    endtime   timestamp,
    cdays     varchar
);

alter table meeting
    owner to excel;

create table requisite
(
    classid integer not null
        constraint classid
            references class,
    requid  integer not null
        constraint reqid
            references class,
    prereq  boolean,
    constraint pk_cid_reqid
        primary key (classid, requid)
);

alter table requisite
    owner to excel;

create table room
(
    rid         serial
        constraint rid
            primary key,
    building    varchar,
    room_number varchar,
    capacity    integer
);

alter table room
    owner to excel;

create table section
(
    sid      serial
        constraint sid
            primary key,
    roomid   integer
        constraint roomid
            references room,
    cid      integer
        constraint cid
            references class,
    mid      integer
        constraint mid
            references meeting,
    semester varchar,
    years    varchar,
    capacity integer
);

alter table section
    owner to excel;

create table syllabus
(
    chunkid        serial
        constraint chunkid
            primary key,
    courseid       integer
        constraint courseid
            references class,
    embedding_text int2vector,
    chunk          varchar
);

alter table syllabus
    owner to excel;


