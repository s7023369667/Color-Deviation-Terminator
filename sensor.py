import serial
import time
import pymongo
##sensor to mongodb

def arduino_conect():
    BAUD = 9600
    #PORT = "COM5"  #windows
    PORT = '/dev/tty.usbmodem14201' #mac
    return serial.Serial(PORT, BAUD)

def main():
    time.sleep(3)
    # get arduino values
    arduino = arduino_conect()
    
    while True:
        time.sleep(0.1)
        line = arduino.readline().decode('utf-8')
        *freq, rgb, bottom = line.split()
        print(rgb, bottom)
        if bottom == '0':
            # initial
            for _ in range(50):
                time.sleep(0.1)
                line = arduino.readline().decode('utf-8')
                print('init', line)
            
            print('Start to pub')
            for _ in range(30):  # 取得第三秒數據
                time.sleep(0.1)
                line = arduino.readline().decode('utf-8')
            *freq, rgb, bottom = line.split()
            r, g, b = [int(e) for e in rgb[1:-1].split(',')]
            for _ in range(9):
                line = arduino.readline().decode('utf-8')
                *temp, t_rgb, t_bottom = line.split()
                t_r, t_g, t_b = [int(e) for e in t_rgb[1:-1].split(',')]
                r, g, b = r+t_r, g+t_g, b+t_b
            r, g, b = r//10, g//10, b//10
            data = {'R': r, 'G': g, 'B': b, 'time': time.time()}
            print('pub: r={R} g={G} b={B} time={time}'.format(**data))
            time.sleep(5)
            # pub the data to server
            USERNAME = 's7023369667'
            PASSWORD = '7023369667s'
            client = pymongo.MongoClient(f"mongodb+srv://{USERNAME}:{PASSWORD}@iot-mongodb.qsu7o.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
            db = client.pythondb
            sensor_sever_db = db.sensor_sever
            sensor_sever_db.insert_one(data)

if __name__ == '__main__':
    main()
