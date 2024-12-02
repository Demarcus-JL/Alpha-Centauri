"""
ALL POSITION VECTORS HAVE THEIR ORIGIN IN THE BOTTOM LEFT

ORIGIN = BOTTOM LEFT = (0, 0)
"""

# region constants
TIMESTEP = 1 #100  # s
SCALE_FACTOR = 1 #500  # Magnification of objects to account for large distances
VIEWPORT = (-10, 10) #(-3.5 * 10**12.3, 3.5 * 10**12.3)  # viewport limits in m for a square viewport
# endregion constants


def m_to_px(pos):
    """Convert metric units to pixels for the specified display

    Args:
        pos (Vector): position vector of the point, in m

    Returns:
        Vector: position vector of the point, in px
    """
    print("in m_to_px function")
    view_size = VIEWPORT[1] - VIEWPORT[0]  # viewport sidelength in m
    print("view_size =", view_size)
    #       (distance from edge) *     (pixels per m)
    result = (pos - VIEWPORT[0]) * SCREEN_SIZE / view_size
    print("result =", result)
    return result


class Vector:
    """Vector class to make the calculation of speeds and positions easier"""
    def __init__(self, dx, dy):
        self.dx = dx
        self.dy = dy
        self.magnitude = (self.dx**2 + self.dy**2) ** 0.5

    def __repr__(self):
        """String representation of the Vector"""
        return "Vector(" + str(self.dx) + ", " + str(self.dy) + ")"

    def __iter__(self):
        """Define iterable behaviour of the vector so it can be treated and unpacked like a tuple"""
        return iter((self.dx, self.dy))

    def __add__(self, obj):
        """Dunder method for adding two vectors

        Args:
            obj (Vector): The vector to be added

        Returns:
            Vector: resulting vector
        """
        return Vector(self.dx + obj.dx, self.dy + obj.dy)

    def __sub__(self, obj):
        """Dunder method for subtracting two vectors

        Args:
            obj (Vector): The vector to be subtracted

        Returns:
            Vector: resulting vector
        """
        return Vector(self.dx - obj.dx, self.dy - obj.dy)

    def __mul__(self, k):
        """Dunder method for multiplying a Vector by a scalar

        Args:
            k (float): scalar to be multiplied by

        Returns:
            Vector: resulting vector
        """
        return Vector(self.dx * k, self.dy * k)

    def __truediv__(self, k):
        """Dunder method for dividing a Vector by a scalar

        Args:
            k (float): scalar to be divided by

        Returns:
            Vector: resulting vector
        """
        return Vector(self.dx / k, self.dy / k)


class Body:
    """Body class for a celestial object"""
    def __init__(
        self,
        start_position=Vector(0, 0),
        start_velocity=Vector(0, 0),
        start_acceleration=Vector(0, 0),
        radius=10**20,
        mass=10**30,
        colour=(255, 255, 255),
    ):

        self.pos = start_position  # position vector, in m
        self.v = start_velocity  # vector, in m/s
        self.a = start_acceleration  # vector, in m/s^2

        self.r = radius  # scalar, in m
        self.m = mass  # scalar, in kg

        self.colour = colour  # RGB value

    def update(self, dt):
        """Update parametres of body with given time accurracy

        Args:
            dt (float): time in seconds over which the changes happen
        """
        print("in update function")
        self.v += self.a * dt
        self.pos += self.v * dt
        print("exiting update function")
        print("resulting parametres: v =", self.v, "pos =", self.pos, "r =", self.r)

    def draw(self):
        """Draw the body on the screen, scaling it if specified"""
        print("in body.draw function")
        fill(self.colour[0], self.colour[1], self.colour[2])  # unpack the tuple into the fill function (WARNING: MIGHT NOT WORK ON PYPROCESSING)
        print("set fill colour")
        print("coordinates:", str(self.pos.dx), str(self.pos.dy))
        circle(self.pos.dx + 1, self.pos.dy + 1, SCALE_FACTOR * 2 * m_to_px(self.radius).dx)  # unpack the tuple into the first 2 args of the circle functoin (WARNING: MIGHT NOT WORK ON PYPROCESSING)
        print("circle drawn")


class Interaction:
    def __init__(
        self,
        bodies,  # Tuple of two Body() instances to interact with each other
        colour=(255, 255, 255),  # Colour to mark the axis and objects for an interaction
    ):
        if len(bodies) != 2:
            raise ValueError("The first argument must be a tuple containing 2 Body() instances")
        self.bodies = bodies
        print("defined bodies in interaction:", str(bodies))
        self.colour = colour

    def update(self):
        """Update attributes of each body in the interaction
        
        Use Newton's gravitational constant to calculate force of attraction based on mass and distance:
        `F = G * (m1 * m2) / r**2`
        """
        print("interaction update function entered")
        # Get distance differences in x and y components
        dx = self.bodies[0].pos.dx - self.bodies[1].pos.dx
        dy = self.bodies[0].pos.dy - self.bodies[1].pos.dy
        print("got dy and dx")
        # Get direct distance between the two bodies
        r = ((dx) ** 2 + (dy) ** 2) ** 0.5
        print("got distance")
        # Get magnitude of resulting force vector
        F = 6.674 * 10 ** -11 * ((self.bodies[0].m * self.bodies[1].m) / (r ** 2))
        print("got vector magnitude")
        # Get angle of interaction with respect to x-axis
        phi = arcsin(dy/dx)
        print("got phi")
        # Turn resulting vector into a vector class
        F_vec = Vector(cos(phi) * F, sin(phi) * F)
        print("got resulting vector")

        # Apply force to bodies
        for body in self.bodies:
            body.a = F_vec / body.m
        
        print("applied force to all bodies, exiting update function...")

    def draw(self):
        """Draw the interaction, marking the involved bodies and the path of force"""
        # Set colour
        stroke(*self.colour)
        for body in self.bodies:
            circle(*m_to_px(body.pos), b = SCALE_FACTOR * m_to_px(body.r).dx + 3)

        # Had to do it this way because pyprocessing doesn't support more than one tuple unpacking in function call
        pos1x, pos1y = m_to_px(self.bodies[0].pos)
        pos2x, pos2y = m_to_px(self.bodies[1].pos)
        line(pos1x, pos1y, pos2x, pos2y)


# region processing-specific functions

def setup():
    global SCREEN_SIZE, bodies, interactions
    SCREEN_SIZE = displayHeight  # only for square viewport

    bodies = []
    interactions = []

    # Set up alpha centauri A
    bodies.append(
        Body(
            start_position=(Vector(1, 1)),
            radius=2, #(8.511*10**8),
            mass=40, #(2.188*10**30),
            colour=(0, 0, 255)
        )
    )

    # # Set up alpha centauri B
    # bodies.append(
    #     Body(
    #         radius=(6.008*10**8),
    #         mass=(1.804*10**30),
    #         colour=(0, 255, 0)
    #     )
    # )

    # interactions.append(
    #     Interaction(bodies, colour=(255, 0, 0))
    # )

    # print("setup completed")


def draw():
    """Draw function is called every tick by processing"""
    background(0)  # clear background to black
    print("in draw loop")

    for interaction in interactions:
        print("in 1st interaction loop")
        interaction.update()
    
    for body in bodies:
        print("in body loop -", body)
        body.update(TIMESTEP)
        body.draw()

    for interaction in interactions:
        print("in 2nd interaction loop")
        interaction.draw()

# endregion processing-specific functions
