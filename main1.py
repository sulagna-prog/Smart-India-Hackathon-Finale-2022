import sqlite3
from tabulate import tabulate
import scanner
import datetime

def addfine():
    fine=20000
    cur.execute("Insert into Fine(fastag_id,amount) values (?,?)",(tag,fine,))
    cur.execute("Select fine_count from Fastag Where fastag_id=?",(tag,))
    finecount=cur.fetchall()[0]
    print(finecount)
    if(finecount==(None,)):
        cur.execute("Update Fastag set fine_count=? Where fastag_id=?",(1,tag,))
        conn.commit()

    else:
        count=finecount[0]
        cur.execute("Update Fastag set fine_count=? Where fastag_id=?",(count+1,tag,))
        conn.commit()
    conn.commit()


conn=sqlite3.connect('Magnusa.db')
cur=conn.cursor()

#cur.execute("Select mapper_class from Vehicleclass") 
#result=cur.fetchall()
fastag_data=scanner.decoder()
tag=fastag_data.split(',')[0]
#tag='100'
vc=fastag_data.split(',')[1]
regno=fastag_data.split(',')[3]
# fine=500
# cur.execute("Insert into Fine(fastag_id) values (?)",(tag,))
# conn.commit()
cur.execute("SELECT EXISTS( SELECT 1 FROM Fastag WHERE fastag_id=?)",(tag,))
fasttag_query=cur.fetchall()
if(fasttag_query[0]==(0,)):
    cur.execute("Insert into Fastag(fastag_id, vehicle_class, registration_no) values (?,?,?)",(tag,vc,regno))
    conn.commit()

#Vechicle class axle check goes here 


# cur.execute("Insert into Fine(fastag_id) values (?)",(tag,))
# conn.commit()

cur.execute("SELECT EXISTS(SELECT 1 FROM Fine WHERE fastag_id=?)",(tag,))
myresult=cur.fetchall()
if(myresult[0]==(1,)):
    cur.execute("SELECT Date FROM Fine WHERE fastag_id = ?", (tag,))
    dateresult=cur.fetchall()
    #print(dateresult)
    if(dateresult[0]==(None,)):
        cur.execute("Select amount from Fine Where fastag_id=?", (tag,))
        fineamount=cur.fetchall()[0]
        print(fineamount)
        #Deduct toll+fine
        #Display total toll in front end
        finedate=datetime.datetime.now()
        date=int(finedate.strftime("%Y%m%d%H%M%S"))
        #print(1)
        cur.execute("Update Fine set Date=? Where fastag_id=?",(date,tag,))
        conn.commit()
    
    else:
        cur.execute("Select Date from Fine Where fastag_id=?",(tag,))
        dates=cur.fetchone()
        currentdate=datetime.datetime.now()
        date=int(currentdate.strftime("%Y%m%d%H%M%S"))
        #print(date)
        #print(dates)
        final_date = (date - dates[0])
        if(final_date<100): #9000000
            print("Deducting normal toll as 24hrs not passed")
        #Usual toll
        else:
            print
            cur.execute("Delete from Fine Where fastag_id=?",(tag,))
            conn.commit()
            addfine()
else:

    #overload check
    #Sreeparno's code


    addfine()
    # fine=20000
    # cur.execute("Insert into Fine(fastag_id,amount) values (?,?)",(tag,fine,))
    # cur.execute("Select fine_count from Fastag Where fastag_id=?",(tag))
    # finecount=cur.fetchall()[0]
    # print(finecount)
    # if(finecount==None):
    #     cur.execute("Update Fastag set fine_count=? Where fastag_id=?",(1,tag,))
    #     conn.commit()

    # else:
    #     cur.execute("Update Fastag set fine_count=? Where fastag_id=?",(finecount+1,tag,))
    #     conn.commit()
    # conn.commit()
    # pass
conn.commit()
cur.close()
#print(tabulate(result, headers=['mapper class']))