# https://raspberrypihq.com/use-a-push-button-with-raspberry-pi-gpio/

#import RPi.GPIO as GPIO
from gpiozero import *
import time

from threading import Thread

#GPIO define
KEY_UP_PIN     = 19
KEY_DOWN_PIN   = 6
KEY_LEFT_PIN   = 26
KEY_RIGHT_PIN  = 5
KEY_PRESS_PIN  = 13

KEY1_PIN       = 21
KEY2_PIN       = 20
KEY3_PIN       = 16

SHUTTER        = 22

class Buttons():
  def __init__(self, main):
    self.exit = False
    self.callback = main.button_pressed

    self.GPIO_KEY_UP_PIN = DigitalInputDevice(KEY_UP_PIN, pull_up=True, active_state=None)
    self.GPIO_KEY_DOWN_PIN = DigitalInputDevice(KEY_DOWN_PIN, pull_up=True, active_state=None)
    self.GPIO_KEY_LEFT_PIN = DigitalInputDevice(KEY_LEFT_PIN, pull_up=True, active_state=None)
    self.GPIO_KEY_RIGHT_PIN = DigitalInputDevice(KEY_RIGHT_PIN, pull_up=True, active_state=None)
    self.GPIO_KEY_PRESS_PIN = DigitalInputDevice(KEY_PRESS_PIN, pull_up=True, active_state=None)

    self.GPIO_KEY1_PIN = DigitalInputDevice(KEY1_PIN, pull_up=True, active_state=None)
    self.GPIO_KEY2_PIN = DigitalInputDevice(KEY2_PIN, pull_up=True, active_state=None)
    self.GPIO_KEY3_PIN = DigitalInputDevice(KEY3_PIN, pull_up=True, active_state=None)

    self.GPIO_SHUTTER = DigitalInputDevice(SHUTTER, pull_up=True, active_state=None)

  def start(self):
    Thread(target=self.listen).start()

  # listen for input
  def listen(self):
    while True:
      if self.exit: return False

      if self.GPIO_KEY_UP_PIN.value == 1:
        self.callback("UP")
      if self.GPIO_KEY_LEFT_PIN.value == 1:
        self.callback("LEFT")
      if self.GPIO_KEY_PRESS_PIN.value == 1:
        self.callback("CENTER")
      if self.GPIO_KEY_RIGHT_PIN.value == 1:
        self.callback("RIGHT")
      if self.GPIO_KEY_DOWN_PIN.value == 1:
        self.callback("DOWN")
      if self.GPIO_KEY1_PIN.value == 1:
        self.callback("BACK")
      if self.GPIO_SHUTTER.value == 1:
        self.callback("SHUTTER")

      time.sleep(0.1)
