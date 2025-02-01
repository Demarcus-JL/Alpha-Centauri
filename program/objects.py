"""Classes needed to make simulation work.

File includes:
- Vector: Vector class that supports addition, subtraction, scalar multiplication,
    scalar division and unpacking.
- Body: Round celestial object with mass, radius, position, velocity, acceleration and colour.
- Interaction: Class to manage interactions between Body instances, applying
    Newton's gravitational law.
"""

# Imports for type hinting
from __future__ import annotations
from typing import Any, Union, Iterator
import pygame
# To make Vector class work like a python iterable
from collections.abc import Sequence
# Imports for program logic
from math import atan2, cos, sin
from pygame import Color
from config import G, SCALE_FACTOR

# TODO remove this function
def show_params(world_params: WorldParams) -> None:
    print(f"world params:\n\ttotal size: {world_params.total_world_size}\n\tstart: {world_params.world_start}\n\tlimits: {world_params.world_limits}")


def to_pixel(pos: Vector, world_params: WorldParams) -> Vector:
    """Return the coordinates as a Vector of px values, generated from the metric Vector as input.

    Args:
        pos (Vector): coordinates in m

    Returns:
        Vector: coordinates in px
    """
    relative_positions: Vector = pos / world_params.total_world_size
    relative_start: Vector = -(world_params.world_start / world_params.total_world_size)
    result = (relative_start + relative_positions) * world_params.screen_size

    return result


class Vector(Sequence):
    """Vector class to make the calculation of speeds and positions easier"""

    def __init__(self, dx: float, dy: float) -> None:
        self.dx = dx
        self.dy = dy

    def __repr__(self) -> str:
        """String representation of the Vector"""
        return f"Vector({self.dx:.2e}, {self.dy:.2e})"

    def __getitem__(self, index: Union[int, slice]) -> Any:
        """Dunder method to enable indexing into a Vector

        dx is seen as self[0]
        dy is seen as self[1]

        Args:
            index (int): index that should be accessed

        Returns:
            float: value at that index
        """
        if isinstance(index, int):  # Handle integer indexing
            if index == 0:
                return self.dx
            if index == 1:
                return self.dy
            raise IndexError("Index out of range")

        if isinstance(index, slice):  # Handle slicing
            return [self.dx, self.dy][index]

        raise TypeError("Index must be an int or slice")

    def __len__(self) -> int:
        """Return the number of vector components in a 2D vector, which is always 2

        This function is needed to comply with the Sequence superclass, so it
        behaves like a python sequence.

        Returns:
            int: number of vector components
        """
        return 2

    def __iter__(self) -> Iterator[float]:
        """Define iterable behaviour of the vector so it can be treated and unpacked like a tuple"""
        return iter((self.dx, self.dy))

    def __hash__(self):
        return hash((self.dx, self.dy))

    def __eq__(self, value):
        if not isinstance(value, Vector):
            raise TypeError("Cannot compare Vectors with non-Vector types")

        return self.dx == value.dx and self.dy == value.dy

    def __add__(self, obj: Vector) -> Vector:
        """Dunder method for adding two vectors

        Args:
            obj (Vector): The vector to be added

        Returns:
            Vector: resulting vector
        """
        return Vector(self.dx + obj.dx, self.dy + obj.dy)

    def __sub__(self, obj: Vector) -> Vector:
        """Dunder method for subtracting two vectors

        Args:
            obj (Vector): The vector to be subtracted

        Returns:
            Vector: resulting vector
        """
        return Vector(self.dx - obj.dx, self.dy - obj.dy)

    def __mul__(self, k: Any[float, int, Vector]) -> Vector:
        """Dunder method for multiplying a Vector

        If the supplied factor is a float, simple scalar multiplication will take place.
        If the supplied factor is another Vector, a Vector with the individual components
        multiplied among each other will be returned.

        Args:
            k (Any[float, int, Vector]): scalar or vector to be multiplied by

        Returns:
            Vector: resulting vector
        """
        if isinstance(k, (float, int)):
            result: Vector = Vector(self.dx * k, self.dy * k)
        elif isinstance(k, Vector):
            result = Vector(self.dx * k.dx, self.dy * k.dy)
        else:
            raise ValueError(f"Unsupported operand types for `{type(k)}` and `Vector`")

        return result

    def __truediv__(self, k: Any[float, int, Vector]) -> Vector:
        """Dunder method for dividing a Vector

        If the supplied denominator is a float, simple scalar division will take place.
        If the supplied denominator is another Vector, a Vector with the individual components
        divided among each other will be returned.

        Args:
            k (Any[float, int, Vector]): scalar or vector to be divided by

        Returns:
            Vector: resulting vector
        """
        if isinstance(k, (float, int)):
            result: Vector = Vector(self.dx / k, self.dy / k)
        elif isinstance(k, Vector):
            result = Vector(self.dx / k.dx, self.dy / k.dy)
        else:
            raise ValueError(f"Unsupported operand types for `{type(k)}` and `Vector`")

        return result

    def __abs__(self) -> Vector:
        """Return the absolute value of the two vector components

        Returns:
            Vector: Vector containing the absolute values 
        """
        return Vector(abs(self.dx), abs(self.dy))

    def __neg__(self) -> Vector:
        """Return the negative value of the Vector

        Returns:
            Vector: Vector with negative components
        """
        return Vector(-self.dx, -self.dy)

    def __lt__(self, obj: Vector) -> bool:
        """Less-than operator for vectors

        Args:
            obj (Vector): Vector to be compared to

        Returns:
            bool: result of the operation
        """
        return self.magnitude < obj.magnitude

    def __gt__(self, obj: Vector) -> bool:
        """Greater-than operator for vectors

        Args:
            obj (Vector): Vector to be compared to

        Returns:
            bool: result of the operation
        """
        return self.magnitude > obj.magnitude

    @property
    def magnitude(self) -> float:
        """Current magnitude of the vector

        Returns:
            float: magnitude of the vector
        """
        return (self.dx**2 + self.dy**2) ** 0.5

    @property
    def unit(self) -> Vector:
        """Compute the Unit vector of the direction in which the full vector points

        Returns:
            Vector: Unit vector showing direction
        """
        if self.magnitude == 0:
            raise ValueError("Cannot normalize a zero vector")

        return Vector(self.dx / self.magnitude, self.dy / self.magnitude)

    @property
    def inverted(self) -> Vector:
        """Return the vector with swapped components

        Returns:
            Vector: Vector with swapped components
        """
        return Vector(self.dy, self.dx)


class Body:
    """Body class for round celestial objects"""

    def __init__(
        self,
        name: str,
        pos: Vector,
        v: Vector,
        r: float,
        m: float,
        color: Color = Color("#ffffff"),
    ) -> None:
        """Body class for round celestial objects

        Args:
            pos (Vector): position vector of starting point (in m)
            v (Vector): vector describing initial velocity (in m/s)
            r (float, optional): radius (in m)
            m (float, optional): mass (in kg)
            color (float, optional): what color the object should have. Defaults to white.
        """
        self.pos: Vector = pos
        self.v: Vector = v
        self.a: Vector = Vector(0, 0)

        self.m = m
        self.r = r
        self.color = color
        self.name = name

    def __repr__(self):
        return f"{self.name}@{self.pos} | v = {self.v}"

    def update(self, dt: float) -> None:
        """Update the position and velocity based on acceleration.

        Args:
            dt (float): timestep since last calculation
        """
        self.pos += self.v * dt
        self.v = self.a * dt + self.v

    def draw(self, screen: pygame.Surface, world_params: WorldParams) -> None:
        """Draw the body on the screen

        Args:
            screen (Surface): pygame screen object to draw on
            cursor_pos (CursorPosition): cursor position object
        """
        pygame.draw.circle(
            screen,
            self.color,
            to_pixel(self.pos, world_params),
            to_pixel(Vector(self.r * SCALE_FACTOR, 0), world_params).dx,
        )


class Interaction:
    """Class to manage interactions between two Body objects"""

    def __init__(
        self,
        obj1: Body,
        obj2: Body,
    ) -> None:
        """Class to manage interactions between two Body objects

        Args:
            obj1 (Body): first Body in the interaction
            obj2 (Body): second Body in the interaction
            color (list[int, int, int], optional): Mark the objects in the interaction.
                Defaults to (255, 255, 255).
        """
        self.body1 = obj1
        self.body2 = obj2
        self.bodies = (self.body1, self.body2)

        # Initial direct distance between bodies
        self.initial_distance: float = (self.body1.pos - self.body2.pos).magnitude

    @property
    def current_distance(self) -> float:
        """Current distance between the two objects"""
        return (self.body1.pos - self.body2.pos).magnitude

    def update(self) -> None:
        """Update the acceleration values of the interaction objects

        Use Newton's gravitational constant to calculate force of attraction based on
        mass and distance:
        `F = G * (m1 * m2) / r**2`

        Then use `F = m * a` to find the correct acceleration value

        Args:
            dt (float): timestep since last calculation
        """
        return  # TODO remove this line
        # Get the magnitude of the acting force
        force_magnitude: float = G * (self.body1.m * self.body2.m) / self.current_distance**2
        # Difference in positions, defined in a vector
        delta_pos: Vector = self.body1.pos - self.body2.pos
        # Angle between the two points
        phi: float = atan2(delta_pos.dy, delta_pos.dx)
        # Get Vector with direction
        directed_force: Vector = Vector(
            cos(phi) * force_magnitude, sin(phi) * force_magnitude
        )

        # Apply force to acceleration for both bodies
        self.body1.a = -directed_force / self.body1.m
        self.body2.a = directed_force / self.body2.m

    def follow_bodies(self, world_params: WorldParams) -> WorldParams:
        for body in self.bodies:
            shift = (body.v * SCALE_FACTOR**6 * 50 / world_params.total_world_size)  # TODO find better v-dependent formula
            if world_params.world_limits.dy - body.pos.dy < world_params.total_world_size.dy * 0.1:
                print(f"{body.name} moved the viewport down by {shift.dy} with speed {body.v}")
                # Move the viewport down to keep bodies in view
                world_params.world_limits.dy += shift.dy
                world_params.world_start.dy += shift.dy
            elif world_params.world_limits.dy - body.pos.dy > world_params.total_world_size.dy * 0.9:
                print(f"{body.name} moved the viewport up by {shift.dy}")
                # Move the viewport up to keep bodies in view
                world_params.world_limits.dy -= shift.dy
                world_params.world_start.dy -= shift.dy

            if world_params.world_limits.dx - body.pos.dx < world_params.total_world_size.dx * 0.1:
                print(f"{body.name} moved the viewport right by {shift.dx}")
                world_params.world_limits.dx += shift.dx
                world_params.world_start.dx += shift.dx
            elif world_params.world_limits.dx - body.pos.dx > world_params.total_world_size.dx * 0.9:
                print(f"{body.name} moved the viewport left by {shift.dx}")
                world_params.world_limits.dx -= shift.dx
                world_params.world_start.dx -= shift.dx

        return world_params


class WorldParams:
    """Class to manage size-related world data in the simulation"""
    def __init__(self, screen_size: Vector, world_limits: Vector, world_start: Vector = Vector(0, 0)) -> None:
        """Class that holds world-sizing-related values for the simulation.

        Args:
            screen_size (Vector): variable that always holds the current screen size (px)
            world_limits (Vector): variable that always holds the current world limits (m)
            world_start (Vector, optional): variable that always holds the current world start (m). Defaults to Vector(0, 0).
        """
        self.screen_size: Vector = screen_size
        self.world_limits: Vector = world_limits
        self.world_start: Vector = world_start

    def __eq__(self, value: WorldParams) -> bool:
        """Equality check for world parametres. Only returns True if all params are the same

        Args:
            value (WorldParams): The WorldParams instance to be checked against

        Returns:
            bool: If both instances have the same values
        """
        if not isinstance(value, WorldParams):
            raise TypeError(f"Cannot compare WorldParams with {type(value)} type")
        return (self.world_limits, self.world_start) == (value.world_limits, value.world_start)

    @property
    def total_world_size(self) -> Vector:
        """Get the total world size in m

        Returns:
            Vector: total world size
        """
        return self.world_limits - self.world_start
