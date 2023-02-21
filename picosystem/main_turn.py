
class ColorEntity:
    def __init__(self, screen_order, rgb, name, selected_order=0):
        self.screen_order = screen_order
        self.rgb = rgb
        self.name = name
        self.selected_order = selected_order

class g:
    cursor = 0
    view = 0
    player_count = 0
    colors = [ColorEntity(0,(15,0,0), "Red"),
              ColorEntity(1,(0,15,0), "Green"),
              ColorEntity(2,(0,0,15), "Blue")]

def reset():
    pass

def update(tick):
    
    if pressed(DOWN):
        g.cursor += 1
    if pressed(UP):
        g.cursor -= 1
    
    if pressed(A):
        g.player_count += 1
        g.colors[g.cursor].selected_order = g.player_count
    
    #Reset Colors
    if pressed(Y):
        g.player_count = 0
        for i in g.colors:
            i.selected_order = g.player_count

def draw(tick):
    pen(0, 0, 0)
    clear()
    y_down = 5
    x_over = 5
    
    for i in g.colors:
        pen(i.rgb[0],i.rgb[1],i.rgb[2])
        frect(x_over, y_down, 105, 15)
        
        pen(0,0,0)
        text(i.name, 20, y_down+4)
        
        pen(15,15,15)
        frect(x_over+2,y_down+2,10,10)
        
        pen(0,0,0)
        if i.selected_order:
            text(str(i.selected_order), 8,y_down+3)
            
        if i.screen_order == g.cursor:
            if tick % 10 == 0:
                pen(0,0,0)
                rect(7,y_down+2,10,10)
        y_down += 15

    #other screen symbols
    pen(15,15,15)
    fpoly((115,55),(115,65),(120,60))
    fpoly((5,55),(5,65),(0,60))
    fpoly((55,5),(65,5),(60,0))
    fpoly((55,115),(65,115),(60,120))
    

# reset()

start()