from manim import *
from math import cos, sin, tan, radians, pi, sqrt
import numpy as np

class ReuleauxPolygonAlignedFix(Scene):
    def construct(self):
        # Parameters
        initial_outer_side_length = 3  # Side length for the outer polygon
        max_sides = 10  # From triangle (3) to decagon (10)

        # Function to calculate the radius of a polygon from its side length
        def polygon_radius_from_side(side_length, n):
            return side_length / (2 * sin(pi / n))

        # Function to calculate the inner side length based on the formula
        def inner_side_length(outer_side, n):
            return (outer_side * cos(radians(180 / n))) / (2 * (cos(radians(90 / n))**2))

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
        reuleaux_r = reuleaux_radius(initial_outer_side_length, n)
        inner_vertices = polygon_vertices(inner_radius, n)  # Inner polygon vertices

        # Create the inner polygon
        inner_polygon = RegularPolygon(n=n, radius=inner_radius)
        inner_polygon.set_stroke(width=4, color=WHITE)

        # Create Reuleaux-like arcs
        arcs = VGroup()
        for i in range(n):
            start_point = inner_vertices[i]
            end_point = inner_vertices[(i + 1) % n]  # Next vertex
            arc = ArcBetweenPoints(
                start=start_point,
                end=end_point,
                radius=reuleaux_r,
                color=RED,
                stroke_width=4
            )
            arcs.add(arc)

        # Add the initial shapes and arcs to the scene
        self.play(Create(inner_polygon))
        self.play(Create(arcs))

        # Animation loop: Increase the sides gradually
        for sides in range(4, max_sides + 1):
            # Recalculate dimensions
            outer_side = 2 * outer_radius * sin(pi / sides)
            inner_side = inner_side_length(outer_side, sides)
            inner_radius = polygon_radius_from_side(inner_side, sides)
            reuleaux_r = reuleaux_radius(outer_side, sides)
            inner_vertices = polygon_vertices(inner_radius, sides)

            # Create new shapes
            new_inner_polygon = RegularPolygon(n=sides, radius=inner_radius)
            new_inner_polygon.set_stroke(width=4, color=WHITE)

            # Create new arcs
            new_arcs = VGroup()
            for i in range(sides):
                start_point = inner_vertices[i]
                end_point = inner_vertices[(i + 1) % sides]
                arc = ArcBetweenPoints(
                    start=start_point,
                    end=end_point,
                    radius=reuleaux_r,  # Ensures arcs align perfectly with corners
                    color=RED,
                    stroke_width=4
                )
                new_arcs.add(arc)

            # Animate the transitions
            self.play(
                Transform(inner_polygon, new_inner_polygon),
                Transform(arcs, new_arcs),
                run_time=2
            )

        # Hold the final scene
        self.wait(2)
