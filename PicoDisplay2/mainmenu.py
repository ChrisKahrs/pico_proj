from pimoroni import Button, RGBLED
from picographics import PicoGraphics, DISPLAY_PICO_DISPLAY_2, PEN_P4
import gc
import time
from machine import Pin

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

class g: # globals for display parts
    display = None
    led = None
    brightness = 0.5
        
# pin layouts
button_a = Button(12)
button_b = Button(13)
button_x = Button(14)
button_y = Button(15)
button_next = Button(18, Pin.IN, Pin.PULL_UP)
g.led = RGBLED(6, 7, 8)
# waveshare ups gp6,7 
# open? 0,1,3,4,5,9,10,11,22,26,27,28 
# button GP16-21 g.display = picodisplay2

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
    red, green, blue = color
    red = int(red * g.brightness)  # Scale the red value
    green = int(green * g.brightness)  # Scale the green value
    blue = int(blue * g.brightness)  # Scale the blue value
    return (red, green, blue)  # Return the adjusted color tuple

def run_menu():
    # read json file into menu_system
    g.display = PicoGraphics(display=DISPLAY_PICO_DISPLAY_2 ,pen_type=PEN_P4) #, rotate= 90 test
    g.display.set_font("bitmap8")
    g.display.set_backlight(g.brightness)
    g.led.set_rgb(0, 0, 0)
    screen_width, screen_height = g.display.get_bounds()
    menu_system = {"defaults": {"bg_color": "black",
                                "fg_color": "white",
                                "alt_fg_color": "black",
                                "alt_bg_color": "orange",
                                "title_fg_color": "black",
                                "title_bg_color": "white",
                                "top_text_buffer": 5,
                                "side_text_buffer": 5,
                                "blink_rate": 0.5,
                                "font": "bitmap8",
                                "font_scale": 3,
                                "font_height": 8,
                                "option_lines": 5,
                                "start_menu": "Splash"},
                    "current_menu": "Players",
                    "current_option": "Settings",
                    "Splash": {"type": "menu",
                                "text": "Welcome to the game there is more text here to test the scroll function", 
                                "options": ["Settings", "Start", "Exit","Test","Test2","test3","test4"],
                                "value": "Settings"},
                    "Settings": {"type": "menu",
                                "text": "Select Setting",
                                "options": ["Players", "Brightness"],
                                "value": "Players"},
                    "Players": {"type": "option",
                                "text": "Number of Players?",
                                "options": ["1", "2", "3", "4", "5", "6", "7", "8", "9", "10"],
                                "value": "2"},
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
            "brown" :{"rgb": BROWN, "pen":g.display.create_pen(*BROWN)}}

    shift = 0
    scroll_counter = 0
    scroll_title = ""

    while True:
        defaults = menu_system["defaults"]
        current_menu = menu_system[menu_system["current_menu"]]
        g.display.set_pen(colors[defaults["bg_color"]]["pen"])
        g.display.clear()
        
        title_height =  int(screen_height / (1 + defaults["option_lines"]) * 1)
        option_height = screen_height - title_height
        # draw rectangle for title and title
        g.display.set_pen(colors[defaults["title_bg_color"]]["pen"])
        g.display.rectangle(0, 0, screen_width, int(title_height))
        g.display.set_pen(colors[defaults["title_fg_color"]]["pen"])
        # scroll title if too long
        title_width = g.display.measure_text(current_menu["text"], defaults["font_scale"])
        scroll_title_width = g.display.measure_text(scroll_title, defaults["font_scale"])
        print("title width: ", title_width)
        print("scroll title width: ", scroll_title_width)
        if scroll_title_width < screen_width:
            scroll_title = " " + current_menu["text"]
        else:
            if scroll_counter % 2 == 0:
                scroll_title = scroll_title[1:]
        g.display.text(scroll_title, defaults["side_text_buffer"], defaults["top_text_buffer"], 100_000, scale = defaults["font_scale"]) 
        
        line = 0
        display_options = current_menu["options"][shift:shift+defaults["option_lines"]]
        row_height = int(option_height / defaults["option_lines"])
        
        for i, option in enumerate(display_options):
            g.display.set_pen(colors[defaults["fg_color"]]["pen"])
            if (option == current_menu["value"]): # make it blink
                if (option != current_menu["options"][0]):
                    option = "^ " + option
                if (time.time() % 2 == 0):
                    g.display.set_pen(colors[defaults["alt_bg_color"]]["pen"])
                    g.display.rectangle(0, int(title_height + (line * row_height)), screen_width, int(row_height))
                    g.display.set_pen(colors[defaults["alt_fg_color"]]["pen"])
                else:
                    option = option + " <<"
            g.display.text(option, defaults["side_text_buffer"], defaults["top_text_buffer"] + ((line+1) * row_height), screen_width, scale = defaults["font_scale"])
            line += 1
            
        if button_x.read():
            if current_menu["options"][0] != current_menu["value"]:
                current_menu["value"] = current_menu["options"][current_menu["options"].index(current_menu["value"]) - 1]
                if shift > 0:
                    shift -= 1

        if button_y.read():
            # check for end of list then do nothing if value = last item
            if current_menu["options"][-1] != current_menu["value"]:
                current_menu["value"] = current_menu["options"][current_menu["options"].index(current_menu["value"]) + 1]
                shift += 1

        g.display.update()
        scroll_counter += 1
        time.sleep(0.1)
        print("Free RAM: ",free(True))

if __name__ == "__main__":
    run_menu()