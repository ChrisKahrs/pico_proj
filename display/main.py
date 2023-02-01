# Multi-sized Font for Raspberry Pi Pico LCD/OLED Displays
# Existing framebuf library only supports 8*8 font size
# lcd_write method has been implemented in the LCD_1inch3
# class inside the lcd_lib.py file
from machine import Pin,SPI,PWM
import framebuf
import time
import os
import gc

BL = 13
DC = 8
RST = 12
MOSI = 11
SCK = 10
CS = 9

def free(full=False):
  gc.collect()
  F = gc.mem_free()
  A = gc.mem_alloc()
  T = F+A
  P = '{0:.2f}%'.format(F/T*100)
  if not full: return P
  else : return ('Total:{0} Free:{1} ({2})'.format(T,F,P))

from lcd_lib import LCD_1inch3
import math 

def rgb_hex565(rgb):
    ''' Args:
            rgb: tuple having B,G,R values in decimal format
            
        Returns:
            64K Hexadecial image color code as a string
    '''
            
    # BRG - 565 format - Waveshare LCD
    # Flipping BGR to RGB
    blue, red, green = rgb[2], rgb[0], rgb[1]
    return ("%0.4X" % ((int(blue / 255 * 31) << 11) | (int(red / 255 * 63) << 5) | (int(green / 255 * 31))))

# LCD = LCD_1inch3()
# LCD.fill(LCD.black)
# orig_tm = time.time()
# pwm = PWM(Pin(BL))
# pwm.freq(1000)
# pwm.duty_u16(32768)#max 65535
# LCD.fill(LCD.black)
# keyA = Pin(15,Pin.IN,Pin.PULL_UP)
# keyB = Pin(17,Pin.IN,Pin.PULL_UP)
# keyX = Pin(19 ,Pin.IN,Pin.PULL_UP)
# keyY= Pin(21 ,Pin.IN,Pin.PULL_UP)

# up = Pin(2,Pin.IN,Pin.PULL_UP)
# dowm = Pin(18,Pin.IN,Pin.PULL_UP)
# left = Pin(16,Pin.IN,Pin.PULL_UP)
# right = Pin(20,Pin.IN,Pin.PULL_UP)
# ctrl = Pin(3,Pin.IN,Pin.PULL_UP)

print("Free RAM: ",free(True))
    

# while True:
    
#     diff_tm = time.time()-orig_tm
#     hour = math.floor(diff_tm/3600)
#     min = math.floor((diff_tm - (hour *3600)) /60)
#     sec = diff_tm - (min * 60) - (hour * 3600)
#     disp_str = "{0:01}:{1:02}:{2:02}".format(hour, min, sec)
    
#             # B-R-G
#     red   =   0x07E0
#     green =   0x003f
#     blue  =   0xf800
#     white =   0xffff
#     black =   0x0000
#     brown =   0x9260
#     cyan  =   0xf87e
#     yellow =  0x07ff
#     purple =  0x0c0f
#     magenta=  0xffe0
#     lavender= 0x7fff
    
#     LCD.fill_rect(0,0,240,25, red)
#     LCD.fill_rect(1,1,25,25,LCD.white)
#     LCD.write_text("red",x=50,y=0,size=3,color=LCD.white)
    
#     LCD.fill_rect(0,27,240,25, yellow)
#     LCD.fill_rect(1,28,25,25,LCD.white)
#     LCD.write_text(free(),x=50,y=27,size=3,color=LCD.black)
    
#     LCD.fill_rect(0,54,240,25, green)
#     LCD.fill_rect(1,55,25,25,LCD.white)
#     LCD.write_text("green",x=50,y=54,size=3,color=LCD.white)
    
#     LCD.fill_rect(0,81,240,25, blue)
#     LCD.fill_rect(1,82,25,25,LCD.white)
#     LCD.write_text("blue",x=50,y=81,size=3,color=LCD.white)
    
#     LCD.fill_rect(0,108,240,25, cyan)
#     LCD.fill_rect(1,109,25,25,LCD.white)
#     LCD.write_text("cyan",x=50,y=108,size=3,color=LCD.white)
    
#     LCD.fill_rect(0,135,240,25, magenta)
#     LCD.fill_rect(1,136,25,25,LCD.white)
#     LCD.write_text("magenta",x=50,y=135,size=3,color=LCD.white)
    
#     # later to get orange? LCD.fill_rect(0,162,240,25, int(rgb_hex565((255,255,0)),16))
#     LCD.fill_rect(0,162,240,25, black)
#     LCD.write_text("Order?",x=10,y=162,size=3,color=LCD.white)
#     LCD.fill_rect(0,189,240,25, black)
#     LCD.write_text("A-Start",x=10,y=189,size=3,color=LCD.white)
#     LCD.fill_rect(0,216,240,25, black)
#     LCD.write_text("Y-Reset",x=10,y=216,size=3,color=LCD.white)
  
#     if keyA.value() == 0:
#         LCD.fill_rect(208,15,30,30,LCD.red)
#     else :
#         LCD.fill_rect(208,15,30,30,LCD.white)
#         LCD.rect(208,15,30,30,LCD.red)
    
#     if keyY.value() == 0:
#         LCD.fill_rect(208,190,30,30,LCD.red)
#     else :
#         LCD.fill_rect(208,190,30,30,LCD.white)
#         LCD.rect(208,190,30,30,LCD.red)
#     LCD.show()
#     #time.sleep(1)
            
        
