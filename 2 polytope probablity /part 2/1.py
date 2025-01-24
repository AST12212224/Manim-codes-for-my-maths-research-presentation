from manim import *

class ShowEqualities(Scene):
    def construct(self):
        # First expression
        expression1 = MathTex(r"s_i = s \quad \text{for all } i \in \{1, 2, 3, \dots, n\}")
        expression1.move_to(DOWN)  # Move this expression slightly downward

        # Second expression
        expression2 = MathTex(r"s_1 = s_2 = s_3 = \cdots = s_n")
        expression2.move_to(UP)  # Move this expression slightly upward

        # Animate both expressions quickly
        self.play(Write(expression2), run_time=1.5)  # Display the second expression in 1 second
        self.play(Write(expression1), run_time=1.4)  # Display the first expression in 1 second
