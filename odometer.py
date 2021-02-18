import RPi.GPIO as GPIO
import time, math
import threading
import picar_4wd as fc

class Duodometer():
    def __init__(self, pin1, pin2):
        self.tick_cm = 1.0
        self.tick_counter = 0
        self.pin1 = pin1
        self.pin2 = pin2
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(pin2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def start(self):
        GPIO.add_event_detect(self.pin1, GPIO.RISING, callback=self.gpio_callback)
        GPIO.add_event_detect(self.pin2, GPIO.RISING, callback=self.gpio_callback)

    def stop(self):
        GPIO.remove_event_detect(self.pin1)
        GPIO.remove_event_detect(self.pin2)

    def reset(self):
        self.tick_counter = 0

    def gpio_callback(self, pin):
        self.tick_counter += 1

    def __call__(self):
        return 0.5 * self.tick_counter * self.tick_cm

    def deinit(self):
        self.stop()


class Odometer():
    def __init__(self, pin):
        self.speed_counter = 0 #
        self.speed = 0
        self.last_time = 0
        self.pin = pin
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        self.timer_flag = True
        self.timer = threading.Thread(target=self.fun_timer, name="Thread1")

    def start(self):
        self.timer.start()
        # print('speed start')

    def print_result(self, s):
        print("Rising: {}; Falling: {}; High Level: {}; Low Level: {}".format(s.count("01"), s.count("10"), s.count("1"), s.count("0")))

    """"
    http://cmra.rec.ri.cmu.edu/previews/rcx_products/robotics_educator_workbook/content/mech/pages/Diameter_Distance_TraveledTEACH.pdf
    3.3 is the radius of the actual wheel in cm. Multiplied by 2 corresponds to the diameter.
    The time.sleep(0.001) in the for loop dictates the frequency of checking the pin values and hence the time over which the distance had been measured.
    So the value of self.speed is the distance in cm the wheel/car has travelled in 1sec (100 * time.sleep(0.001) * 10).
    """


    # calculates the speed
    def fun_timer(self):
        while self.timer_flag:
            l = ""
            for _ in range(100):
                l += str(GPIO.input(self.pin))
                time.sleep(0.001)
            # self.print_result(l)
            count = (l.count("01") + l.count("10")) / 2
            rps = count / 20.0 * 10
            self.speed = round(2 * math.pi * 3.3 * rps, 2)


    def deinit(self):
        self.timer_flag = False
        self.timer.join()

    def __call__(self):
        return self.speed

    def __del__(self):
        self.deinit()
