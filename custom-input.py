import picar_4wd as fc
import sys
import tty
import termios
import asyncio


power_val = 50
key = 'status'
print("If you want to quit.Please press q")


def foward(power:int, time:int):
    fc.forward(power)
    time.sleep(time)
    fc.stop()


def test3():
    speed4 = Speed(25)
    speed4.start()
    # time.sleep(2)
    fc.forward(100)
    x = 0
    for i in range(20):
        time.sleep(0.1)
        speed = speed4()
        x += speed * 0.1
        print("%smm/s"%speed)
    print("%smm"%x)
    speed4.deinit()
    fc.stop()



def readchar():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def readkey(getchar_fn=None):
    getchar = getchar_fn or readchar
    c1 = getchar()
    if ord(c1) != 0x1b:
        return c1
    c2 = getchar()
    if ord(c2) != 0x5b:
        return c1
    c3 = getchar()
    return chr(0x10 + ord(c3) - 65)

def Keyborad_control():
    while True:
        global power_val
        key=readkey()
        if key=='6':
            if power_val <=90:
                power_val += 10
                print("power_val:",power_val)
        elif key=='4':
            if power_val >=10:
                power_val -= 10
                print("power_val:",power_val)
        if key=='w':
            foward(power_val, 1)
        elif key=='a':
            fc.turn_left(power_val)
        elif key=='s':
            fc.backward(power_val)
        elif key=='d':
            fc.turn_right(power_val)
        elif key=="3":
            test3()
        else:
            fc.stop()
        if key=='q':
            print("quit")  
            break  
if __name__ == '__main__':
    Keyborad_control()






