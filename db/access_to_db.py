import sqlite3
con = sqlite3.connect("finance.db")
cursor = con.cursor()
cursor.execute("SELECT * FROM expense")

print(cursor.fetchall())
