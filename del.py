# coding=utf-8
import subprocess as sp
import cv2
import os
import time

color = [int(e) for e in "1 2 3".split()]

with open('test/input.txt', 'w') as f:
    print(*color, file=f)

# print(color[::-1].encode(encoding="utf-8"))
# p2 = sp.Popen(['python3', 'getcolor.py'], stdout=sp.PIPE, stdin=sp.PIPE)#���͹Ϥ�

# print(color[::-1].encode(encoding="utf-8"))
# p2.stdin.write(color[::-1].encode(encoding="utf-8"))
# p2.wait() #���ݹϤ��s�y
os.system('python3 getcolor.py < input.txt')
# time.sleep(0.1)
print('color_fig/b{0}g{1}r{2}.jpg'.format(color[0], color[1], color[2]))
img = cv2.imread('color_fig/b{0}g{1}r{2}.jpg'.format(color[0], color[1], color[2]))
print(img)
# cv2.imshow('test', img)
