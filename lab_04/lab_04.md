### Лабораторная работа №4

#### SQL код схемы

1) Транзакция

```
BEGIN;
UPDATE schedule
SET task_start = '2023-10-24 20:00:00'::TIMESTAMP
WHERE task_id = 24;
SAVEPOINT old_schedule;
DELETE FROM media_files WHERE file_id = 52;
ROLLBACK to old_schedule;
COMMIT;
```

2) Триггер

```
CREATE OR REPLACE FUNCTION delete_actor_after_tool_delete()
    RETURNS TRIGGER AS $$
BEGIN
    DELETE FROM actors WHERE actors.tool_id = OLD.tool_id;
    RETURN OLD;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER after_delete_tool
    AFTER DELETE ON inventory
    FOR EACH ROW
EXECUTE FUNCTION delete_actor_after_tool_delete();
```