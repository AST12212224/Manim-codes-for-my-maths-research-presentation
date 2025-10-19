# scene_law_mu_dense.py
# Dense μ visualization: many values at once, sampled from mu_pi.csv
# - Displays up to 120 values in a compact grid
# - Batches every 0.5s, overlapping so screen remains dense and lively
# - Subtle floating motion applied to all number blocks
#
# Usage:
#   manim -pql scene_law_mu_dense.py Scene_LawMuDense
# or use the high-quality/resolution commands shown below.

from manim import *
import csv
import random
import math
import numpy as np


class Scene_LawMuDense(Scene):
    def construct(self):
        total_duration = 4.0
        batch_time = 0.5
        num_batches = int(total_duration / batch_time)
        batch_size = 30  # how many new items to introduce per batch
        max_total = 120  # cap total unique samples shown

        # --- Load μ values from CSV in same directory ---
        mu_values = []
        try:
            with open("mu_pi.csv", newline="") as csvfile:
                reader = csv.reader(csvfile)
                for i, row in enumerate(reader):
                    if i == 0:
                        # naive header skip if the first row contains "mu" or non-int
                        try:
                            int(row[0])
                        except:
                            continue
                    try:
                        mu = int(row[0])
                        if 2 <= mu <= 199:
                            mu_values.append(mu)
                    except:
                        pass
        except FileNotFoundError:
            # Friendly fallback: if file missing, generate some sample μ values
            mu_values = list(range(2, 200))

        if not mu_values:
            mu_values = list(range(2, 200))

        # sample up to max_total unique μ values
        sample_size = min(len(mu_values), max_total)
        mu_sample = random.sample(mu_values, sample_size)

        # create grid layout parameters
        n_total = len(mu_sample)
        cols = int(math.ceil(math.sqrt(n_total * 16 / 9)))  # bias towards wide aspect
        rows = int(math.ceil(n_total / cols))
        # ensure at least 6 columns for density
        cols = max(cols, 6)
        rows = int(math.ceil(n_total / cols))

        # compute spacing to pack them tightly but legibly
        x_span = config.frame_width * 0.9
        y_span = (config.frame_height - 1.2) * 0.9
        spacing_x = x_span / max(1, cols)
        spacing_y = y_span / max(1, rows)

        # build mobjects for each μ value
        blocks = []
        for i, m in enumerate(mu_sample):
            r = i // cols
            c = i % cols
            x = (c - (cols - 1) / 2) * spacing_x
            y = ((rows - 1) / 2 - r) * spacing_y
            color = GREEN if (m % 4 != 0) else RED
            # compact block: μ on left, small approx placeholder on right (you may change)
            mu_text = Text(f"μ={m}", font="Monospace", font_size=20, color=color)
            # optional: show a short approx (if available in CSV you can replace)
            approx_text = Text("", font="Monospace", font_size=16, color=GREY_B)
            block = (
                VGroup(mu_text, approx_text)
                .arrange(RIGHT, buff=0.24)
                .move_to([x, y, 0])
            )
            blocks.append(block)

        blocks_group = VGroup(*blocks)

        # Title
        title = Text(
            "From all those computations, I realized a clear law.", font_size=32
        ).to_edge(UP, buff=0.5)
        self.play(Write(title), run_time=0.5)

        # Reveal style:
        # We'll reveal blocks in overlapping batches: each batch fades in a slice,
        # but we never fully clear the screen until the end (so it stays dense).
        idx = 0
        for b in range(num_batches):
            # pick next slice of items; wrap-around if necessary
            slice_start = (b * batch_size) % n_total
            slice_end = slice_start + batch_size
            slice_items = []
            for j in range(slice_start, slice_end):
                slice_items.append(blocks[j % n_total])
            # stagger-in appearance for the slice
            self.play(
                LaggedStart(
                    *[FadeIn(m, shift=DOWN * 0.12) for m in slice_items], lag_ratio=0.02
                ),
                run_time=0.28,
            )
            # small overlap: let them breathe then slightly jitter (floating motion)
            # floating animation applied continuously to currently-visible items
            float_anims = []
            for m in slice_items:
                dx = random.uniform(-0.05, 0.05)
                dy = random.uniform(-0.03, 0.03)
                float_anims.append(
                    m.animate.shift(UP * dy + RIGHT * dx).scale(
                        1.0 + random.uniform(-0.01, 0.01)
                    )
                )
            # run a brief floating tweak
            self.play(*float_anims, run_time=0.12)
            self.wait(max(0, batch_time - 0.4))

        # final subtle pulse and hold
        self.play(title.animate.scale(1.03), run_time=0.25)
        self.wait(0.35)

        # fade out all
        self.play(FadeOut(VGroup(title, blocks_group)), run_time=0.5)


# scene_mod4_law_fixed_v2.py
# Manim (v0.18+ / v0.19+) — 7s scene combining animated number-line (1..20)
# and the formal DSRS law (π vs 1) and a 75% probability statement.
# v2: number line is removed when formula appears; ellipsis (...) after 20 added.


class Scene_Mod4Law_Fixed_v2(Scene):
    def construct(self):
        # Colors
        PI_COLOR = GREEN
        ONE_COLOR = RED
        LABEL_COLOR = WHITE

        # TIMINGS
        t_total = 7.0
        t_line = 2.5  # number line phase
        t_formula = 2.5  # formula reveal phase
        t_prob = 2.0  # probability phase

        # ---------- NUMBER LINE (0..2.5s) ----------
        line = Line(LEFT * 6, RIGHT * 6, stroke_width=3, color=GREY_A).shift(DOWN * 0.6)
        tick_height = 0.25

        # Create ticks and number labels for 1..20
        n_min, n_max = 1, 20
        n_count = n_max - n_min + 1
        ticks = VGroup()
        labels = VGroup()
        for i, n in enumerate(range(n_min, n_max + 1)):
            alpha = i / (n_count - 1)
            x = line.point_from_proportion(alpha)
            tick = Line(
                x + UP * tick_height / 2,
                x + DOWN * tick_height / 2,
                stroke_width=2,
                color=GREY_A,
            )
            ticks.add(tick)
            color = PI_COLOR if (n % 4 != 0) else ONE_COLOR
            lbl = MathTex(str(n), font_size=28, color=color).next_to(x, DOWN, buff=0.2)
            labels.add(lbl)

        # Add ellipsis after 20 to indicate continuation
        last_tick_x = line.point_from_proportion(1.0)
        ellipsis = MathTex(r"\ldots", font_size=36, color=GREY_A).next_to(
            last_tick_x, RIGHT, buff=0.6
        )
        # group the numberline elements
        numberline_group = VGroup(line, ticks, labels, ellipsis).move_to(ORIGIN)

        # Caption showing modular condition
        caption = (
            MathTex(r"\mu \not\equiv 0 \pmod{4}", font_size=32)
            .to_corner(UR)
            .set_color(PI_COLOR)
        )
        caption.set_opacity(0.0)

        # Appear number line and labels
        self.play(Create(line), run_time=0.35)
        self.play(
            LaggedStart(*[Create(t) for t in ticks], lag_ratio=0.02), run_time=0.35
        )
        half = len(labels) // 2
        self.play(
            LaggedStart(
                *[FadeIn(labels[i], shift=DOWN * 0.12) for i in range(half)],
                lag_ratio=0.03,
            ),
            run_time=0.5,
        )
        self.play(
            LaggedStart(
                *[
                    FadeIn(labels[i], shift=DOWN * 0.12)
                    for i in range(half, len(labels))
                ],
                lag_ratio=0.03,
            ),
            run_time=0.5,
        )
        self.play(FadeIn(ellipsis, shift=RIGHT * 0.05), run_time=0.25)

        # Pulse multiples of 4 vs others
        mult4 = VGroup(*[lbl for lbl in labels if int(lbl.tex_string) % 4 == 0])
        not4 = VGroup(*[lbl for lbl in labels if int(lbl.tex_string) % 4 != 0])

        # show caption
        self.play(FadeIn(caption, shift=UP * 0.08), run_time=0.25)
        # two quick pulses
        self.play(
            AnimationGroup(
                *[lbl.animate.scale(1.07) for lbl in not4],
                *[lbl.animate.scale(1.12) for lbl in mult4],
                lag_ratio=0.0,
            ),
            run_time=0.25,
        )
        self.play(
            AnimationGroup(
                *[lbl.animate.scale(1 / 1.07) for lbl in not4],
                *[lbl.animate.scale(1 / 1.12) for lbl in mult4],
                lag_ratio=0.0,
            ),
            run_time=0.25,
        )

        # ensure we wait the remainder of t_line
        elapsed_line = 0.35 + 0.35 + 0.5 + 0.5 + 0.25 + 0.25 + 0.25
        self.wait(max(0, t_line - elapsed_line))

        # ---------- FORMAL CONVERGENCE DISPLAY (2.5s) ----------
        # Fade OUT number line cleanly so it is removed from screen for the formula phase
        self.play(
            FadeOut(numberline_group, shift=DOWN * 0.2),
            caption.animate.set_opacity(0.0),
            run_time=0.35,
        )

        # Build the formal expression robustly:
        left = MathTex(r"P(\mu)\to", font_size=44)
        top_line = MathTex(
            r"\pi, \quad \mu \not\equiv 0 \pmod{4}", font_size=40
        ).set_color_by_tex(r"\pi", PI_COLOR)
        bot_line = MathTex(
            r"1, \quad \mu \equiv 0 \pmod{4}", font_size=40
        ).set_color_by_tex("1", ONE_COLOR)
        cases_group = VGroup(top_line, bot_line).arrange(
            DOWN, aligned_edge=LEFT, buff=0.35
        )
        formal = VGroup(left, cases_group).arrange(RIGHT, buff=0.6).move_to(UP * 0.3)

        # Animate in
        self.play(FadeIn(left, shift=LEFT * 0.3), run_time=0.38)
        self.play(
            LaggedStart(Write(top_line), Write(bot_line), lag_ratio=0.18), run_time=0.9
        )

        # subtle colored glows behind each line then fade them
        top_glow = SurroundingRectangle(
            top_line, color=PI_COLOR, stroke_width=2, buff=0.18
        ).set_opacity(0.0)
        bot_glow = SurroundingRectangle(
            bot_line, color=ONE_COLOR, stroke_width=2, buff=0.18
        ).set_opacity(0.0)
        self.add(top_glow, bot_glow)
        self.play(
            top_glow.animate.set_opacity(0.12),
            bot_glow.animate.set_opacity(0.10),
            run_time=0.38,
        )
        self.play(
            top_glow.animate.set_opacity(0.0),
            bot_glow.animate.set_opacity(0.0),
            run_time=0.22,
        )

        self.wait(max(0, t_formula - (0.38 + 0.9 + 0.38 + 0.22)))

        # ---------- PROBABILITY SUMMARY (2s) ----------
        prob = MathTex(
            r"\Pr\bigl(P(\mu)\to\pi\bigr) \;=\; \frac{3}{4} \;=\; 75\%", font_size=46
        ).move_to(DOWN * 0.8)

        try:
            prob.set_color_by_tex_to_color_map({r"\pi": PI_COLOR})
        except Exception:
            pass

        self.play(Write(prob), run_time=0.75)

        # pulse the pi subobject if present
        try:
            pi_sub = prob.get_parts_by_tex(r"\pi")[0]
            self.play(pi_sub.animate.scale(1.14), run_time=0.15)
            self.play(pi_sub.animate.scale(1 / 1.14), run_time=0.12)
        except Exception:
            self.play(prob.animate.scale(1.03), run_time=0.15)
            self.play(prob.animate.scale(1 / 1.03), run_time=0.12)

        self.wait(max(0, t_prob - (0.75 + 0.15 + 0.12)))
        # clean fade out
        self.play(FadeOut(VGroup(left, top_line, bot_line, prob)), run_time=0.5)


# scene_mod4_law_part2_mathonly.py
# Manim (v0.18+ / v0.19+) — 4s scene, math-only:
# "P(mu) -> 1 for mu ≡ 0 (mod 4)" and "Pr(...)=1/4=25%"


class Scene_Mod4Law_Part2_MathOnly(Scene):
    def construct(self):
        ONE_COLOR = RED
        TEXT_COLOR = WHITE

        # Timings
        total_time = 4.0
        t_formal = 2.0
        t_prob = total_time - t_formal

        # Formal convergence line (centered, upper part of screen)
        left = MathTex(r"P(\mu)\to", font_size=72)
        right = MathTex(r"1,\quad \mu \equiv 0 \pmod{4}", font_size=54)
        # color the "1" red
        right.set_color_by_tex_to_color_map({r"1": ONE_COLOR})
        formal = VGroup(left, right).arrange(RIGHT, buff=0.6).to_edge(UP, buff=1.0)

        # Probability line (bottom)
        prob = MathTex(
            r"\Pr\bigl(P(\mu)\to 1\bigr) \;=\; \dfrac{1}{4} \;=\; 25\%", font_size=56
        )
        # color the '1' (and numerator if desired) red
        prob.set_color_by_tex_to_color_map({r"1": ONE_COLOR})

        # Animate: show formal -> pulse the 1 -> show probability -> hold -> fade
        self.play(FadeIn(formal, shift=UP * 0.2), run_time=1.5)

        # wait until formal phase done
        self.wait(max(0, t_formal - (0.5 + 0.6 + 0.24)))

        # show probability line
        self.play(Write(prob), run_time=0.6)
        # hold remaining time
        self.wait(max(0, t_prob - (0.6 + 0.24)))

        # clean fade out
        self.play(FadeOut(VGroup(formal, prob)), run_time=0.4)
