import pymongo
import math
import numpy as np


def ColorDistance(rgb_1, rgb_2):  # calculate RGB dis directly
    B_1, G_1, R_1 = rgb_1
    B_2, G_2, R_2 = rgb_2
    rmean = (R_1 + R_2) / 2
    R = R_1 - R_2
    G = G_1 - G_2
    B = B_1 - B_2
    return math.sqrt((2 + rmean / 256) * (R ** 2) + 4 * (G ** 2) + (2 + (255 - rmean) / 256) * (B ** 2))


# region support function
# RGB2XYZ space transform matrix
M = np.array([[0.412453, 0.357580, 0.180423],
              [0.212671, 0.715160, 0.072169],
              [0.019334, 0.119193, 0.950227]])


# im_channel(range:[0, 1])
def f(im_channel):
    return np.power(im_channel, 1 / 3) if im_channel > 0.008856 else 7.787 * im_channel + 0.137931


def anti_f(im_channel):
    return np.power(im_channel, 3) if im_channel > 0.206893 else (im_channel - 0.137931) / 7.787
# endregion


def RGB2Lab(pixel):  # input B G R
    # rgb -> xyz
    b, g, r = pixel[0], pixel[1], pixel[2]
    rgb = np.array([r, g, b])
    XYZ = np.dot(M, rgb.T)
    XYZ /= 255
    xyz = (XYZ[0] / 0.95047, XYZ[1] / 1.0, XYZ[2] / 1.08883)

    # xyz -> Lab
    F_XYZ = [f(x) for x in xyz]
    L = 116 * F_XYZ[1] - 16 if xyz[1] > 0.008856 else 903.3 * xyz[1]
    a = 500 * (F_XYZ[0] - F_XYZ[1])
    b = 200 * (F_XYZ[1] - F_XYZ[2])
    return L, a, b


def Lab2RGB(Lab):
    fY = (Lab[0] + 16.0) / 116.0
    fX = Lab[1] / 500.0 + fY
    fZ = fY - Lab[2] / 200.0
    x = anti_f(fX)
    y = anti_f(fY)
    z = anti_f(fZ)

    xyz = np.array((x * 0.95047, y * 1.0, z * 1.0883))
    xyz *= 255
    rgb = np.dot(np.linalg.inv(M), xyz.T)
    # rgb = rgb * 255
    rgb = np.uint8(np.clip(rgb, 0, 255))
    return rgb


def cmp(rgb1, rgb2):  # test, simple
    lab1, lab2 = RGB2Lab(rgb1), RGB2Lab(rgb2)
    label = ['L_dis', 'a_dis', 'b_dis']
    result = [['bright', 'dark'], ['red', 'green'], ['yellow', 'blue']]
    e = 0
    value = []
    for i in range(3):
        dis = lab1[i]-lab2[i]
        value.append(lab2[i] - dis)  # that ideal_value add dis
        print("{0}: {1:.2f}".format(label[i], dis), end=' ')
        if dis > 0:
            print('(too {0})'.format(result[i][0]))
        elif dis < 0:
            print('(too {0})'.format(result[i][1]))
        e += abs(dis)
    print("color dis(lab): {0:.2f}".format(e/2))
    return Lab2RGB(value)


def main():
    USERNAME = 's7023369667'
    PASSWORD = '7023369667s'
    client = pymongo.MongoClient(f"mongodb+srv://{USERNAME}:{PASSWORD}@iot-mongodb.qsu7o.mongodb.net/myFirstDatabase?retryWrites=true&w=majority")
    mydb = client.iot
    linetable = mydb['line_sever']

    query = {'userID': input()}  # get by app.py
    result = list(linetable.find(query))
    if result:  # find user input
        ideal = max(result, key=lambda x: float(x["time"]))
        print("ATTTT")
        sensortable = mydb["sensor_sever"]
        result = list(sensortable.find())
        if result:  # find sensor input
            real = max(result, key=lambda x: float(x["time"]))
            i_rgb = tuple(map(float, (ideal['B'], ideal['G'], ideal['R'])))
            r_rgb = tuple(map(float, (real['B'], real['G'], real['R'])))
            print('{0} {1} {2}'.format(real['R'], real['G'], real['B']))
            print('Suggestion(RGB): ({0}, {1}, {2})'.format(*cmp(r_rgb, i_rgb)))
            # finish -> delete data
            # linetable.delete_many(query)
            # sensortable.delete_many()
        else:
            print('no sensor input!')
    else:
        print('no user input!')


if __name__ == "__main__":
    main()
