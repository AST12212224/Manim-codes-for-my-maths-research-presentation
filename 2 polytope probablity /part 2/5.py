from manim import *
from math import cos, sin, radians, pi, sqrt
import numpy as np

class TrianglePointConnection(Scene):
    def construct(self):
        # Parameters
        outer_side_length = 3  # Side length for the outer triangle

        # Function to calculate the radius of the polygon and vertices
        def polygon_radius_from_side(side_length, n):
            return side_length / (2 * sin(pi / n))

        def polygon_vertices(radius, n):
            return [
                radius * np.array([cos(2 * pi * i / n), sin(2 * pi * i / n), 0])
                for i in range(n)
            ]

        # Inner side length calculation using your formula
        def inner_side_length(outer_side, n):
            return (outer_side * cos(radians(180 / n))) / (2 * (cos(radians(90 / n))**2))

        def inner_polygon_vertices(outer_radius, n, outer_side):
            inner_side = inner_side_length(outer_side, n)
            inner_radius = inner_side / (2 * sin(pi / n))
            return polygon_vertices(inner_radius, n)

        # Outer triangle setup
        n = 3
        outer_radius = polygon_radius_from_side(outer_side_length, n)
        outer_vertices = polygon_vertices(outer_radius, n)
        outer_triangle = Polygon(*outer_vertices, color=BLUE, stroke_width=4)
        center_point = Dot(color=RED, radius=0.06)  # Smaller center point

        # Inner triangle setup with corrected size
        inner_vertices = inner_polygon_vertices(outer_radius, n, outer_side_length)
        inner_triangle = Polygon(*inner_vertices, color=WHITE, stroke_width=2)
        inner_points = VGroup(*[Dot(point, color=WHITE, radius=0.06) for point in inner_vertices])  # Smaller points

        # Add outer triangle and center point
        self.add(outer_triangle, center_point)
        self.play(Create(inner_triangle), run_time=1)  # Show inner triangle briefly
        self.play(Transform(inner_triangle, inner_points), run_time=1)  # Transform inner triangle into points
        self.add(inner_points)  # Ensure points remain visible

        # Draw lines from the center to each inner point
        lines_to_center = VGroup(*[Line(center_point.get_center(), point.get_center(), color=YELLOW) for point in inner_points])
        self.play(Create(lines_to_center), run_time=2)

        # Draw lines from inner points to the triangle sides
        lines_to_sides = VGroup()
        for i in range(n):
            side_start = outer_vertices[i]
            side_end = outer_vertices[(i + 1) % n]
            # Calculate position on the side at 1/3 the distance
            point_on_side_1 = side_start + (side_end - side_start) * (1/3)
            # Calculate rotation for 120 degrees to the right
            direction_vector = point_on_side_1 - side_start
            rotated_vector = np.array([
                cos(radians(120)) * direction_vector[0] - sin(radians(120)) * direction_vector[1],
                sin(radians(120)) * direction_vector[0] + cos(radians(120)) * direction_vector[1],
                0
            ])
            point_on_side_2 = point_on_side_1 + rotated_vector

            line_to_side_1 = Line(inner_vertices[i], point_on_side_1, color=YELLOW)
            line_to_side_2 = Line(inner_vertices[i], point_on_side_2, color=YELLOW)
            lines_to_sides.add(line_to_side_1, line_to_side_2)

        self.play(Create(lines_to_sides), run_time=2)
        self.wait(6)  # Keep everything displayed, including the inner points
