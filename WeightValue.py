import serial


def weightSense():
    serialport=serial.Serial('COM3',baudrate=57600,timeout=10)
    prev=-99999999;
    ind=-1
    for i in range(1,30):

        arduinoData=serialport.readline().decode('ascii')
        print(arduinoData)
        ind = arduinoData.index("\r")
        val1 = arduinoData[:ind]

        prev=max(prev,float(val1))
    file1=open("Myfile.txt","w")
    file1.write(str(prev))


    print('Final Weight is',prev)
weightSense()