
import time
from .config import RaspberryPi

class ST7789(RaspberryPi):

    width = 240
    height = 240 
    def command(self, cmd):
        self.digital_write(self.GPIO_DC_PIN, False)
        self.spi_writebyte([cmd])      
    def data(self, val):
        self.digital_write(self.GPIO_DC_PIN, True)
        self.spi_writebyte([val])

    def reset(self):
        """Reset the display"""
        self.digital_write(self.GPIO_RST_PIN,True)
        time.sleep(0.01)
        self.digital_write(self.GPIO_RST_PIN,False)
        time.sleep(0.01)
        self.digital_write(self.GPIO_RST_PIN,True)
        time.sleep(0.01)
    def Init(self):
        """Initialize dispaly"""  
        self.module_init()
        self.reset()

        self.command(0x36)
        self.data(0x70)                 #self.data(0x00)

        self.command(0x11)     

        time.sleep(0.12)               

        self.command(0x36)     
        self.data(0x00)   

        self.command(0x3A)     
        self.data(0x05)   

        self.command(0xB2)     
        self.data(0x0C)   
        self.data(0x0C)   
        self.data(0x00)   
        self.data(0x33)   
        self.data(0x33)   

        self.command(0xB7)     
        self.data(0x00)   

        self.command(0xBB)     
        self.data(0x3F)   

        self.command(0xC0)     
        self.data(0x2C)   

        self.command(0xC2)     
        self.data(0x01)   

        self.command(0xC3)     
        self.data(0x0D)   

        self.command(0xC6)     
        self.data(0x0F)     

        self.command(0xD0)     
        self.data(0xA7)   

        self.command(0xD0)     
        self.data(0xA4)   
        self.data(0xA1)   

        self.command(0xD6)     
        self.data(0xA1)   

        self.command(0xE0)
        self.data(0xF0)
        self.data(0x00)
        self.data(0x02)
        self.data(0x01)
        self.data(0x00)
        self.data(0x00)
        self.data(0x27)
        self.data(0x43)
        self.data(0x3F)
        self.data(0x33)
        self.data(0x0E)
        self.data(0x0E)
        self.data(0x26)
        self.data(0x2E)

        self.command(0xE1)
        self.data(0xF0)
        self.data(0x07)
        self.data(0x0D)
        self.data(0x0D)
        self.data(0x0B)
        self.data(0x16)
        self.data(0x26)
        self.data(0x43)
        self.data(0x3E)
        self.data(0x3F)
        self.data(0x19)
        self.data(0x19)
        self.data(0x31)
        self.data(0x3A)

        self.command(0x21)     

        self.command(0x29) 
  
    def SetWindows(self, Xstart, Ystart, Xend, Yend):
        #set the X coordinates
        self.command(0x2A)
        self.data(0x00)               #Set the horizontal starting point to the high octet
        self.data(Xstart & 0xff)      #Set the horizontal starting point to the low octet
        self.data(0x00)               #Set the horizontal end to the high octet
        self.data((Xend - 1) & 0xff) #Set the horizontal end to the low octet 
        
        #set the Y coordinates
        self.command(0x2B)
        self.data(0x00)
        self.data((Ystart & 0xff))
        self.data(0x00)
        self.data((Yend - 1) & 0xff )

        self.command(0x2C) 
        
    def ShowImage(self,Image):
        """Set buffer to value of Python Imaging Library image."""
        """Write display buffer to physical display"""
        imwidth, imheight = Image.size
        if imwidth > self.width or imheight > self.height:
            raise ValueError('Image must be same dimensions as display \
                ({0}x{1}).' .format(self.width, self.height))
        img = self.np.asarray(Image)
        pix = self.np.zeros((self.width,self.height,2), dtype = self.np.uint8)
        pix[...,[0]] = self.np.add(self.np.bitwise_and(img[...,[0]],0xF8),self.np.right_shift(img[...,[1]],5))
        pix[...,[1]] = self.np.add(self.np.bitwise_and(self.np.left_shift(img[...,[1]],3),0xE0),self.np.right_shift(img[...,[2]],3))
        pix = pix.flatten().tolist()
        self.SetWindows ( 0, 0, self.width, self.height)
        self.digital_write(self.GPIO_DC_PIN,True)
        for i in range(0,len(pix),4096):
            self.spi_writebyte(pix[i:i+4096])		

    def ShowBuffer(self, Buffer):
        """Set buffer to value of Python Imaging Library image."""
        """Write display buffer to physical display"""
        imwidth, imheight = Buffer.size
        if imwidth > self.width or imheight > self.height:
            raise ValueError('Buffer must be same dimensions as display \
                ({0}x{1}).' .format(self.width, self.height))
        img = self.np.asarray(Buffer)
        pix = self.np.zeros((self.width,self.height,2), dtype = self.np.uint8)
        pix[...,[0]] = self.np.add(self.np.bitwise_and(img[...,[0]],0xF8),self.np.right_shift(img[...,[1]],5))
        pix[...,[1]] = self.np.add(self.np.bitwise_and(self.np.left_shift(img[...,[1]],3),0xE0),self.np.right_shift(img[...,[2]],3))
        pix = pix.flatten().tolist()
        self.SetWindows ( 0, 0, self.width, self.height)
        self.digital_write(self.GPIO_DC_PIN,True)
        for i in range(0,len(pix),4096):
            self.spi_writebyte(pix[i:i+4096])	
        
    def clear(self):
        """Clear contents of image buffer"""
        _buffer = [0xff]*(self.width * self.height * 2)
        self.SetWindows ( 0, 0, self.width, self.height)
        self.digital_write(self.GPIO_DC_PIN,True)
        for i in range(0,len(_buffer),4096):
            self.spi_writebyte(_buffer[i:i+4096])	        
        

