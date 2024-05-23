# encoding: utf-8

__author__ = 'Danzel.Li'

import os
import time

from thermal_sensor import read_cpu_temp
from setPWM import set_pwm

def temp_control():
    while(True):
        set_pwm(read_cpu_temp())
        time.sleep(1)

if __name__ == "__main__":
    temp_control()
