import datetime
import sqlite3

day = str(datetime.datetime.now().day)
month = str(datetime.datetime.now().month)

filename = day + "-" + month + ".csv"

file = open(filename, "w")

conn = sqlite3.connect('collection.db')

cursor = conn.execute("SELECT * FROM words")

values = []

for c in cursor:
    values.append(c)

print(values)

for value in values:
    file.write(str(value[0]).replace(",", "") + "," + value[1].replace(",", "") + "," + value[2].replace(",", "") + "\n")

conn.execute("DELETE FROM words")

conn.commit()

conn.close()
file.close()
