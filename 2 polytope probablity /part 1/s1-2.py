from manim import *

class CalculationText(Scene):
    def construct(self):
        # SCENE 3: Calculations on a plain screen (36 seconds)

        # Step 1: Show A_large and A_small calculations (8 seconds)
        a_large = MathTex(r"A_{\text{large}} = \pi x^2", font_size=40).move_to(UP * 1.5)
        a_small = MathTex(r"A_{\text{small}} = \frac{\pi x^2}{4}", font_size=40).next_to(a_large, DOWN, buff=0.5)

        self.play(Write(a_large), run_time=3)
        self.play(Write(a_small), run_time=3)

        # Step 2: Add detailed calculation for A_small below the equation
        a_small_details = MathTex(
            r"A_{\text{small}} = \pi \left(\frac{x}{2}\right)^2 = \frac{\pi x^2}{4}",
            font_size=36,
            color=BLUE
        ).next_to(a_small, DOWN, buff=0.5)
        self.play(Write(a_small_details), run_time=3.5)
        self.wait(2)

        # Step 3: Erase A_large and A_small, and show P_centre formula
        self.play(FadeOut(a_large, a_small, a_small_details))
        p_centre_formula = MathTex(
            r"\mathbb{P}(center) = \frac{A_{\text{small}}}{A_{\text{large}}} = \frac{\frac{\pi x^2}{4}}{\pi x^2} = \frac{1}{4}",
            font_size=36,
            color=BLUE  # Highlight the P_center formula in blue
        ).move_to(ORIGIN)
        self.play(Write(p_centre_formula), run_time=8)
        self.wait(7)  # Freeze the frame for 8 seconds

        # Step 4: Erase P_centre formula and show final answers
        self.play(FadeOut(p_centre_formula))
        p_centre_answer = MathTex(
            r"\mathbb{P}(center) = \frac{1}{4}",
            font_size=40,
            color=BLUE  # Highlight center probability in blue
        ).move_to(UP * 1)
        p_circumference_answer = MathTex(
            r"\mathbb{P}(circumference) = \frac{3}{4}",
            font_size=40,
            color=YELLOW  # Highlight circumference probability in yellow
        ).next_to(p_centre_answer, DOWN, buff=1)

        self.play(Write(p_centre_answer))
        self.play(Write(p_circumference_answer))
        self.wait(4.6)

        # End Part 2
        self.play(FadeOut(p_centre_answer, p_circumference_answer))
