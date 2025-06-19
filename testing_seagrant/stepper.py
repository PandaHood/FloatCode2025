# Uses the smbus2 library to send and receive data from a Tic.
# Works on Linux with either Python 2 or Python 3.
#
# NOTE: The Tic's control mode must be "Serial / I2C / USB".
# NOTE: For reliable operation on a Raspberry Pi, enable the i2c-gpio
#   overlay and use the I2C device it provides (usually /dev/i2c-3).
# NOTE: You might nee to change the 'SMBus(3)' line below to specify the
#   correct I2C device.
# NOTE: You might need to change the 'address = 11' line below to match
#   the device number of your Tic.
 
from smbus2 import SMBus, i2c_msg 

import RPi.GPIO as GPIO
from time import sleep


class TicI2C(object):
  def __init__(self, pwm_pin=18):
    self.pwm_pin = pwm_pin

    GPIO.setmode(GPIO.BCM)  # Set's GPIO pins to BCM GPIO numbering
    GPIO.setup(self.pwm_pin, GPIO.OUT)  # Set our input pin to be an input
    self.pwm = GPIO.PWM(self.pwm_pin, 2000)
    self.pwm.start(0)

  # Sends the "Exit safe start" command.
  def exit_safe_start(self):
    command = [0x83]
    write = i2c_msg.write(self.address, command)
    self.bus.i2c_rdwr(write)
 
  # Sets the target position.
  #
  # For more information about what this command does, see the
  # "Set target position" command in the "Command reference" section of the
  # Tic user's guide.
  def set_target_position(self, target):
    self.pwm.ChangeDutyCycle(target)

 
  # Gets one or more variables from the Tic.
  def get_variables(self, offset, length):
    write = i2c_msg.write(self.address, [0xA1, offset])
    read = i2c_msg.read(self.address, length)
    self.bus.i2c_rdwr(write, read)
    return list(read)
 
  # Gets the "Current position" variable from the Tic.
  def get_current_position(self):
    b = self.get_variables(0x22, 4)
    position = b[0] + (b[1] << 8) + (b[2] << 16) + (b[3] << 24)
    if position >= (1 << 31):
      position -= (1 << 32)
    return position
  
  def move_up():
    pass

  def move_down():
    pass

