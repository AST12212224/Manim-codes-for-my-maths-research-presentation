from manim import *
from math import cos, sin, tan, radians, pi
import numpy as np

class ReuleauxPolygonWithCenter(Scene):
    def construct(self):
        # Parameters
        initial_outer_side_length = 3  # Side length for the outer polygon
        max_sides = 3  # From triangle (3 sides) to other polygons

        # Function to calculate the radius of a polygon from its side length
        def polygon_radius_from_side(side_length, n):
            return side_length / (2 * sin(pi / n))

        # Function to calculate the vertices of a regular polygon
        def polygon_vertices(radius, n):
            return [
                radius * np.array([cos(2 * pi * i / n), sin(2 * pi * i / n), 0])
                for i in range(n)
            ]

        # Function to find the midpoint of a line segment
        def midpoint(point1, point2):
            return (point1 + point2) / 2

        # Initial calculations
        n = 3  # Start with a triangle
        outer_radius = polygon_radius_from_side(initial_outer_side_length, n)
        outer_vertices = polygon_vertices(outer_radius, n)  # Outer polygon vertices
        center_point = np.array([0, 0, 0])  # Center of the polygon
        closest_side_midpoint = midpoint(outer_vertices[0], outer_vertices[1])  # Midpoint of the closest side

        # Create the outer polygon
        outer_polygon = Polygon(*outer_vertices, color=BLUE, stroke_width=4)

        # Draw the center point
        center_dot = Dot(center_point, color=RED)

        # Create the line from the center to the closest side
        center_to_side_line = Line(center_point, closest_side_midpoint, color=GREEN, stroke_width=3)

        # Halve the line to create the radius for the inner circle
        halved_line_length = center_to_side_line.get_length() / 2
        halved_line = Line(center_point, center_point + halved_line_length * (closest_side_midpoint - center_point) / np.linalg.norm(closest_side_midpoint - center_point), color=YELLOW, stroke_width=3)

        # Draw the inner circle using the halved line as the radius
        inner_circle_radius = halved_line.get_length()
        inner_circle = Circle(radius=inner_circle_radius, color=BLUE, fill_opacity=0.5, stroke_width=4)

        # Animate the shapes step by step with specified timings
        self.play(Create(outer_polygon), run_time=4)  # Outer polygon animation for 4s
        self.play(Create(center_dot))  # Center dot (instantaneous for now)
        self.play(Create(center_to_side_line), run_time=4)  # Line from center to side for 4s
        self.play(Transform(center_to_side_line, halved_line), run_time=2.5)  # Line reducing to half for 2.5s
        self.play(Create(inner_circle))  # Inner circle creation (default timing)

        self.wait(10)  # Wait for 3 seconds at the end
