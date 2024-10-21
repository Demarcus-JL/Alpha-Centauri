import random
import time

t_buffer = time.time()


# list of bodies
bodies = []

# list of interactions
interactions = []



# timestep size
dt = 0.0083  # s

# set coordinates
x_min = -10.0 # meter
x_max = 10.0  # meter
y_min = -10.0 # meter
y_max = 10.0  # meter

screen_width = 500  # pixel
screen_height = 500 # pixel



# convert meter to pixel
def meter_to_screen(x,y):
    x_screen = (x - x_min) * screen_width / (x_max - x_min)
    y_screen = (y_max - y) * screen_height / (y_max - y_min)
    
    return x_screen, y_screen


class Body:
    
    def __init__(self, x, y, vx=0, vy=0):
        self.x = x
        self.y = y
        
        self.vx = vx
        self.vy = vy
        
        self.ax = 0
        self.ay = 0
        
        self.r = 1 # m
        self.m = 1   # kg
        
        self.color = (255, 255, 255)
    
    
    # perform euler cromer step
    def update(self, dt):
         
        self.vx = self.ax*dt + self.vx
        self.vy = self.ay*dt + self.vy
    
        self.x = self.vx*dt + self.x
        self.y = self.vy*dt + self.y
    
    
    # draw body on screen
    def draw(self):
        fill(self.color[0], self.color[1], self.color[2])
        
        x, y = meter_to_screen(self.x, self.y)
        
        circle(x, y, 10)
        
    

class Interaction:
    def __init__(self, body1, body2):
        self.body1 = body1
        self.body2 = body2
        
    def update(self):
        d = (self.body1.x - self.body2.x)**2 + (self.body1.y - self.body2.y)**2
        d = d**0.5
        
        self.body1.ax = 0
        self.body1.ay = 0
        self.body2.ax = 0
        self.body2.ay = 0
        
        if d < self.body1.r + self.body2.r:
            F = 1.0/d**2
            
            dx = self.body1.x - self.body2.x
            dy = self.body1.y - self.body2.y
            
            self.body1.ax = F/self.body1.m*dx
            self.body1.ay = F/self.body1.m*dy
            
            self.body2.ax = -F/self.body2.m*dx
            self.body2.ay = -F/self.body2.m*dy
        
        
        


def setup():
    size(500,500)

    frameRate(120)
    
    for i in range(1,9):
        for j in range(1,9):
        
            body = Body(-9+2*i,-9+2*j, vx=1-2*random.random(), vy=1-2*random.random())
            bodies.append(body)
            
    
    for bodyA in bodies:
        for bodyB in bodies:
            
            interactions = Interaction(bodyA,bodyB)
            interactions.append(interactions)
    


def draw():
    global t_buffer
    
    background(0)

    #print(time.time() - t_buffer)
    t_buffer = time.time()
    
    for interaction in interactions:
        interaction.update()
    
    
    for body in bodies:
        
        # Ball auf der Erde
        #body.ax += 0
        #body.ay += -9.81 # m/s^2
        
        # periodic boundary
        '''
        if body.y > y_max:
            body.y = y_min
        elif body.y < y_min:
            body.y = y_max
            
        if body.x > x_max:
            body.x = x_min
        elif body.x < x_min:
            body.x = x_max
        '''
        
        # floor
    
        if body.y < x_min:
            body.y = x_min
            body.vy = -body.vy
        elif body.y > x_max:
            body.y = x_max
            body.vy = -body.vy
            
        # wall
        if body.x > x_max:
            body.x = x_max
            body.vx = -body.vx
        elif body.x < x_min:
            body.x = x_min
            body.vx = -body.vx
            
        # drag
        k = 0
        body.ax += -k*body.vx
        body.ay += -k*body.vy
    

        body.update(dt)
        body.draw()
        
