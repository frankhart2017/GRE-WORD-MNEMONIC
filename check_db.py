import sqlite3

conn = sqlite3.connect('collection.db')

cursor = conn.execute("SELECT * FROM words")

for c in cursor:
    print(c)

conn.close()
