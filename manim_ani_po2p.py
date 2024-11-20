from manim import *

class GrowingPolygon(Scene):
    def construct(self):
        # Parameters
        radius = 2  # Radius of the circle and polygons
        max_sides = 100  # Maximum number of sides before showing circle
        text_position = UP * 3  # Position of the side-count text

        # Create initial polygon (triangle with 3 sides)
        polygon = RegularPolygon(n=3, radius=radius)
        polygon.set_stroke(width=4)
        self.play(Create(polygon))  # Draw the initial triangle

        # Initial text
        side_count_text = Text("S = 3", font_size=36).move_to(text_position)
        self.play(Write(side_count_text))

        # Animation loop: Increase the sides gradually
        for sides in range(4, max_sides + 1):
            # Update the polygon to have one more side
            new_polygon = RegularPolygon(n=sides, radius=radius)
            new_polygon.set_stroke(width=4)
            
            # Smoothly morph the existing polygon into the new one
            self.play(Transform(polygon, new_polygon), run_time=0.05)

            # Update the text to reflect the current number of sides
            new_text = Text(f"S = {sides}", font_size=36).move_to(text_position)
            self.play(Transform(side_count_text, new_text), run_time=0.05)

        # Transition to a circle and show S = ∞
        circle = Circle(radius=radius)
        circle.set_stroke(width=4)
        self.play(Transform(polygon, circle), run_time=2)

        # Update text to S = ∞
        infinity_text = Text("S = ∞", font_size=36).move_to(text_position)
        self.play(Transform(side_count_text, infinity_text), run_time=2)

        # Hold the final scene
        self.wait(2)
