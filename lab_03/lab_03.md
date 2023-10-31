### Лабораторная работа №3

#### SQL код схемы

```
SELECT * FROM actors;

SELECT  DISTINCT(actor_first_name)
FROM actors;

SELECT DISTINCT(actor_surname) FROM actors WHERE actor_age BETWEEN '18' AND '20';

SELECT actor_surname
FROM actors
WHERE actor_sex = 'f';

SELECT actor_first_name, actor_surname
FROM actors
WHERE actor_surname LIKE '%Col%';

SELECT actor_first_name, actor_surname
FROM actors
WHERE tool_id IS NOT NULL;

SELECT actor_first_name, actor_surname, actor_age
FROM actors
ORDER BY actor_first_name ASC, actor_age DESC;

SELECT locations.location_id,
      locations.location_name,
      CONCAT(actors.actor_first_name, ' ', actors.actor_surname) AS actor_full_name
FROM locations
INNER JOIN actors ON locations.location_id = actors.location_id;


SELECT inventory.tool_id,
     inventory.tool_name,
      CONCAT(actors.actor_first_name, ' ', actors.actor_surname) AS actor_full_name
FROM inventory
RIGHT JOIN actors on inventory.tool_id = actors.tool_id;


SELECT CONCAT(actors.actor_first_name, ' ', actors.actor_surname) AS actor_full_name,
     CONCAT(creative_team_specialists.creator_name, ' ', creative_team_specialists.creator_surname) AS creative_team_specialist_full_name,
      locations.location_id  AS location
FROM actors
 LEFT JOIN creative_team_specialists ON actors.actor_id = creative_team_specialists.actor_id
      LEFT JOIN locations ON actors.actor_id = locations.location_id;


12.  SELECT inventory.tool_name, CONCAT(actors.actor_first_name, ' ', actors.actor_surname) AS actor_full_name
FROM inventory
FULL JOIN actors ON inventory.tool_id = actors.actor_id;

13.  SELECT inventory.tool_name, COUNT(actor_id)
FROM inventory
FULL JOIN actors ON inventory.tool_id = actors.actor_id
GROUP BY tool_name, actor_surname;

14. SELECT actor_full_name
FROM (SELECT inventory.tool_type,
   CONCAT(actors.actor_first_name, ' ', actors.actor_surname) AS actor_full_name
    FROM inventory
    RIGHT JOIN actors ON actors.actor_id = inventory.tool_id WHERE tool_type = 'accessory') AS t1;

15. CREATE VIEW ActorsVIEW
 AS
SELECT * FROM actors;

16. CREATE VIEW ActorsAndAccessories
AS
SELECT inventory.tool_type,
   CONCAT(actors.actor_first_name, ' ', actors.actor_surname) AS actor_full_name
    FROM inventory
    RIGHT JOIN actors ON actors.actor_id = inventory.tool_id WHERE tool_type = 'accessory'
```

### Дополнительное задание к лабораторной работе №3

#### SQL код схемы

```
ALTER TABLE "Jobs"
    ADD COLUMN IF NOT EXISTS "salary" decimal(12, 2);

SELECT *
FROM "Cells";


SELECT DISTINCT(first_name)
FROM "Prison_Staff";


SELECT *
FROM "Prisoners"
WHERE sentence_start_date BETWEEN '01/02/2019'::DATE AND '10/06/2035'::DATE;


SELECT COUNT(*)
FROM "Prison_Staff"
WHERE first_name IN ('Евгений', 'Игорь', 'Антон', 'Сергей');


SELECT DISTINCT(first_name)
FROM "Visitors"
WHERE first_name LIKE '%ми%';


SELECT *
FROM "Incidents"
WHERE description IS NOT NULL;


SELECT *
FROM "Jobs"
ORDER BY job_name ASC, job_type ASC;


SELECT "Incidents".pk_incident_id,
       "Incidents".description,
       CONCAT("Prison_Staff".first_name, ' ', "Prison_Staff".last_name) AS staff_full_name
FROM "Incidents"
         INNER JOIN "Prison_Staff" ON "Incidents".fk_staff_id = "Prison_Staff".pk_staff_id;


SELECT "Cells_Check".check_type, CONCAT("Prison_Staff".first_name, ' ', "Pri
son_Staff".last_name) AS staff_full_name
FROM "Cells_Check"
         RIGHT JOIN public."Prison_Staff" on "Prison_Staff".pk_staff_id = "Cells_Check".fk_staff_id;


SELECT CONCAT("Visitors".first_name, ' ', "Visitors".last_name)   visitor_full_name,
       CONCAT("Prisoners".first_name, ' ', "Prisoners".last_name) prisoner_full_name,
       "Prison_Visitation_Schedule".start_time                    visit_date
FROM "Visitors"
         LEFT JOIN "Prisoners" ON "Visitors".fk_prisoner_id = "Prisoners".pk_prisoner_id
         LEFT JOIN "Prison_Visitation_Schedule"
                   ON "Visitors".pk_visitor_id = "Prison_Visitation_Schedule".fk_visitor_id;


SELECT "Jobs".job_name, CONCAT("Prison_Staff".first_name, ' ', "Prison_Staff".last_name) staff_full_name
FROM "Jobs"
         FULL JOIN "Prison_Staff" ON "Jobs".pk_job_id = "Prison_Staff".fk_job_id;


SELECT "Jobs".job_name, COUNT(*) quantity
FROM "Jobs"
         FULL JOIN "Prison_Staff" ON "Jobs".pk_job_id = "Prison_Staff".fk_job_id
GROUP BY "Jobs".job_name, "Prison_Staff"."last_name";


SELECT staff_full_name
FROM (SELECT "Cells_Check".check_type,
             CONCAT("Prison_Staff".first_name, ' ', "Prison_Staff".last_name) AS staff_full_name
      FROM "Cells_Check"
               RIGHT JOIN public."Prison_Staff" on "Prison_Staff".pk_staff_id = "Cells_Check".fk_staff_id
      WHERE "Cells_Check".check_type = 'Success') a ;


CREATE VIEW Prisoners
AS
SELECT first_name, last_name
FROM "Prisoners"
WHERE date_of_birth BETWEEN '02.05.1960'::DATE AND '08.01.2004'::DATE;

CREATE VIEW Visitors
AS
SELECT CONCAT("Visitors".first_name, ' ', "Visitors".last_name)   visitor_full_name,
       CONCAT("Prisoners".first_name, ' ', "Prisoners".last_name) prisoner_full_name,
       "Prison_Visitation_Schedule".start_time                    visit_date
FROM "Visitors"
         LEFT JOIN "Prisoners" ON "Visitors".fk_prisoner_id = "Prisoners".pk_prisoner_id
         LEFT JOIN "Prison_Visitation_Schedule"
                   ON "Visitors".pk_visitor_id = "Prison_Visitation_Schedule".fk_visitor_id;
```