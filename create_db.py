import sqlite3

conn = sqlite3.connect('collection.db')

conn.execute("CREATE TABLE words(id INTEGER PRIMARY KEY AUTOINCREMENT, word TEXT NOT NULL, meaning TEXT NOT NULL, mnemonic TEXT NOT NULL);")

conn.commit()

conn.close()
