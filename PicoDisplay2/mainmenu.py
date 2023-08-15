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
    top_text_buffer = 5
    side_text_buffer = 5
        
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
    # read json file into menu_system
    g.display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2 ,pen_type=PEN_P4) #rotate= 90
    g.display.set_font("bitmap8")
    g.display.set_backlight(0.7)
    g.led.set_rgb(0, 0, 0)
    g.screen_width, g.screen_height = g.display.get_bounds()
    menu_system = {"defaults": {"bg_color": "black",
                                "fg_color": "white",
                                "alt_fg_color": "black",
                                "alt_bg_color": "orange",
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
                                "text": "Welcome to the game this is more text", #scrolling text?
                                "options": ["Settings", "Start", "Exit","Test","Test2","test3","test4"],
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
                                    "value": 0.6},
                    "P1_Color": {"type": "option", # better way?
                                "text": "Player 1 Color?",
                                "options": ["Red", "Yellow", "Green", "Blue", "Black", "White", "Purple", "Pink", "Lime", "Orange", "Grey", "Cyan", "Brown"]},
                                #seat setup, light configuation, etc
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
    shift = 0

    while True:
        defaults = menu_system["defaults"]
        current_menu = menu_system[menu_system["current_menu"]]
        g.display.set_pen(colors[defaults["bg_color"]]["pen"])
        g.display.clear()
        title_height =  g.screen_height / (defaults["text_lines"] + defaults["option_lines"]) # maybe x row height like 2 for the title box?
        option_height = g.screen_height - title_height
        g.display.set_pen(colors[defaults["alt_bg_color"]]["pen"])
        g.display.rectangle(0, 0, g.screen_width, int(title_height))
        g.display.set_pen(colors[defaults["alt_fg_color"]]["pen"])
        g.display.text(current_menu["text"], g.top_text_buffer, g.side_text_buffer, g.screen_width, scale = defaults["font_scale"]) # create another function for this? max_lines = menu_system["defaults"]["text_lines"])
        line = 0
        display_options = current_menu["options"][shift:shift+defaults["option_lines"]]
        row_height = int(option_height / defaults["option_lines"])
        
        for i, option in enumerate(display_options):
            g.display.set_pen(colors[defaults["fg_color"]]["pen"])
            if (option == current_menu["value"]): # make it blink 
                    if (time.time() % 2 == 0):
                        g.display.set_pen(colors[defaults["alt_bg_color"]]["pen"])
                        g.display.rectangle(0, int(title_height + (line * row_height)), g.screen_width, int(row_height))
                        g.display.set_pen(colors[defaults["alt_fg_color"]]["pen"])
                    else:
                        option = "> " + option + " <"
            g.display.text(option, g.top_text_buffer, g.side_text_buffer + ((line+1) * row_height), g.screen_width, scale = defaults["font_scale"])
            line += 1
            
        if button_x.read():
            if current_menu["options"][0] != current_menu["value"]:
                current_menu["value"] = current_menu["options"][current_menu["options"].index(current_menu["value"]) - 1]
                shift -= 1

        if button_y.read():
            # check for end of list then do nothing if value = last item
            if current_menu["options"][-1] != current_menu["value"]:
                current_menu["value"] = current_menu["options"][current_menu["options"].index(current_menu["value"]) + 1]
                shift += 1

        g.display.update()
        time.sleep(0.1)
        # print("Free RAM: ",free(True))


if __name__ == "__main__":
    run_menu()