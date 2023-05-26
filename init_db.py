import sqlite3

connection = sqlite3.connect('magnusa.db')


# with open('schema.sql') as f:
#     connection.executescript(f.read())

cur = connection.cursor()

# cur.execute("INSERT INTO Vehicleclass  (mapper_class, class, axle_count) VALUES (?, ?, ?)",
#             ('VC555', '555' , 2)
#             )

# cur.execute("INSERT INTO posts (title, content) VALUES (?, ?)",
#             ('Second Post', 'Content for the second post')
#             )

connection.commit()
connection.close()