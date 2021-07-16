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
    """Initialises database"""
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


def delete(table: str, row_id: int) -> None:
    """Deletes row by it's id"""
    cursor.execute(
        f"DELETE FROM {table} WHERE id={row_id}"
    )
    conn.commit()


def get_today_expenses() -> str:
    """Returns sum of today expenses"""
    cursor.execute("SELECT SUM(amount)"
                   "FROM expense WHERE DATE(created)=DATE('now', 'localtime')")
    res = cursor.fetchone()
    if res[0]:
        return res[0]
    return "0"


def get_today_base_expenses():
    """Returns sum of today base expenses"""
    cursor.execute("SELECT SUM(amount) FROM expense WHERE DATE(created)=DATE('now', 'localtime') AND category_codename in (SELECT codename FROM category WHERE is_base_expense=true)")
    res = cursor.fetchone()
    if res[0]:
        return res[0]
    return "0"


def get_month_expenses(first_day_of_month: str):
    """Returns sum of expenses of this month"""
    cursor.execute(f"SELECT SUM(amount) FROM expense WHERE DATE(created) >= '{first_day_of_month}'")
    res = cursor.fetchone()
    if res[0]:
        return res[0]
    return "0"


def get_month_base_expenses(first_day_of_month: str):
    """Returns sum of base expenses of this month"""
    cursor.execute(f"SELECT SUM(amount) FROM expense WHERE DATE(created) >= '{first_day_of_month}' AND category_codename in (SELECT codename FROM category WHERE is_base_expense=true)")
    res = cursor.fetchone()
    if res[0]:
        return res[0]
    return "0"


check_db_exists()
