import sqlite3 as sql
import pandas as pd

from config import settings


con = sql.connect(settings.database_file_name)
cur = con.cursor()

# создание таблиц
with open('create.sql') as f:
    cur.executescript(f.read())
con.commit()


async def get_user_info(tg_id):
    cur.execute(f"SELECT * FROM users WHERE tg_id = {tg_id}")
    return cur.fetchone()


async def set_user_info(tg_id, name, age):
    req = f"UPDATE users SET name = ?, age = ? WHERE tg_id = {tg_id}"
    cur.execute(req, (name, age))
    con.commit()


async def add_user(tg_id):
    cur.execute(f"SELECT * FROM users WHERE tg_id = {tg_id}")
    rows = cur.fetchall()
    if len(rows) == 0:
        cur.execute(f"INSERT INTO users VALUES ('{tg_id}', '?', 0)")
        con.commit()


async def all_users(table='users', names=None, chunk_size=None):

    # Select all columns by default:
    if names is None:
        names_str = '*'
    else:
        names_str = ','.join(names)

    try:
        if chunk_size is None:
            query = 'select %s from %s' % (names_str, table)
            done = False
            while True:
                if not done:
                    result = pd.read_sql(query, con=con)
                    done = True
                    yield result['tg_id'].to_list()
                else:
                    raise StopIteration
        else:
            offset = 0
            while True:
                query = 'select %s from %s limit %i offset %i' % (names_str, table, chunk_size, offset)
                result = pd.read_sql(query, con=con)
                result.index = range(offset, offset+len(result))
                if len(result):
                    yield result['tg_id'].to_list()
                else:
                    raise StopIteration
                offset += chunk_size
    except StopIteration:
        return