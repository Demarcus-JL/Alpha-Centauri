import random


# list of bodies
bodies = []

# list of interactions
interactions = []

# timestep size
dt = 0.0083 # s


# world coordinates
x_min = -10.0
x_max = 10.0

y_min = -10.0
y_max = 10.0


# screen dimensions
screen_width = 500
screen_height = 500


# convert meter to pixels
def meter_to_pixel(x,y):
    w = x_max - x_min
    h = y_max - y_min
    
    x_scr = (x - x_min) * screen_width / w
    y_scr = (y_max - y) * screen_height / h
    
    return x_scr, y_scr


# calculate distance between two bodies
def distance(bodyA, bodyB):
    return ( (bodyA.x - bodyB.x)**2 + (bodyA.y - bodyB.y)**2 )**0.5


# class for interactions between bodies
class Interaction:
    
    def __init__(self, bodyA, bodyB, k = 30):
        self.bodyA = bodyA
        self.bodyB = bodyB
        
        
        self.d = distance(bodyA,bodyB)
        
        self.k = k
        
        self.color = (255, 255, 255)
    
    
    # hooke law
    def update(self):
        
        rx = self.bodyA.x - self.bodyB.x
        ry = self.bodyA.y - self.bodyB.y
        
        d = ( rx**2 + ry**2 )**0.5

        F = self.k * (d - self.d) / d
    
        self.bodyB.ax += F*rx/self.bodyB.m
        self.bodyB.ay += F*ry/self.bodyB.m
        
        self.bodyA.ax += -F*rx/self.bodyA.m
        self.bodyA.ay += -F*ry/self.bodyA.m
    
    
    
    def draw(self):
        stroke(self.color[0], self.color[1], self.color[2])
        
        x1, y1 = meter_to_pixel(self.bodyA.x,self.bodyA.y)
        x2, y2 = meter_to_pixel(self.bodyB.x,self.bodyB.y)
        
        line(x1,y1,x2,y2)
    




class Body:
    
    def __init__(self, x, y, vx=0, vy=0, r=0.5, m=1.0, fixed=False):
        self.x = x
        self.y = y
        
        self.vx = vx
        self.vy = vy
        
        self.ax = 0
        self.ay = 0
        
        self.m = m
        
        self.r = r
        
        self.fixed = fixed
        
        self.color = (255, 255, 255)
    
    
    
    # perform euler cromer step
    def update(self, dt):
        
        if not self.fixed:
            self.vx = self.ax*dt + self.vx
            self.vy = self.ay*dt + self.vy
        
            self.x = self.vx*dt + self.x
            self.y = self.vy*dt + self.y
            
    def clear(self):
        self.ax = 0
        self.ay = 0
            
        
            
    
    
    # draw body on screen
    def draw(self):
        fill(self.color[0], self.color[1], self.color[2])
        
        x, y = meter_to_pixel(self.x,self.y)
        r_x, r_y = meter_to_pixel(self.x+self.r,self.y+self.r)
        
        circle(x, y, 2*(r_x-x))
        
    



def setup():
    size(500,500)
    frameRate(120)

    body_1 = Body(0, 2, fixed=True)
    bodies.append(body_1)
    
    body_2 = Body(0, 6, m=0.1)
    bodies.append(body_2)
    
    body_3 = Body(4, 6, m=0.1)
    bodies.append(body_3)
    
    interaction_12 = Interaction(body_1, body_2, k = 200)
    interactions.append(interaction_12)
    
    interaction_23 = Interaction(body_2, body_3, k = 200)
    interactions.append(interaction_23)

   

def draw():

    background(0)

    # clear all accelerations
    for body in bodies:
        body.clear()

    # calculate interactions
    for interaction in interactions:
        interaction.update()
    
    for body in bodies:
        
        # gravity
        body.ax += 0
        body.ay += -9.81 # m/s^2
        
        # drag
        k = 0.01
        body.ax += -k*body.vx
        body.ay += -k*body.vy
        
    
        body.update(dt)
        body.draw()
        
    for interaction in interactions:
        interaction.draw()
        
