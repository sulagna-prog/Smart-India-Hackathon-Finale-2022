import sqlite3
from tabulate import tabulate
import scanner
import datetime
import cv2
import numpy as np
from pyzbar.pyzbar import decode
import WeightValue
import testmail

# def weight():
#     curr_weight=WeightValue.weightSense()
#     cur.execute("Select gvwr from Vehicleclass where mapper_class=?" ,(vc,))
#     gvwr=cur.fetchall()
#     if (curr_weight/10)>gvwr:
#         return (1,curr_weight,gvwr)
#     else:
#         return 0
#     pass

def initialweight():
    cur.execute("Select gvwr from Vehicleclass where mapper_class=?", (vc,))
    gvwr=cur.fetchall()[0]
    return gvwr[0]
    

def scaner():
    cap = cv2.VideoCapture(0)
    while True:
        ret, frame = cap.read()
        cv2.imshow('Image', frame)
        code = cv2.waitKey(10)
        if code == ord('q'):
            break
        gray_img = cv2.cvtColor(frame,0)
        barcode = decode(gray_img)

        for obj in barcode:
            points = obj.polygon
            (x,y,w,h) = obj.rect
            pts = np.array(points, np.int32)
            pts = pts.reshape((-1, 1, 2))
            cv2.polylines(frame, [pts], True, (0, 255, 0), 3)

            barcodeData = obj.data.decode("utf-8")
            barcodeType = obj.type
            string = "Data " + str(barcodeData) + " | Type " + str(barcodeType)
        
            cv2.putText(frame, string, (x,y), cv2.FONT_HERSHEY_SIMPLEX,0.8,(255,0,0), 2)
            #print("Barcode: "+barcodeData +" | Type: "+barcodeType)
            return(barcodeData)

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

        cur.execute("Select fine_count from Fastag where fastag_id=?", (tag,))
        olcount=cur.fetchall()[0]
        #print(olcount)
        if (olcount[0]>5):
            #Call email function
            testmail.mail(regno)
            pass
    conn.commit()


conn=sqlite3.connect('Magnusa.db')
cur=conn.cursor()
while True:
#cur.execute("Select mapper_class from Vehicleclass") 
#result=cur.fetchall()
    fastag_data=scaner()
    tag=fastag_data.split(',')[0]
#tag='100'
    vc=fastag_data.split(',')[1]
    regno=fastag_data.split(',')[3]
# fine=500
# cur.execute("Insert into Fine(fastag_id) values (?)",(tag,))
# conn.commit()
    cur.execute("SELECT EXISTS(SELECT 1 FROM Fastag WHERE fastag_id=?)",(tag,))
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
            
                cur.execute("Delete from Fine Where fastag_id=?",(tag,))
                conn.commit()

                #Sreeparno's code

                addfine()
    else:
            gvwr=initialweight()
            print(gvwr)
    #overload check
        
        # overload, curr_weight, gvwr=weight()
        # if overload==1:
            addfine()
        #     percentage=100*float(curr_weight)/float(gvwr)
        #     if percentage>10:
        #         #inform authorities
        #         pass
        # else:
        #     pass
            #print("Vehicle not overloaded")
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
    #cur.close()
#print(tabulate(result, headers=['mapper class']))