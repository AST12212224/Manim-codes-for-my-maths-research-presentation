from manim import *

class ReuleauxTriangle(Scene):
    def construct(self):
        # Coordinates for the vertices of an equilateral triangle
        A = np.array([-1, np.sqrt(3), 0])
        B = np.array([1, np.sqrt(3), 0])
        C = np.array([0, 0, 0])

        # Calculate the radius for the circles using the side length of the triangle
        radius = np.linalg.norm(B - C)

        # Create three circles passing through each other's center
        circle_A = Circle(radius=radius, arc_center=B).set_color(WHITE)
        circle_B = Circle(radius=radius, arc_center=C).set_color(WHITE)
        circle_C = Circle(radius=radius, arc_center=A).set_color(WHITE)

        # Intersecting area of the circles
        reuleaux_triangle = Intersection(circle_A, circle_B, circle_C, fill_opacity=0.5, color=BLUE)

        # Animation: Draw each circle
        self.play(Create(circle_A), run_time=1/3)
        self.play(Create(circle_B), run_time=1/3)
        self.play(Create(circle_C), run_time=1/3)

        # Display the Reuleaux triangle
        self.play(FadeIn(reuleaux_triangle, run_time=2/3))

        # Make the circles invisible
        self.play(FadeOut(circle_A), FadeOut(circle_B), FadeOut(circle_C), run_time=1)

        # Hold the scene with only the Reuleaux triangle visible
        self.wait(5)
