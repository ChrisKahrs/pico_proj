from math import sin, cos
from random import randrange


view = -1
players = []


class Player:
    def __init__(self, x, y, w, h, r, p):
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.r = r
        self.p = p


def reset():
    global players

    shapes = []
    for i in range(50):
        x = randrange(0, 120)
        y = randrange(0, 120)
        w = randrange(0, 20)
        h = randrange(0, 20)
        r = randrange(0, 360)
        p = hsv(randrange(0, 100) / 100.0, 1.0, 1.0)
        shapes.append(Shape(x, y, w, h, r, p))


def update(tick):
    global view


def label(s):
    pen(0, 0, 0, 8)
    frect(0, 11, 120, 15)
    pen(0, 0, 0)
    text(s + ":", 3, 16)
    pen(15, 15, 15)
    text(s + ":", 2, 15)


def draw(tick):
    global view
    global shapes

    pen(0, 0, 0)
    clear()
    
    if view == 0:
        for s in shapes:
            pen(s.p)
            frect(s.x, s.y, s.w, s.h)
        label("Filled rectangles")

    elif view == 1:
        for s in shapes:
            pen(s.p)
            line(s.x, s.y, s.x + s.w, s.y + s.h)
        label("Lines")

    elif view == 2:
        i = 0
        for s in shapes:
            pen(s.p)
            text(chr((i % 96) + 32), s.x, s.y)
            i += 1
        label("Text")

    elif view == 3:
        i = 0
        for s in shapes:
            sprite(i, s.x, s.y)
            i += 1
        label("Sprites")

    elif view == 4:
        for s in shapes:
            pen(s.p)
            rx = int(sin(s.r * (3.1415927 / 180.0)) * (s.w / 2))
            ry = int(cos(s.r * (3.1415927 / 180.0)) * (s.h / 2))
            fpoly((s.x - rx, s.y - ry), (s.x + ry, s.y - rx), (s.x + rx, s.y + ry), (s.x - ry, s.y + rx))
        label("Filled polygons")

    elif view == 5:
        for s in shapes:
            pen(s.p)
            circle(s.x, s.y, int(s.w / 2))
        label("Circles")

    elif view == 6:
        for s in shapes:
            pen(s.p)
            rect(s.x, s.y, s.w, s.h)
        label("Rectangles")

    elif view == 7:
        for s in shapes:
            pen(s.p)
            fcircle(s.x, s.y, int(s.w / 2))
        label("Filled circles")

    elif view == 8:
        for s in shapes:
            pen(s.p)
            rx = int(sin(s.r * (3.1415927 / 180.0)) * (s.w / 2))
            ry = int(cos(s.r * (3.1415927 / 180.0)) * (s.h / 2))
            poly((s.x - rx, s.y - ry), (s.x + ry, s.y - rx), (s.x + rx, s.y + ry), (s.x - ry, s.y + rx))
        label("Polygons")

    elif view == 9:
        for s in shapes:
            pen(s.p)
            pixel(s.x, s.y)
        label("Pixels")

    # draw title
    pen(15, 0, 0)
    frect(0, 0, 115, 15)
    pen(0, 0, 0)
    text("Red Player", 20, 5)
    pen(15,15,15)
    frect(2,2,10,10)
    pen(0,0,0)
    rect(2,2,10,10)
    if tick % 10 == 0:
        pen(15,15,15)
        rect(2,2,10,10)
    
    
    pen(0, 15, 0)
    frect(0, 15, 115, 15)
    pen(0, 0, 0)
    text("Green Player", 20, 20)
    pen(15,15,15)
    frect(2,17,10,10)
    
    pen(0, 0, 15)
    frect(0, 30, 115, 15)
    pen(0, 0, 0)
    text("Blue Player", 20, 35)
    
    pen(15,15,15)
    fpoly((115,50),(115,60),(120,55))
    
    if pressed(A):
        pen(0,0,0)
        text("1",3,3)
# reset()

start()