from machine import Pin 
import time

led = Pin("LED", Pin.OUT)

led.toggle()
while True:
    led.toggle()
    time.sleep(0.5)
    