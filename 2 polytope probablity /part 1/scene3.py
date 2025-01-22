from manim import *

class OtherPolygons(Scene):
    def construct(self):
        # SCENE 1: Other polygons popping up (10 seconds)

        # Step 1: Show polygons popping up
        polygons = VGroup(
            RegularPolygon(n=3, color=BLUE, stroke_width=2).scale(0.5).shift(LEFT * 3 + UP * 2),
            RegularPolygon(n=4, color=GREEN, stroke_width=2).scale(0.5).shift(RIGHT * 3 + UP * 2),
            RegularPolygon(n=5, color=RED, stroke_width=2).scale(0.5).shift(LEFT * 2 + DOWN * 2),
            RegularPolygon(n=6, color=YELLOW, stroke_width=2).scale(0.5).shift(RIGHT * 2 + DOWN * 2),
            RegularPolygon(n=8, color=ORANGE, stroke_width=2).scale(0.5).shift(UP * 2 + LEFT * 1),
            RegularPolygon(n=10, color=PINK, stroke_width=2).scale(0.5).shift(UP * 2 + RIGHT * 1),
            RegularPolygon(n=12, color=PURPLE, stroke_width=2).scale(0.5).shift(DOWN * 1 + LEFT * 3),
            RegularPolygon(n=15, color=TEAL, stroke_width=2).scale(0.5).shift(DOWN * 1 + RIGHT * 3)
        )

        for poly in polygons:
            self.play(Create(poly), run_time=0.5)
        self.wait(1)

        # Step 2: Show the question mark and move polygons into it
        question_mark = Text("?", font_size=144, color=WHITE).move_to(ORIGIN)
        self.play(FadeIn(question_mark))
        self.wait(1)

        # Move polygons into the question mark and fade them out
        self.play(polygons.animate.arrange_in_grid(buff=0.5).move_to(ORIGIN).scale(0.2), run_time=2)
        self.play(FadeOut(polygons), FadeOut(question_mark))
        self.wait(1)

        # SCENE 2: Final pop-up text (3 seconds)
        popup_text = Text(
            "Check out the next video for other polygons!",
            font_size=36,
            color=WHITE
        ).move_to(UP * 2)
        arrow = Arrow(start=UP * 1, end=DOWN * 1, color=WHITE, buff=0.3)
        link_text = Text(
            "Link in the description!",
            font_size=28,
            color=BLUE
        ).next_to(arrow, DOWN, buff=0.5)

        # Play animations for popup text, arrow, and link text
        self.play(FadeIn(popup_text), Create(arrow), FadeIn(link_text), run_time=2)
        self.wait(2)
