from manim import *
from math import cos, sin, tan, radians, pi
import numpy as np

class ReuleauxPolygonAlignedFix(Scene):
    def construct(self):
        # Parameters for the outer triangle
        initial_outer_side_length = 3  # Side length for the outer polygon

        # Function to calculate the radius of a polygon from its side length
        def polygon_radius_from_side(side_length, n):
            return side_length / (2 * sin(pi / n))

        # Function to calculate the inner side length based on the formula
        def inner_side_length(outer_side, n):
            return (outer_side * cos(radians(180 / n))) / (2 * (cos(radians(90 / n))**2))

        # Initial calculations for the triangle
        n = 3  # Start with a triangle
        outer_radius = polygon_radius_from_side(initial_outer_side_length, n)
        inner_side = inner_side_length(initial_outer_side_length, n)
        inner_radius = polygon_radius_from_side(inner_side, n)

        # Calculate vertices for the triangles
        outer_vertices = [outer_radius * np.array([cos(2 * pi * i / n), sin(2 * pi * i / n), 0])
                          for i in range(n)]  # Outer triangle vertices
        inner_vertices = [inner_radius * np.array([cos(2 * pi * i / n), sin(2 * pi * i / n), 0])
                          for i in range(n)]  # Inner triangle vertices

        # Create the outer and inner triangles
        outer_polygon = Polygon(*outer_vertices, color=BLUE, stroke_width=4)
        inner_polygon = Polygon(*inner_vertices, color=RED, stroke_width=4)

        # Animation: Create the outer and inner triangles and hold for 2 seconds
        self.play(Create(outer_polygon), Create(inner_polygon), run_time=2)
        self.wait(2)  # Hold the triangles for 2 seconds

        # Now, continue with your existing code, directly showing the inner circle and inner polygon
        # Create the inner circle
        inner_circle_r = (initial_outer_side_length / tan(radians(180 / n))) / 4
        inner_circle = Circle(radius=inner_circle_r, color=WHITE, stroke_width=4)

        # Function to calculate the vertices of a regular polygon
        def polygon_vertices(radius, n):
            return [
                radius * np.array([cos(2 * pi * i / n), sin(2 * pi * i / n), 0])
                for i in range(n)
            ]

        # Calculate inner vertices again (this can be omitted if they are the same)
        inner_vertices = polygon_vertices(inner_radius, n)

        # Create the inner polygon using newly calculated vertices (if different)
        new_inner_polygon = Polygon(*inner_vertices, color=BLUE, stroke_width=4)

        # Show the inner circle and the inner polygon without creation animation
        self.add(inner_circle, new_inner_polygon)

        # Continue with any additional animations from your existing code that follows after this setup
