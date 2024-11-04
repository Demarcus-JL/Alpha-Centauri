# list of bodies
bodies = []

# list of interactions
interactions = []

# timestep size
dt = 10  # s


# world coordinates
x_min = -1.75122595*10**12
x_max = 1.75122595*10**12

y_min = -1.75122595*10**12
y_max = 1.75122595*10**12


# screen dimensions in px
screen_width = None
screen_height = None


# convert meter to pixels
def to_pixel(x, y):
    """Return the coordinates in pixels, generated from the metric system.

    Args:
        x (int): x coordinate in m
        y (int): y coordinate in m

    Returns:
        tuple(int, int): coordinates in px
    """
    w = x_max - x_min  # width of the world in m
    h = y_max - y_min  # height of the world in m

    x_scr = (x - x_min) * screen_width / w
    y_scr = (y_max - y) * screen_height / h

    return x_scr, y_scr


# calculate distance between two bodies
def distance(bodyA, bodyB):
    return ((bodyA.x - bodyB.x) ** 2 + (bodyA.y - bodyB.y) ** 2) ** 0.5


# class for interactions between bodies
class Interaction:

    def __init__(self, bodyA, bodyB, k=30, color=(255, 255, 255)):
        self.bodyA = bodyA
        self.bodyB = bodyB

        self.d = distance(bodyA, bodyB)

        self.k = k

        self.color = color

    # hooke law
    def update(self):

        rx = self.bodyA.x - self.bodyB.x
        ry = self.bodyA.y - self.bodyB.y

        d = (rx**2 + ry**2) ** 0.5

        F = self.k * (d - self.d) / d

        self.bodyB.ax += F * rx / self.bodyB.m
        self.bodyB.ay += F * ry / self.bodyB.m

        self.bodyA.ax += -F * rx / self.bodyA.m
        self.bodyA.ay += -F * ry / self.bodyA.m

    def draw(self):
        stroke(self.color[0], self.color[1], self.color[2])

        x1, y1 = to_pixel(self.bodyA.x, self.bodyA.y)
        x2, y2 = to_pixel(self.bodyB.x, self.bodyB.y)

        line(x1, y1, x2, y2)


class Body:

    def __init__(self, x, y, vx=0, vy=0, r=0.5, m=1.0, fixed=False, color=(255, 255, 255), scale_factor=1):
        self.x = x
        self.y = y

        self.vx = vx
        self.vy = vy

        self.ax = 0
        self.ay = 0

        self.m = m

        self.r = r

        self.fixed = fixed

        self.color = color
        self.scale_factor = scale_factor

    # perform euler cromer step
    def update(self, dt):

        if not self.fixed:
            self.vx = self.ax * dt + self.vx
            self.vy = self.ay * dt + self.vy

            self.x = self.vx * dt + self.x
            self.y = self.vy * dt + self.y

    def clear(self):
        self.ax = 0
        self.ay = 0

    # draw body on screen
    def draw(self):
        fill(self.color[0], self.color[1], self.color[2])

        x, y = to_pixel(self.x, self.y)
        r_x, r_y = to_pixel(self.x + self.r, self.y + self.r)

        circle(x, y, self.scale_factor * (2 * (r_x - x)))

# ------------
# Processing-specific functions
# ------------

def setup():
    global screen_width, screen_height
    # screen dimensions in px
    screen_width = displayWidth
    screen_height = displayHeight
    fullScreen()
    frameRate(120)

    alpha_A = Body(x=0, y=0,
                   vx=0, vy=0,
                   r=(8.511*10**8),
                   m=(2.188*10**30),
                   fixed=True,
                   scale_factor=300,
                   color=(0, 0, 255),
                   )
    bodies.append(alpha_A)

    alpha_B = Body(x=0, y=(3.501*10**12),
                   vx=0, vy=0,
                   r=(6.008*10**8),
                   m=(1.804*10**30),
                   fixed=True,
                   color=(0, 255, 0),
                   scale_factor=500,
                   )
    bodies.append(alpha_B)

    interaction_12 = Interaction(alpha_A, alpha_B, k=200, color=(255, 0, 0))
    interactions.append(interaction_12)


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

        # # drag
        # k = 0.01
        # body.ax += -k * body.vx
        # body.ay += -k * body.vy

        body.update(dt)
        body.draw()

    for interaction in interactions:
        interaction.draw()
