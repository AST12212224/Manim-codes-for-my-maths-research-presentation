# scene_dsrs_title_and_links.py
# Manim v0.18+/v0.19+ — 13s outro:
#  - 0..7s : 3-line title centered (drawn then held)
#  - 7..13s: links block + arrow centered (title removed before links appear)

from manim import *


class Scene_DSRSOutro(Scene):
    def construct(self):
        # Timing
        TITLE_DRAW = 2.0  # seconds to draw the title
        TITLE_HOLD = 5.0  # additional seconds the title stays (total title time = 7s)
        LINKS_APPEAR = 0.5  # links fade in time
        LINKS_HOLD = 6.0  # time to hold the links (total links time = 6s)

        # --- Title: 3 lines (smaller font so it fits) ---
        title_lines = VGroup(
            Tex(r"\textbf{Discrete Square Residual Structures (DSRS)}", font_size=44),
            Tex(r"A framework where each integer reveals", font_size=38),
            Tex(r"its own discrete connection to $\pi$", font_size=38),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)
        # Keep title centered but use a slightly higher position so links later sit in center
        title_group = VGroup(*title_lines).move_to(UP * 0.2)

        # --- Links block (centered) ---
        links = VGroup(
            Tex(r"\textit{Preprint link}", font_size=30),
            Tex(r"\textit{Code repository / Resources}", font_size=30),
            Tex(r"\textit{Other videos}", font_size=30),
        ).arrange(DOWN, aligned_edge=LEFT, buff=0.25)

        # Arrow pointing down below the links
        arrow = Arrow(
            start=UP * 0.4,
            end=DOWN * 0.4,
            stroke_width=5,
            tip_length=0.25,
            color=YELLOW,
        )

        arrow_label = Tex(
            r"\textit{Links in the description}", font_size=26, color=YELLOW
        )

        # Group links + arrow and center them vertically for the links phase
        links_group = VGroup(
            links, VGroup(arrow, arrow_label).arrange(DOWN, buff=0.12)
        ).arrange(DOWN, buff=0.6)
        links_group.move_to(ORIGIN)  # center of screen for the links phase

        # --- SCENE: Title phase (0..7s) ---
        self.play(Write(title_group), run_time=TITLE_DRAW)  # draw title
        self.wait(TITLE_HOLD)  # hold until t = 7s

        # --- Transition: remove title and show links (7s) ---
        # Fade out title quickly, then fade in links in center
        self.play(FadeOut(title_group), run_time=0.4)
        # Show links centered
        # Draw the links text, then create the arrow and label
        self.play(FadeIn(links, shift=UP * 0.15), run_time=LINKS_APPEAR)
        self.play(
            Create(arrow), FadeIn(arrow_label, shift=UP * 0.08), run_time=LINKS_APPEAR
        )

        # Hold links for the remaining ~6s
        self.wait(LINKS_HOLD)

        # Fade everything out at the end
        self.play(FadeOut(VGroup(links_group)), run_time=0.6)
