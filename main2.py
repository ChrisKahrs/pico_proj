#Example 1 - Control individual LED

from neopixel import Neopixel
import utime
import random

def allOfIt(onOff):
    numpix = 10
    strip = Neopixel(numpix, 0, 28, "RGB")

    # for some reason it is now GRB?  Swap?
    red = (255, 0, 0)
    orange = (255, 50, 0)
    yellow = (255, 100, 0)
    green = (0, 255, 0)
    blue = (0, 0, 255)
    indigo = (100, 0, 90)
    violet = (200, 0, 100)
    colors_rgb = [red, orange, yellow, green, blue, indigo, violet]

    delay = 0.15
    strip.brightness(2)
    blank = (0,0,0)
    # 
    # strip.fill((0,0,0))
    # while True:
    #     strip.set_pixel(1,blank)
    #     utime.sleep(delay)
    #     strip.show()
    if onOff == 1:
        strip.set_pixel(0,(50,255,0))
    else:
        strip.fill(blank)
    utime.sleep(delay)
    strip.show()
    # strip.fill((0,0,0))
#     strip.set_pixel(3,blue)
#     strip.set_pixel(4,green)
#     strip.show()
    # strip.fill(blank)
     

#     for i in range(10):
#         strip.set_pixel(random.randint(0, numpix-1), colors_rgb[random.randint(0, len(colors_rgb)-1)])
#         strip.set_pixel(random.randint(0, numpix-1), colors_rgb[random.randint(0, len(colors_rgb)-1)])
#         strip.set_pixel(random.randint(0, numpix-1), colors_rgb[random.randint(0, len(colors_rgb)-1)])
#         strip.set_pixel(random.randint(0, numpix-1), colors_rgb[random.randint(0, len(colors_rgb)-1)])
#         strip.set_pixel(random.randint(0, numpix-1), colors_rgb[random.randint(0, len(colors_rgb)-1)])
#         strip.show()
#         utime.sleep(delay)
#         strip.fill((0,0,0))
    
    
        
          


