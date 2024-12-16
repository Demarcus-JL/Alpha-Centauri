import pygame

# Set up pygame window
WINDOW_SIZE = 720
pygame.init()
screen = pygame.display.set_mode((WINDOW_SIZE, WINDOW_SIZE))
clock = pygame.time.Clock()
FPS = 60
running = True

# list of bodies
bodies = []
# list of interactions
interactions = []
# timestep size
dt = 100  # s
# Scale factor to make objects visible
SCALE_FACTOR = 500


# world coordinates
x_min = -3.5*10**12.3
x_max = 3.5*10**12.3

y_min = -3.5*10**12.3
y_max = 3.5*10**12.3


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

    x_scr = (x - x_min) * WINDOW_SIZE / w
    y_scr = (y_max - y) * WINDOW_SIZE / h

    return x_scr, y_scr


# calculate distance between two bodies
def distance(bodyA, bodyB):
    return ((bodyA.x - bodyB.x) ** 2 + (bodyA.y - bodyB.y) ** 2) ** 0.5


# class for interactions between bodies
class Interaction:

    def __init__(self, bodyA, bodyB, k=30, color=(255, 255, 255)):
        self.bodyA = bodyA
        self.bodyB = bodyB

        # initial direct distance between bodies
        self.d = distance(bodyA, bodyB)

        self.k = k

        self.color = color

    # hooke law
    def update(self):

        dx = self.bodyA.x - self.bodyB.x  # x difference between bodies
        dy = self.bodyA.y - self.bodyB.y  # y difference between bodies

        d = (dx**2 + dy**2) ** 0.5  # current direct distance between bodies
        # self.d is the initial distance between bodies

        F = self.k * (d - self.d) / d

        self.bodyB.ax += F * dx / self.bodyB.m
        self.bodyB.ay += F * dy / self.bodyB.m

        self.bodyA.ax += -F * dx / self.bodyA.m
        self.bodyA.ay += -F * dy / self.bodyA.m

    def draw(self):
        print("unimplemented function")
        x1, y1 = to_pixel(self.bodyA.x, self.bodyA.y)
        x2, y2 = to_pixel(self.bodyB.x, self.bodyB.y)

        print("uninplemented function")


class Body:

    def __init__(self, x, y, vx=0, vy=0, r=0.5, m=1.0, color=(255, 255, 255)):
        self.x = x
        self.y = y

        self.vx = vx
        self.vy = vy

        self.ax = 0
        self.ay = 0

        self.m = m

        self.r = r

        self.color = color

    # perform euler cromer step
    def update(self, dt):

        self.vx = self.ax * dt + self.vx
        self.vy = self.ay * dt + self.vy

        self.x = self.vx * dt + self.x
        self.y = self.vy * dt + self.y

    def clear(self):
        self.ax = 0
        self.ay = 0

    # draw body on screen
    def draw(self):
        print("unimplemented")
        x, y = to_pixel(self.x, self.y)
        r_x, r_y = to_pixel(self.x + self.r, self.y + self.r)

        print("unimplemented")


while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # X clicked at top of window
            running = False

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                print("q key pressed, exiting...")
                running = False

    # Clear screen to black
    screen.fill("purple")

    # RENDER YOUR GAME HERE

    # flip() the display to put your work on screen
    pygame.display.flip()

    clock.tick(FPS)

pygame.quit()
