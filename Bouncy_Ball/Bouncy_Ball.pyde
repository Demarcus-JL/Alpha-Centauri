def setup():
    size(500,500)
    
x = 250
y = 250

vx = 10
vy = 10

ax = 0
ay = 0 

dt = 0.5
    
    
def draw():
    global x, y, vx, vy, ax, ay
    background(0)
    
    #konstanste beschleunigung nach unten
    ax = 0
    ay = -1
    

    #k = 0.01
    #ax = k*(250-x)
    #ay = -k*(250-y)

    vx = ax*dt + vx
    vy = ay*dt + vy
    
    x = vx*dt + x
    y = -vy*dt + y
    
    if x > 500:
        vx = -vx
        x = 500
    elif x < 0:
        vx = -vx
    #  x = 500
        
        
    if y > 350:
        vy = -vy
        y = 350
    #elif y < 0:
    #   y = 500

    
    fill(255)
    circle(x,y,10)
    
    rect(0,350,500,150)
    

    
