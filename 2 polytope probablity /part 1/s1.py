from manim import *

class CircleVisualization(Scene):
    def construct(self):
        # Step 0: Add text above the circle
        sample_space_text = Text(
            "Infinite points = Infinite Sample Space",
            font_size=28,
            color=BLUE
        ).move_to(UP * 3)  # Positioned above the circle

        # Display text after 2 seconds
        self.wait(2)
        self.play(FadeIn(sample_space_text))

        # SCENE 1: Circle with roaming point and sprinkle (12 seconds)

        # Step 1: Draw a circle with a red center point (no blue fill)
        large_circle = Circle(radius=2, color=BLUE, stroke_width=4)
        center_point = Dot(ORIGIN, color=RED, radius=0.1)
        self.play(Create(large_circle), FadeIn(center_point), run_time=1)

        # Step 2: Roaming point inside the circle
        roaming_point = Dot(color=WHITE, radius=0.1)
        roaming_path = VMobject()
        roaming_path.set_points_as_corners([
            np.array([x, y, 0]) for x, y in [
                (-1, -1), (1, 0.5), (-0.5, 1.5), (-1.5, -1), (1.5, 1), (0, 1)
            ]
        ])
        self.play(MoveAlongPath(roaming_point, roaming_path), run_time=4)

        # Step 3: Sprinkle 200–300 points inside the circle
        sprinkled_points = VGroup(*[
            Dot(
                np.array([x, y, 0]),
                color=WHITE,
                radius=0.05
            )
            for x, y in [
                (np.random.uniform(-2, 2), np.random.uniform(-2, 2))
                for _ in range(300)  # Increased number of points
            ]
            if np.sqrt(x**2 + y**2) <= 2  # Ensure points are within the circle
        ])
        self.play(FadeOut(roaming_point), FadeIn(sprinkled_points), run_time=2)
        self.wait(2)

        # Step 4: Clear the points
        self.play(FadeOut(sprinkled_points), run_time=1)

        # SCENE 2: Radius cut in half, small circle colored blue (15 seconds)

        # Step 1: Draw radius and cut it in half
        radius_full = Line(start=ORIGIN, end=UP * 2, color=WHITE, stroke_width=4)
        radius_half = Line(start=ORIGIN, end=UP * 1, color=WHITE, stroke_width=4)
        self.play(Create(radius_full), run_time=2)
        self.play(Transform(radius_full, radius_half), run_time=2)

        # Step 2: Draw small circle and color it a deeper blue
        small_circle = Circle(radius=1, color=BLUE, stroke_width=4)
        self.play(Create(small_circle), run_time=2)
        self.play(small_circle.animate.set_fill(color=BLUE_E, opacity=0.7), run_time=4)  # Increased opacity and deeper blue

        # Step 3: Erase the radius line
        self.play(FadeOut(radius_half), run_time=1)

        # Extra 3 seconds of wait time at the end
        self.wait(3)
