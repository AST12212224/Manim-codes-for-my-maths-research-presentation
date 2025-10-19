# scene_LU_increase_fixed.py
# Clean version: no top caption, and separate U(n) and L(n) labels.

from manim import *
from manim import there_and_back_with_pause
import math
import numpy as np


class Scene_LU_Increase_Fixed(Scene):
    def construct(self):
        total_time = 5.0
        mu = 5
        n_min, n_max = 1, 15
        n_values = list(range(n_min, n_max + 1))

        # Compute L and U
        L_vals = [math.floor((n * n) / mu) for n in n_values]
        U_vals = [math.ceil((n * n) / mu) for n in n_values]

        # Colors
        L_color = GREEN
        U_color = RED
        axes_color = GREY_B

        # Axes
        max_y = max(U_vals) + 2
        ax = Axes(
            x_range=[n_min - 0.5, n_max + 0.5, 1],
            y_range=[0, max_y, max(1, max_y // 6)],
            x_length=11,
            y_length=4,
            axis_config={
                "include_numbers": True,
                "font_size": 20,
                "stroke_color": axes_color,
            },
        ).to_edge(DOWN, buff=0.7)

        x_label = MathTex("n", font_size=28).next_to(
            ax.x_axis.get_right(), LEFT, buff=0.6
        )
        y_label = MathTex("Value", font_size=28).next_to(
            ax.y_axis.get_top(), RIGHT, buff=0.3
        )

        # Step function builder
        def create_stair_path(values, color):
            segments = VGroup()
            for i in range(len(values)):
                x = n_values[i]
                y = values[i]
                x_start = x - 0.0
                x_end = x + 1.0 if i < len(values) - 1 else x + 0.4
                p1 = ax.coords_to_point(x_start, y)
                p2 = ax.coords_to_point(x_end, y)
                h_seg = Line(p1, p2, stroke_width=4, color=color)
                segments.add(h_seg)
                if i < len(values) - 1:
                    next_y = values[i + 1]
                    v_p1 = p2
                    v_p2 = ax.coords_to_point(x_end, next_y)
                    v_seg = Line(v_p1, v_p2, stroke_width=4, color=color)
                    segments.add(v_seg)
            return segments

        L_stairs = create_stair_path(L_vals, L_color)
        U_stairs = create_stair_path(U_vals, U_color)

        # Dots
        L_dots = VGroup(
            *[
                Dot(
                    point=ax.coords_to_point(n_values[i], L_vals[i]),
                    radius=0.06,
                    color=L_color,
                )
                for i in range(len(n_values))
            ]
        )
        U_dots = VGroup(
            *[
                Dot(
                    point=ax.coords_to_point(n_values[i], U_vals[i]),
                    radius=0.06,
                    color=U_color,
                )
                for i in range(len(n_values))
            ]
        )

        # Labels (with offset to avoid overlap)
        U_label = MathTex(r"U(n)", font_size=28).set_color(U_color)
        L_label = MathTex(r"L(n)", font_size=28).set_color(L_color)

        # Position U label a bit above U stairs, and L label a bit below L stairs
        U_label.next_to(U_stairs.get_top(), UP, buff=0.3)
        L_label.next_to(
            U_label, RIGHT, buff=1.0
        )  # Move L_label to the right of U_label

        # Animate
        self.play(Create(ax), Write(x_label), Write(y_label), run_time=0.5)
        self.play(Create(L_stairs), Create(L_dots), run_time=1.2)
        self.play(Create(U_stairs), Create(U_dots), run_time=1.0)
        self.play(FadeIn(U_label), FadeIn(L_label), run_time=0.25)

        elapsed = 0.5 + 1.2 + 1.0 + 0.25
        self.wait(max(0, total_time - elapsed))

        self.play(
            FadeOut(
                VGroup(
                    ax,
                    x_label,
                    y_label,
                    L_stairs,
                    U_stairs,
                    L_dots,
                    U_dots,
                    U_label,
                    L_label,
                )
            ),
            run_time=0.5,
        )


########################################################################
#
#


# scene_delta_entropy_13s.py
# ΔU(n) and ΔL(n) for many μ values in two phases:
# Phase 1: μ < 36 (clean structure)
# Phase 2: μ >= 36 (chaotic/entropy rise)
# Duration = 13 seconds total

from manim import *
import math


class Scene_DeltaEntropy(Scene):
    def construct(self):
        # --- μ sets and parameters ---
        MU_PHASE1 = [2, 5, 7, 10, 13, 19, 29, 31]
        MU_PHASE2 = [37, 47, 83, 89, 137]
        MU_VALUES = MU_PHASE1 + MU_PHASE2

        MULTIPLIERS = {
            2: 1.0,
            5: 2.0,
            7: 2.2,
            10: 2.5,
            13: 3.0,
            19: 3.2,
            29: 3.8,
            31: 4.0,
            37: 4.5,
            47: 5.0,
            83: 5.5,
            89: 5.8,
            137: 6.0,
        }

        BASE_N = 30
        TOTAL_DURATION = 13.0
        PHASE1_TIME = 8.0
        PHASE2_TIME = 5.0
        TIME_PER_PHASE1 = PHASE1_TIME / len(MU_PHASE1)
        TIME_PER_PHASE2 = PHASE2_TIME / len(MU_PHASE2)

        # --- Static labels ---
        du_label = (
            MathTex(r"\Delta_U(n)", font_size=30, color=RED)
            .to_corner(UR)
            .shift(LEFT * 0.2 + DOWN * 0.2)
        )
        dl_label = MathTex(r"\Delta_L(n)", font_size=30, color=GREEN).next_to(
            du_label, DOWN, aligned_edge=LEFT, buff=0.12
        )
        mu_label = MathTex(r"\mu = 2", font_size=32).to_corner(UL).set_color(WHITE)
        self.add(du_label, dl_label, mu_label)

        prev_axes = None
        prev_graph = None

        # --- Helper functions ---
        def compute_deltas(mu, N):
            n_values = list(range(1, N + 1))
            U = [math.ceil((n * n) / mu) for n in n_values]
            L = [math.floor((n * n) / mu) for n in n_values]
            delta_U = [U[i + 1] - U[i] for i in range(len(U) - 1)]
            delta_L = [L[i + 1] - L[i] for i in range(len(L) - 1)]
            x_vals = list(range(1, len(delta_U) + 1))
            return x_vals, delta_U, delta_L

        def make_axes(N, max_delta):
            x_max = max(5, N - 1)
            y_max = max(6, int(math.ceil(max_delta + 1)))
            axes = Axes(
                x_range=[0, x_max, max(1, x_max // 6)],
                y_range=[0, y_max, max(1, y_max // 6)],
                x_length=11,
                y_length=4,
                axis_config={
                    "include_numbers": True,
                    "font_size": 22,
                    "stroke_color": GREY_B,
                },
            ).to_edge(DOWN, buff=0.7)
            x_label = MathTex("n", font_size=26).next_to(
                axes.x_axis.get_right(), LEFT, buff=0.6
            )
            return axes, x_label

        def build_curve(ax, x_vals, delta_U, delta_L):
            U_lines, L_lines = VGroup(), VGroup()
            for i in range(len(x_vals) - 1):
                U_lines.add(
                    Line(
                        ax.coords_to_point(x_vals[i], delta_U[i]),
                        ax.coords_to_point(x_vals[i + 1], delta_U[i + 1]),
                        color=RED,
                        stroke_width=3,
                    )
                )
                L_lines.add(
                    Line(
                        ax.coords_to_point(x_vals[i], delta_L[i]),
                        ax.coords_to_point(x_vals[i + 1], delta_L[i + 1]),
                        color=GREEN,
                        stroke_width=3,
                    )
                )
            return VGroup(U_lines, L_lines)

        # --- Animate through all μ values ---
        for idx, mu in enumerate(MU_VALUES):
            N = int(BASE_N * MULTIPLIERS[mu])
            x_vals, dU, dL = compute_deltas(mu, N)
            max_delta = max(max(dU), max(dL))
            axes, xlabel = make_axes(N, max_delta)
            graph = build_curve(axes, x_vals, dU, dL)
            new_mu_label = (
                MathTex(rf"\mu = {mu}", font_size=32).to_corner(UL).set_color(WHITE)
            )

            # Determine runtime depending on which phase we’re in
            run_t = TIME_PER_PHASE1 if mu in MU_PHASE1 else TIME_PER_PHASE2

            # First μ — create from scratch
            if prev_axes is None:
                self.play(Create(axes), Write(xlabel), run_time=run_t * 0.45)
                self.play(
                    Create(graph),
                    Transform(mu_label, new_mu_label),
                    run_time=run_t * 0.55,
                )
            else:
                self.play(
                    ReplacementTransform(prev_axes, axes),
                    ReplacementTransform(prev_graph, graph),
                    Transform(mu_label, new_mu_label),
                    run_time=run_t,
                )

            prev_axes = axes
            prev_graph = graph

        # --- wrap up ---
        self.wait(0.4)
        self.play(
            FadeOut(VGroup(prev_axes, prev_graph, mu_label, du_label, dl_label)),
            run_time=0.5,
        )


############################################################################
#
#
# scene_three_phase_waves.py
# Manim v0.18+/v0.19+ — 6s scene implementing the 3 phases and exact formulas you provided.
#
# Phase1: sin(x) + k (k from 0 to 7.5 step 0.5, 16 waves) — STATIC
# Phase2: pairwise transforms — 8 functions, each assigned to a pair
# Phase3: 16 distinct complex functions (chaos) — MINGLED CHAOS

from manim import *
import numpy as np


class Scene_ThreePhaseWaves(Scene):
    def construct(self):
        # ---------- Configuration ----------
        PH1 = 2.0  # phase 1 duration (sin x + k)
        PH2 = 2.0  # phase 2 duration (transform to 8 pairs)
        PH3 = 2.0  # phase 3 duration (transform to 16 chaos)

        NUM_WAVES = 16
        POINTS = 350
        LEFT_RIGHT_MARGIN = 0.8

        # horizontal domain on screen
        x_min_screen = -config.frame_width / 2 + LEFT_RIGHT_MARGIN
        x_max_screen = config.frame_width / 2 - LEFT_RIGHT_MARGIN
        xs_screen = np.linspace(x_min_screen, x_max_screen, POINTS)

        # colors
        colors = color_gradient([BLUE, TEAL, GREEN, YELLOW, ORANGE, RED], NUM_WAVES)

        # trackers for blending phases
        pair_phase = ValueTracker(0.0)  # 0->1 during PH2
        full_phase = ValueTracker(0.0)  # 0->1 during PH3

        # vertical stacking offsets k from 0 to 7.5 step 0.5 (16 values)
        offsets_k = np.array(
            [
                0.0,
                0.5,
                1.0,
                1.5,
                2.0,
                2.5,
                3.0,
                3.5,
                4.0,
                4.5,
                5.0,
                5.5,
                6.0,
                6.5,
                7.0,
                7.5,
            ]
        )

        frame_h = config.frame_height
        # spacing now primarily for Phase 1 & 2 separation
        spacing = frame_h * 0.10
        k_centered = offsets_k - np.mean(offsets_k)
        y_centers = k_centered * spacing  # centers for each wave (used in P1, P2)

        # amplitude tuned for Phase 1 & 2 to avoid touching
        amp_base = spacing * 0.35
        # NEW: Larger amplitude for chaos phase to encourage mingling
        amp_chaos = frame_h * 0.45

        # Phase 1 & 2: Mathematical x domain (nice periodic waves)
        x_norm_periodic = np.linspace(-4 * np.pi, 4 * np.pi, POINTS)

        # Phase 3: Mathematical x domain for chaos functions (positive small domain)
        def xs_to_xpos(screen_xs):
            # map screen x_min/max to a math domain (e.g., 0.02 to 2*pi)
            t = (screen_xs - x_min_screen) / (x_max_screen - x_min_screen)
            # Use a slightly larger domain for chaotic functions
            return 0.02 + t * (4.0 * np.pi - 0.02)

        x_pos_base = xs_to_xpos(xs_screen)
        eps = 1e-6

        # Generate unique offsets for each chaotic wave to prevent exact overlaps
        rng = np.random.default_rng(20251019)
        chaos_x_offsets = rng.uniform(
            -0.5, 0.5, size=NUM_WAVES
        )  # Small horizontal shifts
        chaos_y_offsets = rng.uniform(
            -amp_chaos * 0.1, amp_chaos * 0.1, size=NUM_WAVES
        )  # Small vertical shifts

        # --- SAFE CHAOS HELPERS ---
        def safe_log_abs(x):
            xa = np.abs(x)
            xa = np.where(xa < 1e-6, 1e-6, xa)
            return np.log(xa)

        def tanh_clip(v, scale=1.0):
            return np.tanh(scale * v)

        def approx_sum_sin_factorial(x, M=6):
            s = np.zeros_like(x)
            fact = 1
            for n in range(1, M + 1):
                fact *= n
                s += np.sin(fact * x) / (n**2)
            return s

        # --- Mid-phase (pair) functions (8) ---
        def mid_f0(z):
            return np.sin(z - np.pi / 4)

        def mid_f1(z):
            return np.cos(z)

        def mid_f2(z):
            return 2.0 * np.sin(z)

        def mid_f3(z):
            return np.sin(2.0 * z)

        def mid_f4(z):
            return -np.sin(z)

        def mid_f5(z):
            return 3.0 * np.sin(z) + 1.0

        def mid_f6(z):
            return np.sin(0.5 * z)

        def mid_f7(z):
            return 2.0 * np.cos(3.0 * z)

        mid_funcs = [mid_f0, mid_f1, mid_f2, mid_f3, mid_f4, mid_f5, mid_f6, mid_f7]

        # --- Final-phase functions (16) ---
        def f1(x):
            return np.sin(1.0 / (x + eps))  # Added eps to denominator

        def f2(x):
            return (x + eps) * np.sin(1.0 / (x + eps))  # Added eps

        def f3(x):
            return np.sin(x**2)

        def f4(x):
            return np.floor(x) * np.sin(np.pi * x)

        def f5(x):
            return np.cos(safe_log_abs(x))

        def f6(x):
            return np.exp(np.sin(x * safe_log_abs(x)))

        def f7(x):
            return np.arctan(np.tan(1.0 / (x + eps)))  # Added eps

        def f8(x):
            return tanh_clip(np.exp(x * np.log(np.where(x <= 0, 1e-6, x))), scale=0.5)

        def f9(x):
            return np.sin(x) / (x**2 + eps)

        def f10(x):
            return approx_sum_sin_factorial(x, M=6)

        def f11(x):
            return np.sin(np.sqrt(np.abs(x)))

        def f12(x):
            frac = x - np.floor(x)
            return np.cos(np.pi * frac)

        def f13(x):
            safe = np.where(x <= 1e-6, 1e-6, x)
            log2 = np.floor(np.log2(safe))
            val = (np.pi / 2.0) * (2.0**log2)
            return np.sin(val)

        def f14(x):
            return np.sin(x) + np.sin(np.pi * x)

        def f15(x):
            return np.sign(np.sin(1.0 / (x + eps)))  # Added eps

        def f16(x):
            denom = np.cos(x) ** 2 + 1e-6
            raw = 1.0 / denom
            return tanh_clip(raw, scale=0.6)

        final_funcs = [
            f1,
            f2,
            f3,
            f4,
            f5,
            f6,
            f7,
            f8,
            f9,
            f10,
            f11,
            f12,
            f13,
            f14,
            f15,
            f16,
        ]

        # ---------- compute y values per-phase and blend ----------
        def compute_phase1_y(i):
            # Phase 1: Pure sin(x) + k offset, using fixed x_norm_periodic domain.
            z = x_norm_periodic + (i / NUM_WAVES) * (2 * np.pi)
            return amp_base * np.sin(z) + y_centers[i]

        def compute_phase2_y(i):
            # Phase 2: Pairwise functions (8 formulas)
            pair_idx = i // 2
            func = mid_funcs[pair_idx % len(mid_funcs)]
            z = x_norm_periodic
            try:
                raw = func(z)
            except Exception:
                raw = np.zeros_like(z)
            return amp_base * raw + y_centers[i]

        def compute_phase3_y(i):
            # Phase 3: 16 Chaotic functions using x_pos domain, now mingled
            func = final_funcs[i]
            # Apply individual x_offsets for more unique chaos
            x_arg = x_pos_base + chaos_x_offsets[i]
            try:
                raw = func(x_arg)
            except Exception:
                raw = np.zeros_like(x_arg)

            # Scale raw output to fit screen
            # NEW: No y_centers here, allowing full vertical overlap
            # NEW: Use amp_chaos for larger vertical span
            # NEW: Add individual y_offsets to differentiate starting positions
            raw_norm = tanh_clip(raw, scale=1.0)  # Still tanh clip for boundedness
            return amp_chaos * raw_norm + chaos_y_offsets[i]

        # Blended y: Interpolates between the three phases
        def compute_blended_pts(i):
            y1 = compute_phase1_y(i)
            y2 = compute_phase2_y(i)
            y3 = compute_phase3_y(i)

            a = pair_phase.get_value()  # 0->1 during PH2
            b = full_phase.get_value()  # 0->1 during PH3

            # Blending logic for y-values
            # (1-a)*y1 + a*y2 = blend between P1 and P2
            y12 = (1 - a) * y1 + a * y2

            # (1-b)*y12 + b*y3 = blend result of (P1<->P2) with P3
            # IMPORTANT: For phase 3, we want to completely override the vertical centering
            # so the waves can mingle. This is achieved by having y3 compute its own full position.
            # We effectively blend (y12) towards (y3).
            y = (1 - b) * y12 + b * y3

            pts = [np.array([xs_screen[j], y[j], 0]) for j in range(len(xs_screen))]
            return pts

        # ---------- create VMobjects and updaters ----------
        waves = VGroup()
        for i in range(NUM_WAVES):
            pts0 = compute_blended_pts(i)
            w = VMobject()
            w.set_points_as_corners(pts0)
            w.set_stroke(colors[i], width=2.6, opacity=0.97)
            w.make_smooth()

            def make_updater(ii):
                def updater(mob):
                    pts_new = compute_blended_pts(ii)
                    mob.set_points_as_corners(pts_new)
                    mob.make_smooth()

                return updater

            w.add_updater(make_updater(i))
            waves.add(w)

        # background and add
        self.add(FullScreenRectangle(fill_color=BLACK, fill_opacity=1.0), waves)

        # PHASE 1: pure sin+offset, held STATIC for PH1 secs
        self.wait(PH1)

        # PHASE 2: Morph to the 8 pairwise formulas over PH2 secs
        self.play(pair_phase.animate.set_value(1.0), run_time=PH2, rate_func=smooth)

        # PHASE 3: Morph to the 16 chaotic formulas over PH3 secs
        self.play(full_phase.animate.set_value(1.0), run_time=PH3, rate_func=smooth)

        # hold a little and fade out
        self.wait(0.5)
        for w in waves:
            w.clear_updaters()
        self.play(FadeOut(waves, run_time=0.6))
        self.wait(0.2)
