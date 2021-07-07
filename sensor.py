##Goal : data from sensor to mongodb
##At : sensor.py is using in raspberry pi.
##Note : arduino.conf is used for supervising the mqtt protocol
import serial
import time
import pymongo
from heroku.Color_Deviation_Terminator.get_secret import Secret

def arduino_conect():
    BAUD = 9600
    #PORT = "COM5"  #windows
    #PORT = "/dev/ttyACM8" #raspberry pi[-][_]"[-]"[_]
    PORT = '/dev/tty.usbmodem14201' #mac
    return serial.Serial(PORT, BAUD)

def get_data(line):
    line_list = line.split()
    bottom = line_list[-1]
    rgb = (int(line_list[1]), int(line_list[3]), int(line_list[5]))
    print(rgb, bottom)
    return rgb,bottom

def main():
    #time.sleep(3)
    # get arduino values
    arduino = arduino_conect()
    
    while True:
        time.sleep(0.1)
        line = arduino.readline().decode('utf-8')
        rgb,bottom=get_data(line)
        time.sleep(0.1)
        if bottom == '0':
            print("Start initializing....")
            # initial
            for _ in range(50):
                time.sleep(0.1)
                line = arduino.readline().decode('utf-8')
                print('init',_, line)
            
            print('Start to publish.....')
            for _ in range(30):  # 取得第三秒數據
                time.sleep(0.1)
                line = arduino.readline().decode('utf-8')
            rgb, bottom = get_data(line)
            rgb=','.join([str(i) for i in rgb])
            r, g, b = [int(e) for e in rgb[:].split(',')]
            data = {'R': r, 'G': g, 'B': b, 'time': time.time()}
            print('publish: r={R} g={G} b={B} time={time}'.format(**data))
            time.sleep(5)
            # pub the data to server
            s=Secret()
            USERNAME = s.get_mongodb_userid()
            PASSWORD = s.get_mongodb_password()
            client = pymongo.MongoClient(f"mongodb+srv://{USERNAME}:{PASSWORD}@iot-mongodb.qsu7o.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            db = client.iot
            sensor_db = db.sensor
            sensor_db.insert_one(data)

if __name__ == '__main__':
    main()
