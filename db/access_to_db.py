import sqlite3
import pytz
import datetime
con = sqlite3.connect("finance.db")
cursor = con.cursor()
tz = pytz.timezone("Europe/Moscow")
now = datetime.datetime.now(tz).strftime("%Y-%m-%d %H:%M:%S")
cursor.execute(f"SELECT sum(amount) FROM expense WHERE date(created)=date('now', 'localtime') AND category_codename in (SELECT codename FROM category WHERE is_base_expense=true)")

print(cursor.fetchall())
