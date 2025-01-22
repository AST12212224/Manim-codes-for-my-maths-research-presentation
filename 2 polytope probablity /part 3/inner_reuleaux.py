from manim import *
from math import cos, sin, tan, radians, pi
import numpy as np

class ReuleauxPolygonAlignedFix(Scene):
    def construct(self):
        # Parameters
        initial_outer_side_length = 3  # Side length for the outer polygon
        max_sides = 50  # From triangle (3) to decagon (10)

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

        # Create Reuleaux-like arcs
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

        # Add the initial shapes and arcs to the scene
        self.play(Create(outer_polygon))
        self.play(Create(inner_circle))
        self.play(Create(inner_polygon))

        # Show the arcs of the Reuleaux and the light orange area
        self.play(Create(arcs))
        self.play(FadeIn(reuleaux_fill), run_time=2)

        # Animation loop: Increase the sides gradually
        for sides in range(4, max_sides + 1):
            # Recalculate dimensions
            outer_side = 2 * outer_radius * sin(pi / sides)
            inner_side = inner_side_length(outer_side, sides)
            inner_radius = polygon_radius_from_side(inner_side, sides)
            inner_circle_r = inner_circle_radius(outer_side, sides)
            reuleaux_r = reuleaux_radius(outer_side, sides)
            outer_vertices = polygon_vertices(outer_radius, sides)
            inner_vertices = polygon_vertices(inner_radius, sides)

            # Create new shapes
            new_outer_polygon = Polygon(*outer_vertices, color=BLUE, stroke_width=4)
            new_inner_polygon = Polygon(*inner_vertices, color=BLUE, stroke_width=4)
            new_inner_circle = Circle(radius=inner_circle_r, color=WHITE, stroke_width=4)

            # Create new arcs
            new_arcs = VGroup()
            new_reuleaux_fill = VGroup()
            for i in range(sides):
                start_point = inner_vertices[i]
                end_point = inner_vertices[(i + 1) % sides]
                arc = ArcBetweenPoints(
                    start=start_point,
                    end=end_point,
                    radius=reuleaux_r,
                    color=ORANGE,
                    stroke_width=4
                )
                new_arcs.add(arc)

                # Filled arc for the Reuleaux shape
                filled_arc = ArcBetweenPoints(
                    start=start_point,
                    end=end_point,
                    radius=reuleaux_r,
                    color=ORANGE,
                    fill_opacity=0.3,  # Light orange fill
                    stroke_opacity=0
                )
                new_reuleaux_fill.add(filled_arc)

            # Animate the transitions
            self.play(
                Transform(outer_polygon, new_outer_polygon),
                Transform(inner_polygon, new_inner_polygon),
                Transform(inner_circle, new_inner_circle),
                Transform(arcs, new_arcs),
                Transform(reuleaux_fill, new_reuleaux_fill),
                run_time=2
            )

        # Final transformation to circles
        final_outer_circle = Circle(radius=outer_radius, color=BLUE, stroke_width=4)
        final_inner_circle = Circle(radius=outer_radius / 2, color=WHITE, stroke_width=4)

        # Animate the transformation into circles
        self.play(
            Transform(outer_polygon, final_outer_circle),
            Transform(inner_polygon, final_inner_circle),
            Transform(inner_circle, final_inner_circle),
            FadeOut(arcs),
            FadeOut(reuleaux_fill),
            run_time=2
        )

        # Hold the final scene
        self.wait(2)
