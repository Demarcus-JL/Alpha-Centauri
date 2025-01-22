"""Module to store configuration variables for the simulation."""

# Constants
FPS: int = 60
# Simulated seconds that pass between simulation steps
TIMESTEP: float = 1e7  # ca. 3.8 months on earth
START_SCREEN_SIZE: tuple[int, int] = (400, 400)  # screen resolution in px
START_WORLD_SIZE: tuple[float, float] = (7e12, 7e12)  # in meters

# Newton's gravitational constant
G = 6.67430e-11  # in N m^2 kg^-2
# Scale factor so you can actually see the objects
SCALE_FACTOR: int = 500
