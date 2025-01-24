from manim import *
from math import cos, sin, tan, radians, pi
import numpy as np

class ReuleauxPolygonAlignedFix(Scene):
    def construct(self):
        # Parameters
        initial_outer_side_length = 3  # Side length for the outer polygon
        max_sides = 3  # From triangle (3) to decagon (10)

        # Function to calculate the radius of a polygon from its side length
        def polygon_radius_from_side(side_length, n):
            return side_length / (2 * sin(pi / n))

        # Function to calculate the inner side length based on the formula
        def inner_side_length(outer_side, n):
            return (outer_side * cos(radians(180 / n))) / (2 * (cos(radians(90 / n))**2))

        # Function to calculate the radius of the inner circle
        def inner_circle_radius(outer_side, n):
            return (outer_side / tan(radians(180 / n))) / 4

        # Function to calculate the vertices of a regular polygon
        def polygon_vertices(radius, n):
            return [
                radius * np.array([cos(2 * pi * i / n), sin(2 * pi * i / n), 0])
                for i in range(n)
            ]

        # Initial calculations
        n = 3  # Start with a triangle
        outer_radius = polygon_radius_from_side(initial_outer_side_length, n)
        inner_side = inner_side_length(initial_outer_side_length, n)
        inner_radius = polygon_radius_from_side(inner_side, n)
        inner_circle_r = inner_circle_radius(initial_outer_side_length, n)
        outer_vertices = polygon_vertices(outer_radius, n)  # Outer polygon vertices
        inner_vertices = polygon_vertices(inner_radius, n)  # Inner polygon vertices

        # Create the outer polygon using calculated vertices
        outer_polygon = Polygon(*outer_vertices, color=BLUE, stroke_width=4)

        # Create the inner circle
        inner_circle = Circle(radius=inner_circle_r, color=WHITE, stroke_width=4)

        # Create the inner polygon using calculated vertices
        inner_polygon = Polygon(*inner_vertices, color=BLUE, stroke_width=4)

        # Create a dot at the center
        center_dot = Dot(color=RED)

        # Play all animations together
        self.play(
            Create(outer_polygon),
            Create(inner_circle),
            Create(inner_polygon),
            FadeIn(center_dot),  # Add the center point
            run_time=2  # All shapes appear over 2 seconds
        )

        # Keep the shapes and center point on screen for an additional 4 seconds
        self.wait(5)
