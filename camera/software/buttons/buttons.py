# https://raspberrypihq.com/use-a-push-button-with-raspberry-pi-gpio/

import RPi.GPIO as GPIO
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

    # already set as BCM by OLED

    GPIO.setmode(KEY_UP_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # UP
    GPIO.setmode(KEY_LEFT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # LEFT
    GPIO.setmode(KEY_PRESS_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # CENTER
    GPIO.setmode(KEY_RIGHT_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # RIGHT
    GPIO.setmode(KEY_DOWN_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # DOWN
    GPIO.setmode(KEY1_PIN, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # BACK
    GPIO.setmode(SHUTTER, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)  # SHUTTER

  def start(self):
    Thread(target=self.listen).start()

  # listen for input
  def listen(self):
    while True:
      if self.exit: return False

      if GPIO.input(KEY_UP_PIN) == GPIO.HIGH:
        self.callback("UP")
      if GPIO.input(KEY_LEFT_PIN) == GPIO.HIGH:
        self.callback("LEFT")
      if GPIO.input(KEY_PRESS_PIN) == GPIO.HIGH:
        self.callback("CENTER")
      if GPIO.input(KEY_RIGHT_PIN) == GPIO.HIGH:
        self.callback("RIGHT")
      if GPIO.input(KEY_DOWN_PIN) == GPIO.HIGH:
        self.callback("DOWN")
      if GPIO.input(KEY1_PIN) == GPIO.HIGH:
        self.callback("BACK")
      if GPIO.input(SHUTTER) == GPIO.HIGH:
        self.callback("SHUTTER")

      time.sleep(0.1)
