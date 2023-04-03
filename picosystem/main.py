import time
import math
import gc

class ColorEntity:
    def __init__(self, screen_order, rgb, name, pen_white=False, selected_order=0):
        self.screen_order = screen_order
        self.rgb = rgb
        self.name = name
        self.pen_white = pen_white
        self.selected_order = selected_order
        self.time_counter = 0
    
    def update_time(self,t):
        self.time_counter += t        

class g:
    cursor = 0
    page = 0
    player_count = 0
    current_player = 0
    colors = [ColorEntity(0,(15,0,0), "Red", True),
              ColorEntity(1,(0,15,0), "Green"),
              ColorEntity(2,(0,0,15), "Blue", True),
              ColorEntity(3,(10,0,10), "Purple", True),
              ColorEntity(4,(0,0,0), "Black", True),
              ColorEntity(5,(15,15,15), "White"),
              ColorEntity(6,(14,14,3), "Yellow"),
              ColorEntity(7,(15,8,0), "Orange")]
    players = []

def reset():
    pass

def update(tick):
    
    if g.page == 1:
        if pressed(DOWN):
            g.cursor += 1
        if pressed(UP):
            g.cursor -= 1
    if g.page == 3:
        if pressed(DOWN):
            if (g.current_player + 1) < len(g.players):
                g.current_player += 1
            else:
                g.current_player = 1
        if pressed(UP): # on page 3 up always goes to pause?  Everything except up goes to next player?
            g.current_player -= 1
            if g.current_player < 0:
                g.current_player = 0
        if len(g.players) > 0:
            delta = time.ticks_diff(time.ticks_us(), g.start_time)
            if delta > 1000000:
                new_time = delta/1000000
                g.players[g.current_player].update_time(new_time)
                g.start_time = time.ticks_us()
        return
    
    if pressed(RIGHT):
        if g.page < 3:
            g.page += 1
    if pressed(LEFT):
        if g.page > 0:
            g.page -= 1
    
    if pressed(A):
        g.player_count += 1
        g.colors[g.cursor].selected_order = g.player_count
    
    #Reset Colors
    if pressed(Y):
        g.player_count = 0
        for i in g.colors:
            i.selected_order = g.player_count
    
    if g.page==2:
        if pressed(X):
            g.page=3
            g.players = [ColorEntity(0,(0,0,0), "PAUSE", True)]
            g.start_time = time.ticks_us()
            for i in g.colors:
                if i.selected_order > 0:
                    g.players.append(i)
            g.players.sort(key=lambda x: x.selected_order)
            
            g.current_player = 0
            counter = 0
            for i in g.players:
                i.screen_order = counter
                i.time_counter = 0
                counter += 1 
                print("players", i.name, "order", i.screen_order)
            
#     if g.page ==3:
#         if len(g.players) > 0:
#             delta = time.ticks_diff(time.ticks_us(), g.start_time)
#             if delta > 1000000:
#                 new_time = delta/1000000
#                 g.players[g.current_player].update_time(new_time)
#                 g.start_time = time.ticks_us()

def draw(tick):
    pen(0, 0, 0)
    clear()
    y_down = 5
    x_over = 5
    
    if g.page == 0:
        pen(12,12,12)
        t = ("\\penffff-- Time Totum --\\pencccc\n\nClick right to select order of players.  'A' to add player.  Then right again to start game timer.  Enjoy!!\n\nBattery: " + str(battery()) + "%\n\nFree Memory: " + str(math.floor(gc.mem_free()/1000)) + "kb")
        text(t, 5,5,100)
        pen(15,15,15)
        fpoly((115,55),(115,65),(120,60))
            
    if g.page == 1:    
        for i in g.colors:
            pen(i.rgb[0],i.rgb[1],i.rgb[2])
            frect(x_over, y_down, 105, 15)
            
            if i.pen_white:
                pen(15,15,15)
            else:
                pen(0,0,0)
            text(i.name, 20, y_down+4)
            
            pen(15,15,15)
            frect(x_over+2,y_down+2,10,10)
            
            pen(0,0,0)
            rect(x_over+2, y_down+2,10,10)
        
            if i.selected_order:
                text(str(i.selected_order), x_over+4,y_down+4)
                
            if i.screen_order == g.cursor:
                if tick % 5 == 0:
                    pen(1,1,1)
                    rect(x_over+3,y_down+3,8,8)
            y_down += 15

        #other screen symbols
        pen(11,11,11)
        fpoly((115,55),(115,65),(120,60))
        fpoly((5,55),(5,65),(0,60))
        fpoly((55,5),(65,5),(60,0))
        fpoly((55,115),(65,115),(60,120))
    
    if g.page == 2:
        pen(12,12,12)
        t = "Press...\n\nY to Reset Players.\n\nA to add player.\n\nUP/DOWN select player\n\nX to \\penffffStart!"
        text(t,15,10,100)
        pen(11,11,11)
        fpoly((115,55),(115,65),(120,60))
        fpoly((5,55),(5,65),(0,60))
        
    if g.page == 3:    
        for i in g.players:
            pen(i.rgb[0],i.rgb[1],i.rgb[2])
            if i.screen_order == g.current_player:
                frect(x_over, y_down, 105, 15+15)
                led(i.rgb[0]*6,i.rgb[1]*6,i.rgb[2]*6)
            else:
                frect(x_over, y_down, 105, 15)
            
            if i.pen_white:
                pen(15,15,15)
            else:
                pen(0,0,0)
            str_text = ""
            if i.name == "PAUSE":
                str_text = "PAUSE:"
            hour = math.floor(i.time_counter/3600)
            min = math.floor((i.time_counter - (hour *3600)) /60)
            sec = round(i.time_counter - (min * 60) - (hour * 3600))
            str_text += "    {0:01} : {1:02} : {2:02}".format(hour, min, sec)
            if i.screen_order == g.current_player:
                text(str_text, 20, y_down+4+7)
            else:
                text(str_text, 20, y_down+4)
            
            pen(15,15,15)
            frect(x_over+2,y_down+2,10,10)
            
            pen(0,0,0)
            rect(x_over+2, y_down+2,10,10)
        
            if i.selected_order:
                text(str(i.selected_order), x_over+4,y_down+4)
            
            if i.screen_order == g.current_player:
                if tick % 5 == 0:
                    pen(i.rgb[0],i.rgb[1],i.rgb[2])
                    frect(x_over,y_down,105,15+15)
                y_down += 15        
                
            y_down += 15

        #other screen symbols
        pen(15,15,15)
#         fpoly((5,55),(5,65),(0,60))
        fpoly((55,5),(65,5),(60,0))
        fpoly((55,115),(65,115),(60,120))
# reset()

start()