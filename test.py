
import numpy as np
import matplotlib.pyplot as plt
import sys
from PIL import Image

x = [ 31,  31,  32,  34,  36,  38,  32,  37,  42,  50,  58,  75,  99, 113, 125, 134, 141, 146, 149]
y = [ 0,  3,  6,  9, 12, 15, 32, 36, 46, 48, 48, 70, 86, 75, 63, 48, 33, 16,  0]

x1 = [-15, -14, -11,  -6,   0,  51,  11,  24,  39,  50,  61,  61,  66,
        71,  74,  78,  81,  85,  48]
y1 = [ 0, 11, 22, 32, 42, -1, 68, 73, 65, 65, 64, 31, 28, 25, 20, 16, 11,
        6,  0]

x2 = [-15, -14, -10,  -6,   0,   7,  11,  24,  37,  50,  61,  61,  66,
        71,  74,  78,  81,  86,  48]
y2 = [ 0, 11, 22, 32, 42, 51, 68, 73, 76, 66, 64, 32, 28, 25, 20, 16, 11,
        6,  0]


x3 = [-18, -60, -19, -16, -14, -11,  -9,  -6,  -3,   0,  13,  11,  16,
        20,  25,  30,  -1,  -1,  66]
y3 = [ 0, 10,  7,  9, 11, 14, 15, 17, 19, 78, 77, 32, 28, 24, 21, 17,  0,
        0,  0]

x4 = [-20, -20, -19, -17, -15, -13, -11,  -8,  -4,   0,   4,   7,  10,
        13,  16,  19,  22,  -1,  -2]
y4 = [ 0,  3,  7, 10, 12, 16, 20, 24, 24, 24, 25, 20, 18, 16, 13, 11,  8,
        0,  0]

# should be cars angle?
def offsetXY(obstacleX, obstacleY, vehicleX, vehicleY, theta):
    # angle in radians?
    if theta >= 0:
        outputX = vehicleX - obstacleX
    else:
        outputX = vehicleX + obstacleX

    outputY = (vehicleY * 2) + obstacleY
    
    return outputX, outputY


def fill_map( x, y, value = 255):
    
    bit_map = np.zeros((100, 100))


    xy = np.zeros(100)


    for i in range(len(x)):
        
        x_offset = x[i] + 50
        # check to see if value is in range
        if x_offset > 99 or x_offset < 0: 
            continue
        elif y[i] > 99 or y[i] < 0:
            continue

        xy[x_offset] = y[i]
        bit_map[y[i], x_offset] = 1
        #bit_map[y[i]:, x[i]] = 1
        
    print(xy)
    plt.imshow(bit_map, interpolation='none', origin = "lower")
    plt.show()

    x100 = np.arange(0,100)
    x = np.array(x) + 50
    y100 = np.interp(x100, x, y)
    plt.plot(x100, y100)
    plt.show()
    #i = Image.fromarray(bit_map, mode='1')
    #i.save('maps/test_map.png')

plt.plot(x4, y4)
plt.show()

fill_map(x4, y4)