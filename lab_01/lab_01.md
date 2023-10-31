### Лабораторная работа №1
#### SQL код схемы
```
create schema marketing_agency;

create table marketing_agency.schedule
(
    task_id     integer not null primary key,
    task_name   varchar(50),
    task_start  timestamp,
    task_finish timestamp
);

create table marketing_agency.clients
(
    client_id    integer not null primary key,
    first_name   varchar(50),
    surname      varchar(50),
    company      varchar(50),
    email        varchar(50) unique,
    phone_number varchar(50)
);

create table marketing_agency.media_files
(
    file_id            integer not null primary key,
    file_name          varchar(50),
    file_type          varchar(10),
    file_creation_date timestamp,
    file_path          varchar(100) unique
);

create table marketing_agency.filming_equipment
(
    equipment_id          integer not null primary key,
    equipment_name        varchar(80),
    equipment_type        varchar(50),
    equipment_price       numeric(13, 4)
);

create table marketing_agency.inventory
(
    tool_id          integer not null primary key,
    tool_name        varchar(80),
    tool_type        varchar(50),
    tool_property    varchar(50),
    tool_price       numeric(13, 4)
);

create table marketing_agency.actors
(
    actor_id             integer not null primary key,
    actor_first_name     varchar(50),
    actor_surname        varchar(50),
    actor_sex            varchar(6),
    actor_age            varchar(3),
    actor_specialization varchar(50),
    actor_email          varchar(50),
    actor_phone          varchar(50)
);

create table marketing_agency.creative_team_specialists
(
    creator_id             integer not null primary key,
    creator_name           varchar(50),
    creator_surname        varchar(50),
    creator_sex            varchar(6),
    creator_age            varchar(3),
    creator_specialization varchar(50),
    creator_email          varchar(50),
    creator_phone          varchar(50)
);

create table marketing_agency.production_centre
(
    production_centre_id             integer not null primary key,
    production_centre_name           varchar(50),
    production_centre_address        varchar(100),
    production_centre_town           varchar(50),
    production_centre_country        varchar(50),
    production_centre_contact_person varchar(100),
    production_centre_email          varchar(50),
    production_centre_phone          varchar(50)
);

create table marketing_agency.locations
(
    location_id            integer not null primary key,
    location_name          varchar(50),
    location_address       varchar(120),
    location_town          varchar(50),
    location_country       varchar(50),
    location_accessibility varchar(50)
);

create table marketing_agency.marketing_brief
(
    brief_id              integer not null primary key,
    brief_aim             varchar(256),
    brief_target_audience varchar(100),
    brief_budget          numeric(13, 2),
    brief_deadline        timestamp
);
```
#### IDEF1 схема
(картинка)