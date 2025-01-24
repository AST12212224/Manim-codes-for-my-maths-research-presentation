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

        # Function to calculate the Reuleaux arc radius
        def reuleaux_radius(s, n):
            return (
                s * (1 / tan(radians(180 / n))) * (4 + tan(radians(90 / n))**2) / 8
            )

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
        reuleaux_r = reuleaux_radius(initial_outer_side_length, n)
        outer_vertices = polygon_vertices(outer_radius, n)  # Outer polygon vertices
        inner_vertices = polygon_vertices(inner_radius, n)  # Inner polygon vertices

        # Create the outer polygon using calculated vertices
        outer_polygon = Polygon(*outer_vertices, color=BLUE, stroke_width=4)

        # Create the inner polygon using calculated vertices
        inner_polygon = Polygon(*inner_vertices, color=BLUE, stroke_width=4)

        # Create the inner circle
        inner_circle = Circle(radius=inner_circle_r, color=WHITE, stroke_width=4)

        # Play all animations together
        self.play(
            Create(outer_polygon),
            Create(inner_circle),
            Create(inner_polygon),
            run_time=2
        )

        # Add points
        # Point 1: On one corner of the inner triangle
        point_1 = Dot(inner_vertices[0], color=GREEN, radius=0.05)
        self.play(FadeIn(point_1))
        self.wait(2)

        # Point 2: On the inner circle, positioned between corner 1 and corner 2
        mid_angle = (np.arctan2(inner_vertices[1][1], inner_vertices[1][0]) +
                     np.arctan2(inner_vertices[0][1], inner_vertices[0][0])) / 2
        point_on_circle = inner_circle.point_at_angle(mid_angle)
        point_2 = Dot(point_on_circle, color=ORANGE, radius=0.05)
        self.play(FadeIn(point_2))
        self.wait(2)

        # Point 3: On another corner of the inner triangle
        point_3 = Dot(inner_vertices[1], color=GREEN, radius=0.05)
        self.play(FadeIn(point_3))
        self.wait(2)

        # Create Reuleaux-like arcs after points are made
        arcs = VGroup()
        for i in range(n):
            start_point = inner_vertices[i]
            end_point = inner_vertices[(i + 1) % n]  # Next vertex
            arc = ArcBetweenPoints(
                start=start_point,
                end=end_point,
                radius=reuleaux_r,
                color=ORANGE,
                stroke_width=4
            )
            arcs.add(arc)

        # Create the filled Reuleaux area
        reuleaux_fill = VGroup()
        for i in range(n):
            start_point = inner_vertices[i]
            end_point = inner_vertices[(i + 1) % n]
            arc = ArcBetweenPoints(
                start=start_point,
                end=end_point,
                radius=reuleaux_r,
                color=ORANGE,
                fill_opacity=0.3,  # Light orange fill
                stroke_opacity=0
            )
            reuleaux_fill.add(arc)

        # Show the arcs and the Reuleaux fill
        self.play(Create(arcs))
        self.play(FadeIn(reuleaux_fill), run_time=2)

        # Keep everything displayed for an additional 4 seconds
        self.wait(4)
