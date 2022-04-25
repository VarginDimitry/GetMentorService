from pprint import pprint

import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

conn = psycopg2.connect(
    dbname='gms',
    user='postgres',
    password='qwe321',
    host='localhost',
    port=5432,
)
conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
cursor = conn.cursor()

if __name__ == '__main__':
    tables = ['user']
    delete_query = "DELETE FROM public.{}"

    for table in tables:
        try:
            cursor.execute(delete_query.format(table))
            cursor
        except Exception as ex:
            print(f'Cannot delete {table}')
            raise ex
        else:
            print(f"{table} deleted")

    cursor.close()
    conn.close()
