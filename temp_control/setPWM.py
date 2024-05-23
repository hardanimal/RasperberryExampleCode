# encoding: utf-8

__author__ = 'Danzel.Li'

import time
import subprocess
import RPi.GPIO as GPIO

# PARAMETERS
PIN_FAN = 14
STEP_1_TEMP = 45
STEP_2_TEMP = 65
STEP_3_TEMP = 80
Hysteresis = 2
STEP_0_PWM = 0.0
STEP_1_PWM = 0.2
STEP_2_PWM = 0.6
STEP_3_PWM = 1.0
f_rise_STEP_1 = False
f_rise_STEP_2 = False
f_rise_STEP_3 = False

def _init_fan():
    GPIO.setwarnings(False)
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(PIN_FAN, GPIO.OUT)
    GPIO.output(PIN_FAN, GPIO.LOW)
    GPIO.PWM(PIN_FAN, 100)
    time.sleep(2)
    GPIO.PWM(PIN_FAN, 0)
    # PI.wiringPiSetup()
    # PI.pinMode(PIN_FAN, PI.PWM_OUTPUT)
    # PI.pwmSetMode(PI.PWM_MODE_MS)
    # PI.pwmSetClock(8)
    # PI.pwmSetRange(100)
    # PI.pwmWrite(PIN_FAN, 100)
    # time.sleep(2)
    # PI.pwmWrite(PIN_FAN, 0)

def set_pwm(temp=25.0):
    pwm = _calc_pwm(temp) * 100
    # set PWM port
    GPIO.PWM(PIN_FAN, pwm)

def _calc_pwm(temp):
    global f_rise_STEP_1
    global f_rise_STEP_2
    global f_rise_STEP_3

    rtn_pwm = STEP_0_PWM

    if temp <= (STEP_1_TEMP - Hysteresis):
        rtn_pwm = STEP_0_PWM
        f_rise_STEP_1 = False
        f_rise_STEP_2 = False
        f_rise_STEP_3 = False

    if (STEP_1_TEMP - Hysteresis) <= temp < STEP_1_TEMP:
        if f_rise_STEP_1:
            rtn_pwm = STEP_1_PWM
        else:
            rtn_pwm = STEP_0_PWM

    if STEP_1_TEMP <= temp < (STEP_2_TEMP - Hysteresis):
        rtn_pwm = STEP_1_PWM
        f_rise_STEP_1 = True
        f_rise_STEP_2 = False
        f_rise_STEP_3 = False

    if (STEP_2_TEMP - Hysteresis) <= temp < STEP_2_TEMP:
        if f_rise_STEP_2:
            rtn_pwm = STEP_2_PWM
        else:
            rtn_pwm = STEP_1_PWM

    if STEP_2_TEMP <= temp < (STEP_3_TEMP - Hysteresis):
        rtn_pwm = STEP_2_PWM
        f_rise_STEP_1 = True
        f_rise_STEP_2 = True
        f_rise_STEP_3 = False

    if (STEP_3_TEMP - Hysteresis) <= temp < STEP_3_TEMP:
        if f_rise_STEP_3:
            rtn_pwm = STEP_3_PWM
        else:
            rtn_pwm = STEP_2_PWM

    if STEP_3_TEMP <= temp:
        rtn_pwm = STEP_3_PWM
        f_rise_STEP_1 = True
        f_rise_STEP_2 = True
        f_rise_STEP_3 = True

    return rtn_pwm

_init_fan()

if __name__ == "__main__":
    temp_points = [40, 44, 45, 46, 43.6, 42, 48, 62, 63.6, 66, 64, 60, 68, 77, 79, 80, 82, 78.5, 75, 55, 35]
    for i in temp_points:
        print(i, _calc_pwm(i))
