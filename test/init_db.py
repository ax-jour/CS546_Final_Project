import sqlite3

connection = sqlite3.connect('database.db')

with open('./sql_scripts/users.sql') as f:
    connection.executescript(f.read())

with open('./sql_scripts/votes.sql') as f:
    connection.executescript(f.read())

# cur = connection.cursor()

# cur.execute("INSERT INTO users (FName, LName, DOB) VALUES (?, ?, ?)",
#             ('Alex', 'Ao', '09/01/1995')
#             )

# cur.execute("INSERT INTO users (FName, LName, DOB) VALUES (?, ?, ?)",
#             ('John', 'Wick', '10/11/2002')
#             )

connection.commit()
connection.close()