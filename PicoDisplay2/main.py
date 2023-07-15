import time
import picographics
from pimoroni_bus import SPIBus
from pimoroni import Button
from pimoroni import RGBLED
import gc

button_a = Button(12)
button_b = Button(13)
button_x = Button(14)
button_y = Button(15)

led = RGBLED(6, 7, 8)

def free(full=False):
  gc.collect()
  F = gc.mem_free()
  A = gc.mem_alloc()
  T = F+A
  P = '{0:.2f}%'.format(F/T*100)
  if not full: return P
  else : return ('Total:{0} Free:{1} ({2})'.format(T,F,P))

from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2, PEN_P4
#from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_P8
#from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY, PEN_RGB332

display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2, rotate=270 ,pen_type=PEN_P4)
#display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, rotate=270 ,pen_type=PEN_P8)
#display = PicoGraphics(display=DISPLAY_PICO_DISPLAY, rotate=270, pen_type=PEN_RGB332)

display.set_backlight(1.0)

black = display.create_pen(0, 0, 0)
red = display.create_pen(255, 0, 0)
yellow = display.create_pen(255, 255, 0)
green = display.create_pen(0, 255, 0)
blue = display.create_pen(0, 0, 255)

while True:
    if button_a.read(): 
        display.set_pen(red)
        display.clear()
        display.set_pen(black)
        #display.text("Button A Pressed", 10, 10, 240, 6)   # landscape
        display.text("Button A Pressed", 2, 10, 135, 3)    # potrait 
        display.update()
        led.set_rgb(255, 0, 0)
        print("Free RAM: ",free(True))
        time.sleep(1.0)
    elif button_b.read():
        display.set_pen(yellow)
        display.clear()
        display.set_pen(black)
        #display.text("Button B Pressed", 10, 10, 240, 6)   # landscape
        display.text("Button B Pressed", 2, 10, 135, 3)    # potrait 
        display.update()
        led.set_rgb(255, 255, 0)
        time.sleep(1.0)
        a=95
        file=open("add.csv","w")	# file is created and opened in write mode
        while a>0:			# program logic			
            file.write(str(a)+",")	# data is written as a string in the CSV file
            file.flush()		# internal buffer is flushed
            a-=5
    elif button_x.read():    
        display.set_pen(green)
        display.clear()
        display.set_pen(black)
        #display.text("Button X Pressed", 10, 10, 240, 6)   # landscape
        display.text("Button X Pressed", 2, 10, 135, 3)    # potrait 
        display.update()
        led.set_rgb(0, 255, 0)
        time.sleep(1.0)
    elif button_y.read():    
        display.set_pen(blue)
        display.clear()
        display.set_pen(black)
        #display.text("Button Y Pressed", 10, 10, 240, 6)   # landscape
        display.text("Button Y Pressed", 2, 10, 135, 3)    # potrait 
        display.update()
        led.set_rgb(0, 0, 255)
        time.sleep(1.0)
        display.clear()
        display.update()
