import sqlite3
from tabulate import tabulate
import scanner
import datetime

conn=sqlite3.connect('Magnusa.db')
cur=conn.cursor()

cur.execute("Select mapper_class from Vehicleclass") 
result=cur.fetchall()
fastag_data=scanner.decoder()
tag=fastag_data.split(',')[0]
fine=500
cur.execute("Insert into Fine(fastag_id) values (?)",(tag,))
conn.commit()
cur.execute("SELECT EXISTS(SELECT 1 FROM Fine WHERE fastag_id=?)",(tag,))
myresult=cur.fetchall()
# if(myresult[0]==(1,)):
#     cur.execute("SELECT Date FROM Fine WHERE fastag_id = ?", (tag,))
#     dateresult=cur.fetchall()
#     print(dateresult)
#     if(dateresult[0]==(None,)):
#         #Deduct toll+fine
#         date=str(datetime.datetime.now())
#         cur.execute("Insert into Fine(Date) values(?) WHERE fastag_id=?",(date,tag))
#         conn.commit()
#     pass
# else:
#     cur.execute("Select Date from Fine Where fastag_id=?",(tag))
#     date=cur.fetchall()
#     diff=datetime.datetime.now()-date
#     #Usual toll
#     pass
conn.commit()
cur.close()
#print(tabulate(result, headers=['mapper class']))