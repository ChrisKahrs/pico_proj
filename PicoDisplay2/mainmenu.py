import time
from pimoroni import Button
from pimoroni import RGBLED
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2, PEN_P4
from neopixel import NeoPixel
import gc
from machine import Pin
import math

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
PINK = (255, 192, 203)
LIME = (0, 255, 255)
ORANGE = (255, 165, 0)
GREY = (128, 128, 128)
CYAN = (0, 255, 255)
BROWN = (165, 42, 42)

class g:
    current_screen = 0 # splash
    current_player = 0 # pause
    active_player = 0 # used to capture when a player changes
    display = None
    neopixel_pin = 2
    neopixel_strip = None
    neopixel_brightness = 0.1
    screen_brightness = 0.7
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
    page = 2 # 0 splash, 1 settings, 2 game, 3 score
    page_old = 2
    player_count = 1
        
# pin layouts
button_a = Button(12)
button_b = Button(13)
button_x = Button(14)
button_y = Button(15)
button_next = Button(18, Pin.IN, Pin.PULL_UP)
g.led = RGBLED(6, 7, 8)
# pin GP02 on neopixel
# waveshare ups gp6,7 
# open? 0,1,3,4,5,9,10,11,22,26,27,28 
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

def run_menu():
    g.neopixel_strip = NeoPixel(Pin(g.neopixel_pin, Pin.OUT) , g.led_count)

    g.display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2 ,pen_type=PEN_P4) #rotate= 90
    g.display.set_font("bitmap8")
    g.display.set_backlight(0.7)
    g.screen_width, g.screen_height = g.display.get_bounds()
    menu_system = {"defaults": {"bg_color": "black",
                               "fg_color": "white",
                               "alt_fg_color": "black",
                               "alt_bg_color": "white",
                               "blink_rate": 0.5,
                               "font": "bitmap8",
                               "font_scale": 3,
                               "font_height": 8,
                               "text_lines": 1,
                               "option_lines": 5,
                               "start_menu": "Splash"},
                  "current_menu": "Splash",
                  "current_option": "Settings", # or should it be 0?
                  "Splash": {"type": "menu",
                             "text": "Welcome to the game",
                             "options": ["Settings", "Start"],
                             "value": "Settings"},
                  "Settings": {"type": "menu",
                               "text": "Select Setting",
                               "options": ["Players", "Brightness"],
                               "value": "Players"},
                  "Players": {"type": "option",
                              "text": "Number of Players?",
                              "options": [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
                              "value": 4},
                  "Brightness": {"type": "option",
                                 "text": "Screen Brightness?",
                                 "options": [0.2, 0.4, 0.6, 0.8, 1.0],
                                 "value": 0.6}
    }
    colors = {"red" :{"rgb": RED, "pen":g.display.create_pen(*RED) },
            "yellow" :{"rgb": YELLOW, "pen":g.display.create_pen(*YELLOW)},
            "green" :{"rgb": GREEN, "pen":g.display.create_pen(*GREEN)},
            "blue" :{"rgb": BLUE, "pen":g.display.create_pen(*BLUE)},
            "black" :{"rgb": BLACK, "pen":g.display.create_pen(*BLACK)},
            "white" :{"rgb": WHITE, "pen":g.display.create_pen(*WHITE)},
            "purple" :{"rgb": PURPLE, "pen":g.display.create_pen(*PURPLE)},
            "pink" :{"rgb": PINK, "pen":g.display.create_pen(*PINK)},
            "lime" :{"rgb": LIME, "pen":g.display.create_pen(*LIME)},
            "orange" :{"rgb": ORANGE, "pen":g.display.create_pen(*ORANGE)},
            "grey" :{"rgb": GREY, "pen":g.display.create_pen(*GREY)},
            "cyan" :{"rgb": CYAN, "pen":g.display.create_pen(*CYAN)},
                        "cyan" :{"rgb": BROWN, "pen":g.display.create_pen(*BROWN)}}
    player_counts = [1,2,3,4,5,6,7,8,9,10]
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
        g.display.set_pen(colors[menu_system["defaults"]["bg_color"]]["pen"])
        g.display.clear()
        title_height =  g.screen_height / (menu_system["defaults"]["text_lines"] + menu_system["defaults"]["option_lines"])
        option_height = g.screen_height - title_height
        current_menu = menu_system[menu_system["current_menu"]]
        print("current_menu", current_menu)
        current_menu_text = current_menu["text"]
        g.display.set_pen(colors[menu_system["defaults"]["alt_bg_color"]]["pen"])
        g.display.rectangle(0, 0, g.screen_width, int(title_height))
        g.display.set_pen(colors[menu_system["defaults"]["alt_fg_color"]]["pen"])
        g.display.text(current_menu_text, 5, 5, g.screen_width, scale = menu_system["defaults"]["font_scale"]) # create another function for this? max_lines = menu_system["defaults"]["text_lines"])
        line = 0
        g.display.set_pen(colors[menu_system["defaults"]["fg_color"]]["pen"])
        row_height = option_height / menu_system["defaults"]["option_lines"]
        for i, option in enumerate(current_menu["options"]):
            if (line + 1 + row_height) < option_height:
                line += 1
                g.display.text(option, 5, int(5 + (line * row_height)), g.screen_width, scale = menu_system["defaults"]["font_scale"])
        g.display.update()
        break
        
        
        
        if g.page != g.page_old:
            g.page_old = g.page
        
        if g.page == 2:

            row_height = 10 # figure out how to divide by 6 and have all of this work?  Display text size?
            color_height = 30
            color_width = g.screen_width - 10
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
                        g.display.rectangle(0, row_height-4, color_width+12, color_height+8)
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
                
            # button checks
            if button_next.read():
                print("next")
                
            if button_a.read(): # pause button
                print("Free RAM: ",free(True))
                print('\u2713')
                # print(u'\N{check mark}')show graphics?
                g.display.set_backlight(g.screen_brightness)
                # unpause come back to current player?
                # g.paused_current_player = g.current_player
                # g.paused_row_selected = g.row_selected
                # g.paused_shift = g.shift
                g.current_player = 0
                g.shift = 0
                g.row_selected = 0
                
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

        if g.page == 1:
            question_window_height = 0 # figure out how to divide by 6 and have all of this work?  Display text size?
            scroll_window_height = 0 # 5/6th of the screen
            row_height = 10 # figure out how to divide by 6 and have all of this work?  Display text size?
            color_height = 30
            color_width = g.screen_width - 10
            line = 0
            if first_time_setup:
                first_time_setup = False
                g.row_selected = 0
                g.player_count = 0
                row_height= 50
                g.total_lines = 5
                g.shift = 0
            
            g.display.set_pen(colors["white"]["pen"])
            g.display.text("Player Count? ", 5, row_height + 5, g.screen_width, scale = 3)
            
            g.list_length = len(player_counts) -1
            short_list = player_counts[g.shift:g.shift+g.total_lines]
            row_height += 40 # to take into account the question window
            # display list of players on the screen
            for pcount in short_list:
                if (g.row_selected == line):
                    if (time.time() % 2 == 0):
                        g.display.set_pen(colors["white"]["pen"])
                        g.display.rectangle(0, row_height-4, color_width+12, color_height+8)
                        g.display.set_pen(colors["black"]["pen"])
                        g.display.text(str(player_counts[pcount-1]), 5, row_height+5, g.screen_width, scale = 3)
                        g.display.set_pen(colors["white"]["pen"])
                    else:
                        g.display.text(str(player_counts[pcount-1]), 5, row_height+5, g.screen_width, scale = 3)
                else:
                    g.display.text(str(player_counts[pcount-1]), 5, row_height+5, g.screen_width, scale = 3)
                row_height += 40
                line += 1
                
            # button checks
            if button_next.read():
                print("next")
                
            if button_a.read(): # pause button
                print("Free RAM: ",free(True))
                print('\u2713')
                # print(u'\N{check mark}')show graphics?
                g.display.set_backlight(g.screen_brightness)
                # record and return to home screen? Or move to player setup screens?
                
            if button_b.read(): 
                print("Free RAM: ",free(True))
                g.display.set_backlight(0.1)
            
            if button_x.read():
                if g.player_count > 0:
                    g.player_count -= 1
                if g.row_selected > 0:
                    g.row_selected -= 1  
                else:
                    if g.shift > 0:
                        g.shift -= 1  

            if button_y.read():
                if g.player_count <= (g.list_length):
                    g.player_count += 1
                if g.row_selected < (g.total_lines -1):
                    g.row_selected += 1
                else: 
                    if g.shift+ (g.total_lines-1) < (g.list_length):
                        g.shift += 1
                if g.player_count == (g.list_length+1):
                    g.player_count = 0
                    g.shift = 0
                    g.row_selected = 0
                print(g.player_count)
                print(g.row_selected)
                print(g.shift)


        # check and other overlay graphics?
        g.display.update()
        time.sleep(0.1)

if __name__ == "__main__":
    run_menu()

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