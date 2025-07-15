import spidev
import time
import numpy as np
#import RPi.GPIO as GPIO
import logging
from gpiozero import *

spi_freq=40000000
BL_freq =1000
i2c=None
i2c_freq=100000

width = 240
height = 240 

#GPIO Set
LCD_RST_PIN = 27 # 25
LCD_DC_PIN  = 25 # 24
LCD_BL_PIN = 24
LCD_CS_PIN  = 8

GPIO_LCD_RST_PIN = DigitalOutputDevice(LCD_RST_PIN, active_high = True, initial_value =False)
GPIO_LCD_DC_PIN  = DigitalOutputDevice(LCD_DC_PIN, active_high = True, initial_value =False)
GPIO_LCD_BL_PIN = PWMOutputDevice(LCD_BL_PIN, frequency = BL_freq)

#SPI init
SPI = spidev.SpiDev(0, 0)
SPI.max_speed_hz = spi_freq
SPI.mode = 0b00

def digital_write(Pin, value):
    if value:
        Pin.on()
    else:
        Pin.off()

def digital_read(Pin):
    return Pin.value

def delay_ms(delaytime):
    time.sleep(delaytime / 1000.0)

def spi_writebyte(data):
    if SPI!=None :
        SPI.writebytes(data)

def bl_DutyCycle(duty):
    GPIO_LCD_BL_PIN.value = duty / 100
    
def bl_Frequency(freq):# Hz
    GPIO_LCD_BL_PIN.frequency = freq
        
def module_init():
    if SPI!=None :
        SPI.max_speed_hz = spi_freq 
        SPI.mode = 0b00     
    return 0

def module_exit():
    logging.debug("spi end")
    if SPI!=None :
        SPI.close()
    
    logging.debug("gpio cleanup...")
    digital_write(GPIO_LCD_RST_PIN, 1)
    digital_write(GPIO_LCD_DC_PIN, 0)   
    GPIO_LCD_BL_PIN.close()
    time.sleep(0.001)

def command(cmd):
    digital_write(GPIO_LCD_DC_PIN, False)
    spi_writebyte([cmd])

def data(val):
    digital_write(GPIO_LCD_DC_PIN, True)
    spi_writebyte([val])

def reset():
    """Reset the display"""
    digital_write(GPIO_LCD_RST_PIN,True)
    time.sleep(0.01)
    digital_write(GPIO_LCD_RST_PIN,False)
    time.sleep(0.01)
    digital_write(GPIO_LCD_RST_PIN,True)
    time.sleep(0.01)

def Init():
    """Initialize dispaly"""  
    module_init()
    reset()

    command(0x36)
    data(0x70)                 #data(0x00)

    command(0x11)     

    time.sleep(0.12)               

    command(0x36)     
    data(0x00)   

    command(0x3A)     
    data(0x05)   

    command(0xB2)     
    data(0x0C)   
    data(0x0C)   
    data(0x00)   
    data(0x33)   
    data(0x33)   

    command(0xB7)     
    data(0x00)   

    command(0xBB)     
    data(0x3F)   

    command(0xC0)     
    data(0x2C)   

    command(0xC2)     
    data(0x01)   

    command(0xC3)     
    data(0x0D)   

    command(0xC6)     
    data(0x0F)     

    command(0xD0)     
    data(0xA7)   

    command(0xD0)     
    data(0xA4)   
    data(0xA1)   

    command(0xD6)     
    data(0xA1)   

    command(0xE0)
    data(0xF0)
    data(0x00)
    data(0x02)
    data(0x01)
    data(0x00)
    data(0x00)
    data(0x27)
    data(0x43)
    data(0x3F)
    data(0x33)
    data(0x0E)
    data(0x0E)
    data(0x26)
    data(0x2E)

    command(0xE1)
    data(0xF0)
    data(0x07)
    data(0x0D)
    data(0x0D)
    data(0x0B)
    data(0x16)
    data(0x26)
    data(0x43)
    data(0x3E)
    data(0x3F)
    data(0x19)
    data(0x19)
    data(0x31)
    data(0x3A)

    command(0x21)     

    command(0x29) 

def SetWindows(Xstart, Ystart, Xend, Yend):
    #set the X coordinates
    command(0x2A)
    data(0x00)               #Set the horizontal starting point to the high octet
    data(Xstart & 0xff)      #Set the horizontal starting point to the low octet
    data(0x00)               #Set the horizontal end to the high octet
    data((Xend - 1) & 0xff) #Set the horizontal end to the low octet 
    
    #set the Y coordinates
    command(0x2B)
    data(0x00)
    data((Ystart & 0xff))
    data(0x00)
    data((Yend - 1) & 0xff )

    command(0x2C) 
    
def ShowImage(Image):
    """Set buffer to value of Python Imaging Library image."""
    """Write display buffer to physical display"""

    if(Image == None):
        return

    imwidth, imheight = Image.size
    if imwidth > width or imheight > height:
        raise ValueError('Image must be same dimensions as display \
            ({0}x{1}).' .format(width, height))

    img = np.asarray(Image.rotate(90))
    pix = np.zeros((width,height,2), dtype = np.uint8)
    pix[...,[0]] = np.add(np.bitwise_and(img[...,[0]],0xF8),np.right_shift(img[...,[1]],5))
    pix[...,[1]] = np.add(np.bitwise_and(np.left_shift(img[...,[1]],3),0xE0),np.right_shift(img[...,[2]],3))
    pix = pix.flatten().tolist()
    SetWindows ( 0, 0, width, height)
    digital_write(GPIO_LCD_DC_PIN,True)
    for i in range(0,len(pix),4096):
        spi_writebyte(pix[i:i+4096])		

def ShowBuffer(Buffer):
    """Set buffer to value of Python Imaging Library image."""
    """Write display buffer to physical display"""
    if(Buffer == None):
        return

    #imwidth, imheight = Buffer.size
    #if imwidth > width or imheight > height:
    #    raise ValueError('Buffer must be same dimensions as display \
    #        ({0}x{1}).' .format(width, height))
    img = np.asarray(Buffer.rotate(90))
    pix = np.zeros((width,height,2), dtype = np.uint8)
    pix[...,[0]] = np.add(np.bitwise_and(img[...,[0]],0xF8),np.right_shift(img[...,[1]],5))
    pix[...,[1]] = np.add(np.bitwise_and(np.left_shift(img[...,[1]],3),0xE0),np.right_shift(img[...,[2]],3))
    pix = pix.flatten().tolist()
    SetWindows ( 0, 0, width, height)
    digital_write(GPIO_LCD_DC_PIN,True)
    for i in range(0,len(pix),4096):
        spi_writebyte(pix[i:i+4096])	
    
def clear():
    """Clear contents of image buffer"""
    _buffer = [0xff]*(width * height * 2)
    SetWindows ( 0, 0, width, height)
    digital_write(GPIO_LCD_DC_PIN,True)
    for i in range(0,len(_buffer),4096):
        spi_writebyte(_buffer[i:i+4096])