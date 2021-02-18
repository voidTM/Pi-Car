import RPi.GPIO as GPIO
import time, math
import threading
import picar_4wd as fc

"""A helper module to calculate the distance travelled of the PiCar-4WD."""

import math

from RPi import GPIO

# based on code from Frank Blechschmidt and Matt Williamson 
class Duodometer(object):

    """Calculates the travelled distance based on the car's photo interrupters.

    The PiCar-4WD uses a photo interrupter in combination with black wheels
    with punched holes as mechanism to measure distance.
    Counting the transitions from hole to non-hole (and vice versa) provides an
    approximation of the car's travelled distance.

    Attributes:
        counter: An integer count of the observed transitions.
        pin1: An integer for the first GPIO pin of the photo interrupter.
        pin2: An integer for the second GPIO pin of the photo interrupter.
        slippage_multiplier: An optional multiplier to account for slippage.
    """

    # Divisor for the counter representing: 2 pins * 2 transition types
    divisor = 4
    # Amount of transitions from from hole to non-hole (and vice versa) that
    # represent one full wheel revolution
    transitions_per_revolution = 20
    # diameter of the actual wheel in CM
    wheel_diameter = 6.6

    # slippage is around 1.7-2 on carpet
    def __init__(self, pin1: int, pin2: int, slippage_multiplier: float = 1.0):
        """Initialize attributes and set up GPIO interaction.

        Args:
            pin1:
                An integer for the first GPIO pin of the photo interrupter.
            pin2:
                An integer for the second GPIO pin of the photo interrupter.
            pin2:
                An optional multiplier to account for slippage.
        """
        self.counter = 0
        self.pin1 = pin1
        self.pin2 = pin2
        self.multiplier = slippage_multiplier
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(pin1, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
        GPIO.setup(pin2, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    @property
    def distance(self):
        """Return current distance based on counted GPIO transitions.

        Returns:
            A float representing the travelled distance in cm.
        """
        avg_wheel_revolutions = (
            self.counter / self.divisor / self.transitions_per_revolution
        )
        wheel_circumference = self.wheel_diameter * math.pi
        return wheel_circumference * avg_wheel_revolutions * self.multiplier

    def start(self):
        """Register for GPIO events of the photo interrupter."""
        GPIO.add_event_detect(
            #self.pin1, GPIO.BOTH, callback=self._gpio_callback,
            self.pin1, GPIO.BOTH, callback=self._gpio_callback,
        )
        GPIO.add_event_detect(
            self.pin2, GPIO.BOTH, callback=self._gpio_callback,
        )

    def reset(self):
        """Reset internal transition counter."""
        self.counter = 0

    def stop(self):
        """Unregister for GPIO events of the photo interrupter."""
        GPIO.remove_event_detect(self.pin1)
        GPIO.remove_event_detect(self.pin2)

    def _gpio_callback(self, pin: int):
        """Increments counter for observed transitions.

        Args:
            pin:
                GPIO pin with observed transition (ignored).
        """
        self.counter += 1

    def __del__(self):
        self.stop()


