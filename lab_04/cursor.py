from lab_02.bonus_task.credentials import HOST, USER, PASSWORD, PORT, DBNAME
import psycopg2


def connect(
    database: str, host: str, username: str, password: str, port: int = 5432
) -> tuple[psycopg2.extensions.connection, psycopg2.extensions.cursor] | None:
    """
    This function makes connection with database
    :return: tuple with connector and cursor
    """
    try:
        con = psycopg2.connect(
            dbname=database,
            user=username,
            password=password,
            port=port,
            host=host,
        )
        cur = con.cursor()
        con.set_session(autocommit=True)
        return con, cur
    except Exception as connection_error:
        print(f'The error is: {str(connection_error)}')
        return None


con, cur = connect(
    database=DBNAME, host=HOST, username=USER, password=PASSWORD
)
cur.execute(
    'SELECT equipment_id, equipment_price FROM filming_equipment WHERE equipment_price < 600;'
)

for row in tuple(cur.fetchall()):
    cur.execute(
        'UPDATE filming_equipment SET equipment_price = equipment_price + 1.1 WHERE equipment_id = %s',
        (str(row[0]),),
    )
