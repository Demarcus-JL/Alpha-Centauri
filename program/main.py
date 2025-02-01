"""Main progam logic including event loop and key handlers for pygame."""

from sys import exit as sys_exit
import pygame
from config import FPS, TIMESTEP, START_SCREEN_SIZE, G, START_WORLD_SIZE, PERFECT_ORBIT
from objects import Vector, Body, Interaction, WorldParams, draw_grid


def handle_keypress(key_event: pygame.event.Event) -> None:
    """Handle keypresses and act accordingly. Assumes that the passed event has a `key` attribute.

    Args:
        cursor_pos (CursorPosition): cursor position object
        key_event (pygame.event.Event): event object containing the key pressed
    """
    global FPS
    if key_event.key in (pygame.K_q, pygame.K_ESCAPE):
        # Exit when user presses Q or ESC
        finish()

    elif key_event.key == pygame.K_SPACE:
        global SIMULATION_PAUSED
        # toggle simulation pause
        SIMULATION_PAUSED = not SIMULATION_PAUSED

    elif key_event.key == pygame.K_DOWN:
        FPS = max(FPS - 5, 1)
        print("FPS:", FPS)
    elif key_event.key == pygame.K_UP:
        FPS += 5
        print("FPS:", FPS)

    elif key_event.key == pygame.K_f:
        # Enter fullscreen
        pygame.display.set_mode((0, 0), pygame.FULLSCREEN)


def handle_window_resize() -> None:
    """Handle window resize events by updating the viewport and screen limits."""
    old_limits: Vector = world_params.screen_size
    world_params.screen_size = Vector(screen.get_width(), screen.get_height())
    relative_change: Vector = world_params.screen_size / old_limits
    world_params.world_limits *= relative_change


def finish() -> None:
    """Quit the pygame application and terminate the program.
    
    Also displays the amount of equivalent earth years that have been simulated since the beginning.
    """
    # 31'556'952 seconds in a year, accounting for leap years
    # Replace "," delimiter with "'" to adapt to european way of writing
    print(f"\nCirca {f"{round(rounds * TIMESTEP / 31_556_952):,}".replace(",", "'")} earth years have been simulated.")
    pygame.quit()
    sys_exit(0)


# Pygame-related stuff
pygame.init()
screen: pygame.Surface = pygame.display.set_mode(START_SCREEN_SIZE, pygame.RESIZABLE)
clock: pygame.time.Clock = pygame.time.Clock()  # Clock to manage frame rate
pygame.display.set_caption("Alpha Centauri")
icon = pygame.image.load("../thumbnail.png")
pygame.display.set_icon(icon)

# Initialize data structures for simulation
bodies: list[Body] = []
interactions: list[Interaction] = []

# Simulation state
SIMULATION_PAUSED: bool = False
rounds: int = 0  # To display passed time at the end


# Viewport and screen sizes for scaling
world_params: WorldParams = WorldParams(
    Vector(screen.get_width(), screen.get_height()),
    Vector(*(START_WORLD_SIZE)),
)

if __name__ == "__main__":
    # Add stars to the simulation
    bodies.append(
        Body(
            name="Alpha Centauri A",
            pos=Vector(
                1.75e13, 3.5e13
            ),
            v=Vector(0, 0),
            r=8.511e8,
            m=2.188e30,
            color=pygame.Color("#ffffff"),  # f9ff86
        )
    )
    bodies.append(
        Body(
            name="Alpha Centauri B",
            pos=Vector(
                5.25e13, 3.5e13
            ),
            v=Vector(0, 0),
            r=6.008e8,
            m=1.804e30,
            color=pygame.Color("#e3b213"),
        )
    )

    if PERFECT_ORBIT:
        # Set starting velocities so that the bodies have a stable orbit
        DISTANCE = (bodies[0].pos - bodies[1].pos).magnitude

        bodies[0].v.dy = (
            (G * bodies[1].m) / DISTANCE * (bodies[0].m / (bodies[0].m + bodies[1].m))
        ) ** 0.5

        bodies[1].v.dy = -(
            ((G * bodies[0].m) / DISTANCE * (bodies[1].m / (bodies[0].m + bodies[1].m)))
            ** 0.5
        )

    interactions.append(Interaction(bodies[0], bodies[1]))

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # X clicked at top of window
                finish()

            elif event.type == pygame.KEYDOWN:  # Key pressed
                handle_keypress(event)

            elif event.type == pygame.WINDOWSIZECHANGED:  # Window resize
                handle_window_resize()

        # Clear screen to black
        screen.fill("black")
        draw_grid(screen, world_params, Vector(*START_WORLD_SIZE) / 10)

        if SIMULATION_PAUSED:
            # Don't update anything if simulation is paused
            continue

        for body in bodies:
            body.draw(screen, world_params)

        # Update interaction parameters and keep bodies in view
        for interaction in interactions:
            interaction.update()
            world_params = interaction.follow_bodies(world_params)

        # Update bodies for next frame
        for body in bodies:
            body.update(TIMESTEP)

        # refresh the screen
        pygame.display.flip()
        # maintain frame rate
        rounds += 1
        clock.tick(FPS)
