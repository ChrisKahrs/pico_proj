import time
from pimoroni import Button
from pimoroni import RGBLED
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2, PEN_P4
from neopixel import NeoPixel
import gc
from machine import Pin
import math

class g:
    current_screen = 0 # splash
    current_player = 0 # pause
    active_player = 0 # used to capture when a player changes
    display = None
    neopixel_pin = 2
    neopixel_strip = None
    neopixel_brightness = 0.1
    led = None
    screen_width = 0
    screen_height = 0
    brightness = 0.1
    led_count = 7
    line = 1 
    row_selected = 0
    shift = 0
    list_length = 0
    total_lines = 6
        
# pin layouts
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
    g.neopixel_strip = NeoPixel(Pin(g.neopixel_pin, Pin.OUT) , g.led_count)

    g.display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2 ,pen_type=PEN_P4) #rotate= 90
    g.display.set_font("bitmap8")
    g.display.set_backlight(0.7)
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

    players = [{"name":"P0", "start_time": 0, "bg_color": colors["grey"], "fg_color": colors["white"], "turns": [], "position" : 0},
               {"name":"P1", "start_time": 0, "bg_color": colors["red"], "fg_color": colors["black"], "turns": [], "position" : 1},
               {"name":"P2", "start_time": 0, "bg_color": colors["yellow"], "fg_color": colors["black"], "turns": [], "position" : 2},
               {"name":"P3", "start_time": 0, "bg_color": colors["green"], "fg_color": colors["black"], "turns": [], "position" : 3},
               {"name":"P4", "start_time": 0, "bg_color": colors["blue"], "fg_color": colors["black"], "turns": [], "position" : 4},
               {"name":"P5", "start_time": 0, "bg_color": colors["black"], "fg_color": colors["white"], "turns": [], "position" : 5},
               {"name":"P6", "start_time": 0, "bg_color": colors["white"], "fg_color": colors["black"], "turns": [], "position" : 6},
               {"name":"P7", "start_time": 0, "bg_color": colors["purple"], "fg_color": colors["black"], "turns":[], "position" :7},
               {"name":"P8", "start_time": 0, "bg_color": colors["pink"], "fg_color": colors["black"], "turns": [], "position" : 8},
               {"name":"P9", "start_time": 0, "bg_color": colors["lime"], "fg_color": colors["black"], "turns": [], "position" : 9}]
    first_time_setup = True

    while True:

        g.display.set_pen(colors["black"]["pen"])
        g.display.clear()
        row_height = 10 # figure out how to divide by 6 and have all of this work?  Display text size?
        color_height = 30
        color_width = g.screen_width - 5
        line = 0
        if first_time_setup:
            first_time_setup = False
            players[0]["start_time"] = time.time()
        
        g.list_length = len(players) -1
        short_list = players[g.shift:g.shift+g.total_lines]

        if g.current_player != g.active_player:
            print("player changed from ", g.active_player, " to ", g.current_player)
            players[g.active_player]["turns"].append(time.time() - players[g.active_player]["start_time"])
            players[g.active_player]["start_time"] = 0
            players[g.current_player]["start_time"] = time.time()
            g.active_player = g.current_player
            # print(json.dumps(players[g.active_player]))

        # display list of players on the screen
        for player in short_list:
            if (g.row_selected == line):
                if (time.time() % 2 == 0):
                    g.display.set_pen(colors["white"]["pen"])
                    g.display.rectangle(0, row_height-2, color_width+12, color_height+4)
                for i in range(g.led_count):
                    g.neopixel_strip[i] = set_brightness(player["bg_color"]["rgb"])
                g.led.set_rgb(*player["bg_color"]["rgb"])

            g.display.set_pen(player["bg_color"]["pen"])
            g.display.rectangle(5, row_height, color_width, color_height)

            g.display.set_pen(player["fg_color"]["pen"])
            summy = sum(player["turns"])
            hour = math.floor(summy/3600)
            min = math.floor((summy - (hour *3600)) /60)
            sec = round(summy - (min * 60) - (hour * 3600))
            str_text = player["name"] + "- {0:01}:{1:02}:{2:02}".format(hour, min, sec)
            adder = 0
            if player["name"] == players[g.current_player]["name"]:
                adder = 1
                summy = (time.time() - player["start_time"])
                hour = math.floor(summy/3600)
                min = math.floor((summy - (hour *3600)) /60)
                sec = round(summy - (min * 60) - (hour * 3600))
                str_text =str(str_text + "->{0:01}:{1:02}:{2:02}".format(hour, min, sec))
                
            str_text = str(str_text + " t" + str(len(player["turns"])+adder))
            g.display.text(str_text, 5, row_height+5, g.screen_width, scale = 3)


            row_height += 40
            line += 1
            
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
            if g.current_player > 0:
                g.current_player -= 1
            if g.row_selected > 0:
                g.row_selected -= 1  
            else:
                if g.shift > 0:
                    g.shift -= 1  

        if button_y.read():
            if g.current_player <= (g.list_length):
                g.current_player += 1
            if g.row_selected < (g.total_lines -1):
                g.row_selected += 1
            else: 
                if g.shift+ (g.total_lines-1) < (g.list_length):
                    g.shift += 1
            if g.current_player == (g.list_length+1):
                g.current_player = 1
                g.shift = 0
                g.row_selected = 1

        # check and other overlay graphics?
        g.neopixel_strip.write() 
        g.display.update()

if __name__ == "__main__":
    main()

""" old code
        #display.text("Button A Pressed", 10, 10, 240, 6)   # landscape
        display.text("Button A Pressed", 2, 10, 135, 4)    # potrait 
        
        a=95
        file=open("add.csv","w")	# file is created and opened in write mode
        while a>0:			# program logic			
            file.write(str(a)+",")	# data is written as a string in the CSV file
            file.flush()		# internal buffer is flushed
            a-=5
"""