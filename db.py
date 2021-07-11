import os
from typing import Dict, List, Tuple

import sqlite3

conn = sqlite3.connect(os.path.join("db", "finance.db"))
cursor = conn.cursor()


def insert(table: str, column_values: Dict):
    """Inserts expenses into database"""
    columns = ', '.join(column_values.keys())
    values = [tuple(column_values.values())]
    placeholders = ', '.join("?" * len(column_values.keys()))
    cursor.executemany(
        f"INSERT INTO {table} "
        f"({columns}) "
        f"VALUES ({placeholders})",
        values)
    conn.commit()


def _init_db():
    """Inits database"""
    with open("createdb.sql", "r") as f:
        sql = f.read()
    cursor.executescript(sql)
    conn.commit()


def fetch_all(table: str, columns: List[str]) -> List[Dict]:
    """Returns list of dictionaries with name of column as a key and field of row as a value"""
    columns_joined = ", ".join(columns)
    cursor.execute(f"SELECT {columns_joined} FROM {table}")
    rows = cursor.fetchall()
    result = []
    for row in rows:
        dict_row = {}
        for index, column in enumerate(columns):
            dict_row[column] = row[index]
        result.append(dict_row)
    return result



def check_db_exists():
    """Checks if db is initialized, if no - initializes"""
    cursor.execute("SELECT name FROM sqlite_master "
                   "WHERE type='table' AND name='expense'")
    table_exist = cursor.fetchall()
    if table_exist:
        return
    _init_db()


def erase_all_tables():
    """Erases tables for their updating"""
    cursor.execute("DROP TABLE budget;"
                   "DROP TABLE expenses"
                   "DROP TABLE category")


check_db_exists()