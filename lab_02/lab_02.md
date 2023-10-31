### Лабораторная работа №2

#### SQL код схемы

```
INSERT INTO media_files(file_id, file_name, file_type, file_creation_date, file_path)
VALUES (1, 'lanadelrey', 'mp3', '07/21/2004'::timestamp, 'Desktop/lanadelrey.mp3');

INSERT INTO inventory(TOOL_ID, TOOL_NAME, TOOL_TYPE, TOOL_PROPERTY, TOOL_PRICE) values (1, 'sword', 'weapon', 'Kirishka', 123);

INSERT INTO inventory(TOOL_ID, TOOL_NAME, TOOL_TYPE, TOOL_PROPERTY, TOOL_PRICE) values (2, 'kirka', 'weapon', 'Olga', 224);

INSERT INTO inventory(TOOL_ID, TOOL_NAME, TOOL_TYPE, TOOL_PROPERTY, TOOL_PRICE) values (3, 'dessert eagle', 'weapon', 'Katya', 301);

INSERT INTO schedule(task_id, task_name, task_start, task_finish) VALUES (1, 'find Ariana Grande ASAP', '07/21/2004'::date, '08/21/2005'::date);

INSERT INTO schedule(task_id, task_name, task_start, task_finish) VALUES (1, 'buy bunnies', '05/25/2012'::date, '07/21/2012'::date);

INSERT INTO schedule(task_id, task_name, task_start, task_finish) VALUES (2, 'find HONEYMOON', '09/13/2023'::date, '09/14/2023'::date);

INSERT INTO filming_equipment(equipment_id, equipment_name, equipment_type, equipment_price) VALUES ('1', 'karaganda', 'camera', 334048);

INSERT INTO filming_equipment(equipment_id, equipment_name, equipment_type, equipment_price) VALUES ('2', 'CANON 50D', 'camera', 54804);

INSERT INTO filming_equipment(equipment_id, equipment_name, equipment_type, equipment_price) VALUES ('3', 'FUJI 23S', 'camera', 1236);
INSERT INTO marketing_brief (brief_aim, brief_target_audience, brief_budget, brief_deadline) VALUES ('promotion', 'Angry customers', 10.24, '06/23/2024'::DATE);

INSERT INTO marketing_brief (brief_aim, brief_target_audience, brief_budget, brief_deadline) VALUES ('promotion', 'Angry customers', 10.24, '24/06/2024'::DATE);

INSERT INTO actors (actor_first_name, actor_surname, actor_sex, actor_age, actor_specialization, actor_email,
                   actor_phone)
VALUES ('Mabel', 'Arnold', 'f', '3', 'family', NULL, NULL);

INSERT INTO media_files (file_id, file_name, file_type, file_creation_date, file_path)
VALUES (1, 'taylorswift', 'mp3', '12/15/2023'::date, 'Desktop/taylorswift.mp3');

INSERT INTO media_files (file_id, file_name, file_type, file_creation_date, file_path)
VALUES (3, 'meow', 'jpeg', '09/19/2023 14:55:23'::timestamp, '/opt/meow.jpef');

INSERT INTO clients (client_id, first_name, surname, company, email, phone_number)
VALUES (1, 'Elizabeth', 'Grant', 'Spotify', 'lanadelrey@god.com', '79049241195');

INSERT INTO clients (client_id, first_name, surname, company, email, phone_number)
VALUES (2, 'Ariana', 'Grande', 'Apple music', 'arianawhatareyoudoing@here.com', '88005553535');

INSERT INTO clients (client_id, first_name, surname, company, email, phone_number)
VALUES (3, 'Otis', 'Presley', 'SRE', 'otis_psychologist@netlifx.org', '2323950155352');

INSERT INTO locations VALUES (1, 'Lake Grizzly', '363415 Bukngiham road', 'Yale', 'USA', 'by car');

INSERT INTO locations VALUES (2, 'Black castle', '234665 Meowmeow avenue', 'New York', 'USA', 'by public transport');

INSERT INTO locations VALUES (3, 'Hedgehog House', '545462 Antonio street', 'Moscow', 'Russia', 'by car');

UPDATE actors
SET actor_first_name = 'Balenciaga'
WHERE actor_id = 32;

UPDATE clients
SET first_name = 'Barbie'
WHERE client_id = 21;

UPDATE clients
SET first_name = 'Cameron'
WHERE client_id = 34;

UPDATE actors
SET actor_first_name = 'Bebe'
WHERE actor_id = 2;

UPDATE creative_team_specialists
SET creator_name = 'Kirishka'
WHERE creator_id = 2;

DELETE FROM actors WHERE actor_id = 66;

DELETE FROM inventory WHERE tool_price BETWEEN 100 AND 101;

DELETE FROM locations WHERE location_town = 'Saint Pet.';

DELETE FROM media_files WHERE file_path like '/opt/%s';

DELETE FROM schedule WHERE task_start BETWEEN '06/12/2023'::DATE AND '06/24/2023'::DATE;
```