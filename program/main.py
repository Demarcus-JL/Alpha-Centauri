"""Module docsting here"""

import sys
import pygame
from config import FPS, TIMESTEP, START_SCREEN_SIZE, G, START_WORLD_SIZE
from objects import Vector, Body, Interaction, WorldParams

DEBUG: bool = True
SIMULATION_PAUSED: bool = False

# TODO remove this when done
def show_viewport() -> None:
    """Print the current viewport and screen limits to the console."""
    print(f"top right: {world_params.world_limits.dx:.2e} x {world_params.world_limits.dy:.2e}")
    print(f"bottom left: {world_params.world_start.dx:.2e} x {world_params.world_start.dy:.2e}")
    print()

# Initialize pygame-related stuff
pygame.init()
screen: pygame.Surface = pygame.display.set_mode(START_SCREEN_SIZE, pygame.RESIZABLE)
clock: pygame.time.Clock = pygame.time.Clock()  # Clock to manage frame rate

# Data structures for simulation
bodies: list[Body] = []
interactions: list[Interaction] = []

# Viewport and screen sizes for scaling
world_params: WorldParams = WorldParams(
    Vector(screen.get_width(), screen.get_height()), Vector(*(START_WORLD_SIZE))
)

# TODO: write unit tests for to_pixel, because I'm not sure it works properly
def to_pixel(pos: Vector) -> Vector:
    """Return the coordinates as a Vector of px values, generated from the metric Vector as input.

    Args:
        pos (Vector): coordinates in m

    Returns:
        Vector: coordinates in px
    """
    relative_positions: Vector = pos / world_params.world_limits
    result = Vector(relative_positions.dx, relative_positions.dy) * world_params.screen_size

    return result

def handle_keypress(key_event: pygame.event.Event) -> None:
    """Handle keypresses and act accordingly. Assumes that the passed event has a `key` attribute.

    Args:
        cursor_pos (CursorPosition): cursor position object
        key_event (pygame.event.Event): event object containing the key pressed
    """
    if key_event.key in (pygame.K_q, pygame.K_ESCAPE):
        # Exit when user presses Q or ESC
        finish()

    elif key_event.key == pygame.K_SPACE:
        global SIMULATION_PAUSED
        # toggle simulation pause
        SIMULATION_PAUSED = not SIMULATION_PAUSED
        print(f"Simulation {"paused" if SIMULATION_PAUSED else "resumed"}")

def handle_window_resize() -> None:
    """Handle window resize events by updating the viewport and screen limits."""
    old_limits = world_params.screen_size
    world_params.screen_size = Vector(screen.get_width(), screen.get_height())
    relative_change: Vector = world_params.screen_size / old_limits
    world_params.world_limits *= relative_change
    print("UPDATED viewport: "
            f"{world_params.world_limits.dx:.2e} x {world_params.world_limits.dy:.2e}")

# TODO working on this
def handle_world_zoom() -> None:
    # Get the outermost bodies in each direction and adjust world limits accordingly
    world_params.world_limits = world_params.world_limits + Vector(max(bodies, key=lambda body: body.pos.dx).pos.dx, max(bodies, key=lambda body: body.pos.dy).pos.dy)
    world_params.world_start = world_params.world_start - Vector(min(bodies, key=lambda body: body.pos.dx).pos.dx, min(bodies, key=lambda body: body.pos.dy).pos.dy)

def finish() -> None:
    """Quit the pygame application and terminate the program."""
    pygame.quit()
    sys.exit()

bodies.append(
    Body(
        name="Aplha Centauri A",
        pos=Vector(1.75e12, 1.5e12),
        v=Vector(0, 0),
        r=8.511e8,
        m=2.188e30,
        color=pygame.Color("#ffffff"), # ffc300
    )
)
bodies.append(
    Body(
        name="Alpha Centauri B",
        pos=Vector(5.25e12, 3.5e12),
        v=Vector(0, 0),
        r=6.008e8,
        m=1.804e30,
        color=pygame.Color("#ffd95c"),
    )
)

if not DEBUG:
    # Set starting velocities so that the bodies have a stable orbit
    DISTANCE = (bodies[0].pos - bodies[1].pos).magnitude

    bodies[0].v.dx = (
        (G * bodies[1].m) / DISTANCE * (bodies[0].m / (bodies[0].m + bodies[1].m))
    ) ** 0.5

    bodies[1].v.dy = -(
        ((G * bodies[0].m) / DISTANCE * (bodies[1].m / (bodies[0].m + bodies[1].m)))
        ** 0.5
    )

    interactions.append(Interaction(bodies[0], bodies[1], pygame.Color("#ff0000")))


while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:  # X clicked at top of window
            finish()

        elif event.type == pygame.KEYDOWN:  # Key pressed
            # Handle keypresses which might stop the simulation
            handle_keypress(event)

        elif event.type == pygame.WINDOWSIZECHANGED:  # Window resize
            handle_window_resize()

    # Clear screen to black
    screen.fill("black")

    for body in bodies:
        # Draw bodies even if simulation is paused to enable zooming when paused
        body.draw(screen)

    if SIMULATION_PAUSED:
        # skip continuing with the simulation
        continue

    # Update locations, velocities, etc.
    for interaction in interactions:
        interaction.update()

    # Update bodies for next frame
    for body in bodies:
        body.update(TIMESTEP)

    if DEBUG:
        # debug functionality here, not used at the moment
        pass

    # refresh the screen
    pygame.display.flip()
    # maintain frame rate
    clock.tick(FPS)
