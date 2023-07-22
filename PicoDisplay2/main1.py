import time
# import picographics
# from pimoroni_bus import SPIBus
from pimoroni import Button
from pimoroni import RGBLED
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2, PEN_P4
from neopixel import NeoPixel
import gc
from machine import Pin

button_a = Button(12)
button_b = Button(13)
button_x = Button(14)
button_y = Button(15)

led = RGBLED(6, 7, 8)

class g:
    display = 0
    screen_width = 0
    screen_height = 0
    players = []
    colors = []

display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2 ,pen_type=PEN_P4) #rotate= 90
display.set_font("bitmap8")
display.set_backlight(0.8)
screen_width, screen_height = display.get_bounds()

def free(full=False):
  gc.collect()
  F = gc.mem_free()
  A = gc.mem_alloc()
  T = F+A
  P = '{0:.2f}%'.format(F/T*100)
  if not full: return P
  else : return ('Total:{0} Free:{1} ({2})'.format(T,F,P))

colors = {"red" :{"rgb": (255, 0, 0), "pen":display.create_pen(255, 0, 0) },
        "yellow" :{"rgb": (255, 255, 0), "pen":display.create_pen(255, 255, 0)},
        "green" :{"rgb": (0, 255, 0), "pen":display.create_pen(0, 255, 0)},
        "blue" :{"rgb": (0, 0, 255), "pen":display.create_pen(0, 0, 255)},
        "black" :{"rgb": (0, 0, 0), "pen":display.create_pen(0, 0, 0)},
        "white" :{"rgb": (255, 255, 255), "pen":display.create_pen(255, 255, 255)},
        "purple" :{"rgb": (255, 0, 255), "pen":display.create_pen(255, 0, 255)},
        "pink" :{"rgb": (255, 192, 203), "pen":display.create_pen(255, 192, 203)},
        "lime" :{"rgb": (0, 255, 255), "pen":display.create_pen(0, 255, 255)},
        "orange" :{"rgb": (255, 165, 0), "pen":display.create_pen(255, 165, 0)},
        "grey" :{"rgb": (128, 128, 128), "pen":display.create_pen(128, 128, 128)},
        "cyan" :{"rgb": (0, 255, 255), "pen":display.create_pen(0, 255, 255)}}

players = [{"name":"P1", "total_time":0, "start_time": 0, "bg_color": colors["red"], "fg_color": colors["black"], "turns": [(0,0)], "position" : 0},
            {"name":"P2", "total_time":0, "start_time": 0, "bg_color": colors["yellow"], "fg_color": colors["black"], "turns": [(0,0)], "position" : 1},
            {"name":"P3", "total_time":0, "start_time": 0, "bg_color": colors["green"], "fg_color": colors["black"], "turns": [(0,0)], "position" : 2},
            {"name":"P4", "total_time":0, "start_time": 0, "bg_color": colors["blue"], "fg_color": colors["black"], "turns": [(0,0)], "position" : 3},
            {"name":"P5", "total_time":0, "start_time": 0, "bg_color": colors["black"], "fg_color": colors["white"], "turns": [(0,0)], "position" : 4},
            {"name":"P6", "total_time":0, "start_time": 0, "bg_color": colors["white"], "fg_color": colors["black"], "turns": [(0,0)], "position" : 5},
            {"name":"P7", "total_time":0, "start_time": 0, "bg_color": colors["purple"], "fg_color": colors["black"], "turns": [(0,0)], "position" : 6},
            {"name":"P8", "total_time":0, "start_time": 0, "bg_color": colors["pink"], "fg_color": colors["black"], "turns": [(0,0)], "position" : 7},
            {"name":"P9", "total_time":0, "start_time": 0, "bg_color": colors["lime"], "fg_color": colors["black"], "turns": [(0,0)], "position" : 8}]

while True:
    display.clear()
    display.set_pen(colors["black"]["pen"])
    height = 10
    width = 150
    for player in players:
        display.set_pen(player["bg_color"]["pen"])
        display.rectangle(0, height, width, 30)

        display.set_pen(player["fg_color"]["pen"])
        display.text(player["name"], 5, height+5, 100, scale = 3)
        height += 40
        led.set_rgb(*colors["black"]["rgb"]) # and led light string
    time.sleep(0.1)
    if button_a.read(): 
        print("Free RAM: ",free(True))
        print('\u2713')
        # print(u'\N{check mark}')
        display.set_backlight(0.8)
    if button_b.read(): 
        print("Free RAM: ",free(True))
        display.set_backlight(0.1)
    if button_x.read():


        pin = Pin(2, Pin.OUT)   # set GPIO8 to output to drive NeoPixels
        np = NeoPixel(pin, 10)   # create NeoPixel driver for 8 pixels
        np[1] = (255, 0, 0) # set the first pixel to white
        np.write()
    if button_y.read():


        pin = Pin(2, Pin.OUT)   # set GPIO8 to output to drive NeoPixels
        np = NeoPixel(pin, 10)   # create NeoPixel driver for 8 pixels
        np[1] = (0, 255, 0) # set the first pixel to white
        np.write() 
        # numpix = 10
        # strip = Neopixel(numpix, 0, 2pi8, "RGB")

        # delay = 0.15
        # strip.brightness(2)

        # strip.set_pixel(0,(50,255,0))

        # strip.show()
    display.update()

"""
while True:
    if button_a.read(): 
        display.set_backlight(0.5)
        display.set_pen(red)
        display.clear()
        display.set_pen(black)
        #display.text("Button A Pressed", 10, 10, 240, 6)   # landscape
        display.text("Button A Pressed", 2, 10, 135, 4)    # potrait 
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
        display.set_backlight(0.1)
"""