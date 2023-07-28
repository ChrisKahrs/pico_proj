import time
from pimoroni import Button
from pimoroni import RGBLED
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2, PEN_P4
from neopixel import NeoPixel
import gc
from machine import Pin

class g:
    current_screen = 0 # splash
    current_player = 0 # pause
    display = None
    neopixel_pin = 2
    neopixel_strip = None
    neopixel_brightness = 0.5
    led = None
    screen_width = 0
    screen_height = 0
    brightness = 0.5
    led_count = 7
    players = []
    colors = []
        
button_a = Button(12)
button_b = Button(13)
button_x = Button(14)
button_y = Button(15)
button_next = Button(18, Pin.IN, Pin.PULL_UP)
# pin GP02 on neopixel
# waveshare ups gp6,7 
# open? 0,1,3,4,5,9,10,11,22,26,27,28 
g.led = RGBLED(6, 7, 8)
# button GP16-21 g.display

def free(full=False):
    gc.collect()
    F = gc.mem_free()
    A = gc.mem_alloc()
    T = F+A
    P = '{0:.2f}%'.format(F/T*100)
    if not full: return P
    else : return ('Total:{0} Free:{1} ({2})'.format(T,F,P))

def set_brightness(color):
    # Adjust the brightness of the RGB values in the color tuple
    r, gg, b = color
    r = int(r * g.brightness)  # Scale the red value
    gg = int(gg * g.brightness)  # Scale the green value
    b = int(b * g.brightness)  # Scale the blue value
    return (r, gg, b)  # Return the adjusted color tuple

def main():
    pin = Pin(g.neopixel_pin, Pin.OUT) 
    g.neopixel_strip = NeoPixel(pin, g.led_count)
    # ? g.neopixel_strip.brightness(g.neopixel_brightness)
    g.display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2 ,pen_type=PEN_P4) #rotate= 90
    g.display.set_font("bitmap8")
    g.display.set_backlight(0.8)
    g.screen_width, g.screen_height = g.display.get_bounds()

    colors = {"red" :{"rgb": (255, 0, 0), "pen":g.display.create_pen(255, 0, 0) },
            "yellow" :{"rgb": (255, 255, 0), "pen":g.display.create_pen(255, 255, 0)},
            "green" :{"rgb": (0, 255, 0), "pen":g.display.create_pen(0, 255, 0)},
            "blue" :{"rgb": (0, 0, 255), "pen":g.display.create_pen(0, 0, 255)},
            "black" :{"rgb": (0, 0, 0), "pen":g.display.create_pen(0, 0, 0)},
            "white" :{"rgb": (255, 255, 255), "pen":g.display.create_pen(255, 255, 255)},
            "purple" :{"rgb": (255, 0, 255), "pen":g.display.create_pen(255, 0, 255)},
            "pink" :{"rgb": (255, 192, 203), "pen":g.display.create_pen(255, 192, 203)},
            "lime" :{"rgb": (0, 255, 255), "pen":g.display.create_pen(0, 255, 255)},
            "orange" :{"rgb": (255, 165, 0), "pen":g.display.create_pen(255, 165, 0)},
            "grey" :{"rgb": (128, 128, 128), "pen":g.display.create_pen(128, 128, 128)},
            "cyan" :{"rgb": (0, 255, 255), "pen":g.display.create_pen(0, 255, 255)}}

    players = [{"name":"P0", "total_time":0, "start_time": 0, "bg_color": colors["grey"], "fg_color": colors["black"], "turns": [(0,0)], "position" : 0},
               {"name":"P1", "total_time":0, "start_time": 0, "bg_color": colors["red"], "fg_color": colors["black"], "turns": [(0,0)], "position" : 1},
               {"name":"P2", "total_time":0, "start_time": 0, "bg_color": colors["yellow"], "fg_color": colors["black"], "turns": [(0,0)], "position" : 2},
               {"name":"P3", "total_time":0, "start_time": 0, "bg_color": colors["green"], "fg_color": colors["black"], "turns": [(0,0)], "position" : 3},
               {"name":"P4", "total_time":0, "start_time": 0, "bg_color": colors["blue"], "fg_color": colors["black"], "turns": [(0,0)], "position" : 4},
               {"name":"P5", "total_time":0, "start_time": 0, "bg_color": colors["black"], "fg_color": colors["white"], "turns": [(0,0)], "position" : 5},
               {"name":"P6", "total_time":0, "start_time": 0, "bg_color": colors["white"], "fg_color": colors["black"], "turns": [(0,0)], "position" : 6},
               {"name":"P7", "total_time":0, "start_time": 0, "bg_color": colors["purple"], "fg_color": colors["black"], "turns": [(0,0)], "position" :7},
               {"name":"P8", "total_time":0, "start_time": 0, "bg_color": colors["pink"], "fg_color": colors["black"], "turns": [(0,0)], "position" : 8},
               {"name":"P9", "total_time":0, "start_time": 0, "bg_color": colors["lime"], "fg_color": colors["black"], "turns": [(0,0)], "position" : 9}]

    while True:
        g.display.clear()
        g.display.set_pen(colors["black"]["pen"])
        row_height = 10
        color_height = 30
        color_width = 300
        counter = 0
        for player in players:
            if counter == 2 and (time.time() % 2 == 0):
                g.display.set_pen(colors["white"]["pen"])
                g.display.rectangle(0, row_height-2, color_width+12, color_height+4)
            g.display.set_pen(player["bg_color"]["pen"])
            g.display.rectangle(5, row_height, color_width, color_height)

            g.display.set_pen(player["fg_color"]["pen"])
            g.display.text(player["name"], 5, row_height+5, 100, scale = 3)
            row_height += 40
            counter += 1
            
            
        # g.led.set_rgb(*player["bg_color"]["rgb"]) # and led light string
        time.sleep(0.1)
        if button_next.read():
            print("next")
        if button_a.read(): 
            print("Free RAM: ",free(True))
            print('\u2713')
            # print(u'\N{check mark}')show graphics?
            g.display.set_backlight(0.8)
        if button_b.read(): 
            print("Free RAM: ",free(True))
            g.display.set_backlight(0.1)
        if button_x.read():
            g.neopixel_strip[1] = set_brightness(colors["red"]["rgb"]) # set the first pixel to white
            g.led.set_rgb(*colors["red"]["rgb"]) # and led light string
            g.neopixel_strip.write()
        if button_y.read():
            g.neopixel_strip[5] = set_brightness(colors["orange"]["rgb"]) # set the first pixel to white
            g.led.set_rgb(*colors["orange"]["rgb"]) # and led light string
        # check and other overlay graphics?
        g.neopixel_strip.write() 
        g.display.update()

if __name__ == "__main__":
    main()
    


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