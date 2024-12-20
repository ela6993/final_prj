import sqlite3

conn = sqlite3.connect('/home/elaman/flask projects/socialnetwork/instance/appdb.db')
cursor = conn.cursor()
cursor.execute('delete from users')
conn.commit()