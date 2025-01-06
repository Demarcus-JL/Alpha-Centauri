"""Module docsting here"""

import sys
import pygame
from config import FPS, TIMESTEP, START_SCREEN_SIZE, G
from objects import Vector, Body, Interaction, CursorPosition

# TODO: write unit tests for to_pixel, because I'm not sure it works properly

DEBUG: bool = False
SIMULATION_PAUSED: bool = False


# TODO remove this when done
def show_viewport() -> None:
    """Print the current viewport and screen limits to the console."""
    print(f"top right: {cursor_position.world_limits.dx:.2e} x {cursor_position.world_limits.dy:.2e}")
    print(f"bottom left: {cursor_position.world_start.dx:.2e} x {cursor_position.world_start.dy:.2e}")
    print()

pygame.init()  # Initialize pygame

# Initialize pygame-related stuff
screen: pygame.Surface = pygame.display.set_mode(START_SCREEN_SIZE, pygame.RESIZABLE)
clock: pygame.time.Clock = pygame.time.Clock()  # Clock to manage frame rate

# Data structures for simulation
bodies: list[Body] = []
interactions: list[Interaction] = []

# Viewport and screen sizes for scaling
cursor_position: CursorPosition = CursorPosition(
    Vector(screen.get_width(), screen.get_height()), Vector(7e12, 7e12)
)

def to_pixel(pos: Vector) -> Vector:
    """Return the coordinates as a Vector of px values, generated from the metric Vector as input.

    Args:
        pos (Vector): coordinates in m

    Returns:
        Vector: coordinates in px
    """
    relative_positions: Vector = pos / cursor_position.world_limits
    result = Vector(relative_positions.dx, 1 - relative_positions.dy) * cursor_position.screen_limits

    return result

def handle_keypress(key_event: pygame.event.Event) -> None:
    """Handle keypresses and act accordingly.

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


def zoom_board(percent: float) -> None:
    """Zoom board around the middle of the screen by a certain percentage.

    Args:
        percent (float): How much to zoom in/out, in %
    """
    # TODO make function work, probably move left first, then right
    zoom_factor: float = percent / 100
    # How much the world limits will change on each side in m
    change: Vector = cursor_position.total_world_size * (zoom_factor) / 2
    print(f"change in m: {change.dx:.2e} x {change.dy:.2e}")
    cursor_position.world_limits += change
    cursor_position.world_start -= change

def handle_window_resize() -> None:
    """Handle window resize events by updating the viewport and screen limits."""
    old_limits = cursor_position.screen_limits
    cursor_position.screen_limits = Vector(screen.get_width(), screen.get_height())
    relative_change: Vector = cursor_position.screen_limits / old_limits
    cursor_position.world_limits *= relative_change
    print("UPDATED viewport: "
            f"{cursor_position.world_limits.dx:.2e} x {cursor_position.world_limits.dy:.2e}")

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
        color=pygame.Color("#ffc300"),
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

    bodies[0].v.dy = (
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
            print(f"{"-" * 5} new keypress {"-" * 5} {event.unicode} ({event.key})")
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
