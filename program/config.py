"""Module to store configuration variables for the simulation."""

# Constants
FPS: int = 60  # can be adjusted using up/down arrow keys during the simulation
# Simulated seconds that pass per frame
TIMESTEP: float = 1e8  # ca. 3.17 years on earth
START_SCREEN_SIZE: tuple[int, int] = (700, 700)  # screen resolution in px
START_WORLD_SIZE: tuple[float, float] = (7e13, 7e13)  # in meters

# Newton's gravitational constant
G = 6.67430e-11  # in N m^2 kg^-2
# Scale factor so you can actually see the objects
SCALE_FACTOR: int = 2500

# Whether the starting velocities of the bodies should result in a perfect orbit
# If this is False, the velocities defined in `main.py` are used.
PERFECT_ORBIT: bool = True
