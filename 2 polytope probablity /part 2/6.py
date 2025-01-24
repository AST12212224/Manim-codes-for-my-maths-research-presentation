from manim import *
from math import cos, sin, radians, pi

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

        # Inner triangle setup with corrected size
        inner_vertices = inner_polygon_vertices(outer_radius, n, outer_side_length)
        inner_points = VGroup(*[Dot(point, color=WHITE, radius=0.06) for point in inner_vertices])  # Smaller points
        inner_triangle = Polygon(*inner_vertices, color=WHITE, stroke_width=2)

        # Add and animate the outer triangle, inner points, and inner triangle
        self.play(
            Create(outer_triangle),
            FadeIn(inner_points),
            Create(inner_triangle),
            run_time=1
        )
        self.wait(4)  # Display all elements for 4 seconds
