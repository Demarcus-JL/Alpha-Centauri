dda
x = 250
y = 250

vx = 0   # v = s/t
vy = 0


ax = 0 # a = v/t  => v = a*t
ay = 0

dt = 0.5

def setup():
    size (500,500)

def draw():
    global x, y,vx,vy
    
    ay = 3
    
    vx = vx + ax * dt
    vy = vy + ay * dt
    
    x = x + vx * dt 
    y = y + vy * dt
    
    if y > 300:
        y = 300
     
    background(51) 
    rect(x,y,20,20)
    
def keyPressed():
    global vx, vy
    if keyCode == 65: # A
        vx = -10
    elif keyCode == 68: # D
        vx = 10
    elif keyCode == 87: #W
        vy = -20
    elif keyCode == 83: #S
        ay = 2
        
def keyReleased():
    global ax,ay
    if keyCode == 65: #A
        vx = 0
    elif keyCode == 68: #D
        vx = 0
    elif keyCode == 87: #W
        ay = 0
    elif keyCode == 83: #S
        ay = 0
        
    
