"""ILI9341 demo (fonts)."""
from time import sleep
from ili9341 import Display, color565
from machine import Pin, SPI
from xglcd_font import XglcdFont


def test():
    """Test code."""
    # Baud rate of 40000000 seems about the max
    spi = SPI(1, baudrate=40000000, sck=Pin(14), mosi=Pin(13))
    display = Display(spi, dc=Pin(4), cs=Pin(16), rst=Pin(17))

    print('Loading fonts...')
    print('Loading arcadepix')
    arcadepix = XglcdFont('ArcadePix9x11.c', 9, 11)
     print('Fonts loaded.')

    display.draw_text(0, 0, 'Arcade Pix 9x11', arcadepix, color565(255, 0, 0))

    sleep(9)
    display.clear()

    display.draw_text(0, 255, 'Arcade Pix 9x11', arcadepix,
                      color565(255, 0, 0),
                      landscape=True)
 
    sleep(9)
    display.clear()

    display.draw_text(0, 0, 'Arcade Pix 9x11', arcadepix, color565(255, 0, 0),
                      background=color565(0, 255, 255))


    sleep(9)
    display.cleanup()


test()
