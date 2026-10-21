import numpy as np
from tkinter import *
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# ══════════════════════════════════════════════════════════════════════════════
#  INVERSION 1  —  Link 1 (frame/ground) fixed
#  Standard slider-crank: A pinned to ground, rail is horizontal and fixed.
#  Crank AB rotates, rod BC connects to slider C which translates on fixed rail.
#  Real-world: IC engine piston
# ══════════════════════════════════════════════════════════════════════════════
class Inversion1App:
    def __init__(self, master, r, l):
        self.r, self.l, self.k = r, l, 0

        self.fig, self.ax = plt.subplots(figsize=(9, 5))
        self.fig.patch.set_facecolor('#f9f9f9')
        self.ax.set_facecolor('#f9f9f9')

        pad = max(r, l) * 0.4
        self.ax.set_xlim(-(r + pad), r + l + pad)
        self.ax.set_ylim(-(r + pad * 1.2), r + pad * 1.2)
        self.ax.set_aspect('equal')
        self.ax.grid(True, alpha=0.25, linestyle='--')
        self.ax.set_title("Inversion 1 — Standard (Link 1 / Frame fixed)\n"
                          "Crank rotates | Slider translates on fixed rail\n"
                          "Real-world: IC Engine / Reciprocating Pump", fontsize=9)

        # Fixed horizontal rail (hatched ground)
        rail_x = [-(r + pad * 0.6), r + l + pad * 0.6]
        self.ax.fill_between(rail_x, [-r * 0.08, -r * 0.08], [-r * 0.22, -r * 0.22],
                             color='#bbb', alpha=0.5, zorder=1)
        self.ax.plot(rail_x, [-r * 0.08, -r * 0.08], 'k-', lw=1.5, zorder=2)

        # Fixed ground pivot A
        self.ax.plot(0, 0, 'k^', ms=12, zorder=6)
        self.ax.text(-r * 0.15, -r * 0.28, 'A', fontsize=10, fontweight='bold')

        self.crank_line, = self.ax.plot([], [], '-', color='royalblue',  lw=5, solid_capstyle='round', zorder=3)
        self.rod_line,   = self.ax.plot([], [], '-', color='darkorange', lw=4, solid_capstyle='round', zorder=3)
        self.pin_dots,   = self.ax.plot([], [], 'o', color='#111',       ms=8, zorder=7)
        self.slider_box, = self.ax.plot([], [], 's', color='crimson',    ms=20, zorder=5)
        self.lbl         = self.ax.text(0, r * 0.85, '', fontsize=9, color='#555')

        FigureCanvasTkAgg(self.fig, master=master).get_tk_widget().place(x=0, y=0, height=500, width=800)
        Label(master, text="A pinned to ground  |  B = crank pin  |  C = slider translates on fixed horizontal rail",
              font=("Arial", 9, "italic"), fg="#555").place(x=80, y=505, width=640, height=18)
        Button(master, text="▶ Start", command=self.start, width=14, bg="#b6e8b6").place(x=150, y=528, height=28)
        Button(master, text="■ Stop",  command=self.stop,  width=14, bg="#e8b6b6").place(x=460, y=528, height=28)

        self.anim = animation.FuncAnimation(self.fig, self._animate,
                                            frames=np.linspace(0, 2 * np.pi, 180, endpoint=False),
                                            interval=20, blit=False, repeat=True)

    def _calc(self, theta):
        A = np.array([0.0, 0.0])
        B = A + self.r * np.array([np.cos(theta), np.sin(theta)])
        disc = self.l**2 - (self.r * np.sin(theta))**2
        xC = self.r * np.cos(theta) + np.sqrt(max(disc, 0))
        C = np.array([xC, 0.0])
        return A, B, C

    def start(self):
        self.k = 1; self.anim.event_source.start()

    def stop(self):
        self.k = 0; self.anim.event_source.stop()

    def _animate(self, theta):
        if not self.k:
            return self.crank_line, self.rod_line, self.pin_dots, self.slider_box
        A, B, C = self._calc(theta)
        self.crank_line.set_data([A[0], B[0]], [A[1], B[1]])
        self.rod_line.set_data([B[0], C[0]], [B[1], C[1]])
        self.pin_dots.set_data([A[0], B[0]], [A[1], B[1]])
        self.slider_box.set_data([C[0]], [C[1]])
        self.lbl.set_text(f"θ = {np.degrees(theta):.0f}°")
        return self.crank_line, self.rod_line, self.pin_dots, self.slider_box


# ══════════════════════════════════════════════════════════════════════════════
#  INVERSION 2  —  Link 2 (crank) fixed
#
#  Original links:  A──crank(r)──B──rod(l)──C──slider on fixed rail through A
#  Now fix link 2 (crank AB).  Both A and B are nailed to ground.
#
#  What moves:
#   • Link 1 (the frame/rail) is now free to ROTATE about A (it was ground before).
#   • The slider C is on the rotating rail (link 1) and is connected to fixed B
#     via the rod (link 3, length l).
#   • As link 1 rotates about A, the slider C moves along it so that |BC| = l.
#
#  Geometry each frame:
#   Let φ = angle of the rotating rail from x-axis.
#   Rail direction unit vector: u = [cosφ, sinφ]
#   Slider C is on the rail at distance s from A:  C = s·u
#   Constraint |BC|² = l²:
#     |s·u - B|² = l²
#     s² - 2s(B·u) + |B|² = l²
#     s² - 2s(r·cosφ) + r² = l²       [since B=(r,0), B·u = r·cosφ]
#     s = r·cosφ ± √(l² - r²sin²φ)
#   Take the positive root (C on same side as B).
#
#  The rail rotates fully (360°) — this is the oscillating cylinder / Rapson's slide.
#  Real-world: Oscillating Cylinder Steam Engine
# ══════════════════════════════════════════════════════════════════════════════
class Inversion2App:
    def __init__(self, master, r, l):
        self.r, self.l, self.k = r, l, 0

        self.fig, self.ax = plt.subplots(figsize=(9, 5))
        self.fig.patch.set_facecolor('#f9f9f9')
        self.ax.set_facecolor('#f9f9f9')

        pad = (r + l) * 0.4
        lim = r + l + pad
        self.ax.set_xlim(-lim * 0.5, lim * 0.8)
        self.ax.set_ylim(-lim * 0.65, lim * 0.65)
        self.ax.set_aspect('equal')
        self.ax.grid(True, alpha=0.25, linestyle='--')
        self.ax.set_title("Inversion 2 — Link 2 (Crank) fixed\n"
                          "Rail (Link 1) rotates about fixed A | Slider C on rail, constrained by fixed pin B\n"
                          "Real-world: Oscillating Cylinder Engine", fontsize=9)

        self.A = np.array([0.0, 0.0])    # fixed crank pivot
        self.B = np.array([r,   0.0])    # fixed crank pin

        # Draw fixed crank as bold bar
        self.ax.plot([self.A[0], self.B[0]], [self.A[1], self.B[1]],
                     '-', color='#333', lw=9, solid_capstyle='round', zorder=3)
        self.ax.plot(*self.A, 'k^', ms=13, zorder=8)
        self.ax.plot(*self.B, 'k^', ms=13, zorder=8)
        self.ax.text(self.A[0] - r * 0.05, -r * 0.22, 'A (fixed)', fontsize=8, ha='center', color='#333')
        self.ax.text(self.B[0] + r * 0.05, -r * 0.22, 'B (fixed pin)', fontsize=8, ha='center', color='#333')

        # Artists
        self.rail_line,  = self.ax.plot([], [], '-', color='#999',      lw=7, solid_capstyle='round', zorder=2, alpha=0.6)
        self.rod_line,   = self.ax.plot([], [], '-', color='darkorange', lw=4, solid_capstyle='round', zorder=4)
        self.slider_box, = self.ax.plot([], [], 's', color='crimson',    ms=22, zorder=6)
        self.pin_dot,    = self.ax.plot([], [], 'o', color='#111',       ms=9,  zorder=9)
        self.lbl         = self.ax.text(-(r + l) * 0.45, lim * 0.55, '', fontsize=9, color='#555')

        FigureCanvasTkAgg(self.fig, master=master).get_tk_widget().place(x=0, y=0, height=500, width=800)
        Label(master, text="A, B both fixed (crank is ground) | Rail rotates about A | Slider C on rail, |BC|=l",
              font=("Arial", 9, "italic"), fg="#555").place(x=80, y=505, width=640, height=18)
        Button(master, text="▶ Start", command=self.start, width=14, bg="#b6e8b6").place(x=150, y=528, height=28)
        Button(master, text="■ Stop",  command=self.stop,  width=14, bg="#e8b6b6").place(x=460, y=528, height=28)

        self.anim = animation.FuncAnimation(self.fig, self._animate,
                                            frames=np.linspace(0, 2 * np.pi, 180, endpoint=False),
                                            interval=20, blit=False, repeat=True)

    def _calc(self, phi):
        u = np.array([np.cos(phi), np.sin(phi)])
        # B · u = r*cosφ
        B_dot_u = self.r * np.cos(phi)
        disc = self.l**2 - self.r**2 * np.sin(phi)**2
        disc = max(disc, 0)
        s = B_dot_u + np.sqrt(disc)          # positive root → C on far side
        C = s * u
        rail_len = self.r + self.l
        rail_start = -u * rail_len * 0.3     # behind A
        rail_end   =  u * rail_len * 1.05    # beyond C
        return C, rail_start, rail_end

    def start(self):
        self.k = 1; self.anim.event_source.start()

    def stop(self):
        self.k = 0; self.anim.event_source.stop()

    def _animate(self, phi):
        if not self.k:
            return self.rail_line, self.rod_line, self.slider_box, self.pin_dot
        C, rs, re = self._calc(phi)
        self.rail_line.set_data([rs[0], re[0]], [rs[1], re[1]])
        self.rod_line.set_data([C[0], self.B[0]], [C[1], self.B[1]])
        self.slider_box.set_data([C[0]], [C[1]])
        self.pin_dot.set_data([C[0]], [C[1]])
        rod_len = np.linalg.norm(C - self.B)
        self.lbl.set_text(f"φ = {np.degrees(phi):.0f}°  |  BC = {rod_len:.1f}")
        return self.rail_line, self.rod_line, self.slider_box, self.pin_dot


# ══════════════════════════════════════════════════════════════════════════════
#  INVERSION 3  —  Link 3 (connecting rod) fixed
#
#  Original links:  A──crank(r)──B──rod(l)──C──slider on rail through A
#  Fix link 3 (rod BC, length l).  B and C are now both fixed to ground.
#   B = (0, 0),  C = (l, 0)
#
#  What moves:
#   • Link 2 (crank, length r) rotates about fixed B.  Its free end is A (old
#     crank pivot, now moving).  A traces a circle of radius r about B.
#   • Link 1 (old frame/rail) is pinned at A (moving) and passes through fixed C.
#     C is the fixed slider pivot — the axis slides THROUGH C.
#   • The slider (link 4) is at C, pinned to ground; the axis (link 1) slides
#     through it.
#
#  So the AXIS (link 1) always passes through both A (moving) and C (fixed).
#  Its direction is the line AC.  It can rotate to any angle.
#
#  For r < l  →  Turning Block Mechanism
#  For r > l  →  Whitworth Quick-Return Mechanism
#
#  Real-world: Whitworth Quick-Return (shaping machines)
# ══════════════════════════════════════════════════════════════════════════════
class Inversion3App:
    def __init__(self, master, r, l):
        self.r, self.l, self.k = r, l, 0

        self.fig, self.ax = plt.subplots(figsize=(9, 5))
        self.fig.patch.set_facecolor('#f9f9f9')
        self.ax.set_facecolor('#f9f9f9')

        scale = max(r, l)
        pad = scale * 0.65
        self.ax.set_xlim(-(scale + pad), l + scale + pad)
        self.ax.set_ylim(-(scale + pad), scale + pad)
        self.ax.set_aspect('equal')
        self.ax.grid(True, alpha=0.25, linestyle='--')
        mech = "Whitworth Quick-Return" if r > l else "Turning Block"
        self.ax.set_title(f"Inversion 3 — Link 3 (Connecting Rod) fixed  →  {mech}\n"
                          "B and C fixed | Crank end A circles B | Axis (Link 1) rotates, slides through fixed C",
                          fontsize=9)

        self.B = np.array([0.0, 0.0])    # fixed
        self.C = np.array([l,   0.0])    # fixed slider pivot

        # Fixed rod BC = ground
        self.ax.plot([self.B[0], self.C[0]], [self.B[1], self.C[1]],
                     '-', color='#333', lw=9, solid_capstyle='round', zorder=3)
        self.ax.plot(*self.B, 'k^', ms=13, zorder=8)
        self.ax.plot(*self.C, 'k^', ms=13, zorder=8)
        self.ax.text(self.B[0] - scale * 0.04, -scale * 0.18, 'B\n(fixed crank pivot)', fontsize=8, ha='center', color='#333')
        self.ax.text(self.C[0] + scale * 0.04, -scale * 0.18, 'C\n(fixed slider pivot)', fontsize=8, ha='center', color='#333')

        # Artists
        self.crank_line, = self.ax.plot([], [], '-', color='royalblue',  lw=6, solid_capstyle='round', zorder=4)
        self.axis_line,  = self.ax.plot([], [], '-', color='#999',       lw=7, solid_capstyle='round', zorder=2, alpha=0.55)
        self.slider_sq,  = self.ax.plot([], [], 's', color='crimson',    ms=20, zorder=6)
        self.joint_dots, = self.ax.plot([], [], 'o', color='#111',       ms=9,  zorder=9)
        self.lbl         = self.ax.text(-(scale + pad * 0.7), scale * 0.82, '', fontsize=9, color='#555')

        FigureCanvasTkAgg(self.fig, master=master).get_tk_widget().place(x=0, y=0, height=500, width=800)
        Label(master, text=f"{mech} | B, C fixed (rod is ground) | Crank pin A circles B | Axis slides through C",
              font=("Arial", 9, "italic"), fg="#555").place(x=60, y=505, width=680, height=18)
        Button(master, text="▶ Start", command=self.start, width=14, bg="#b6e8b6").place(x=150, y=528, height=28)
        Button(master, text="■ Stop",  command=self.stop,  width=14, bg="#e8b6b6").place(x=460, y=528, height=28)

        self.anim = animation.FuncAnimation(self.fig, self._animate,
                                            frames=np.linspace(0, 2 * np.pi, 180, endpoint=False),
                                            interval=20, blit=False, repeat=True)

    def _calc(self, theta):
        # A = moving crank pin, circles B with radius r
        A = self.B + self.r * np.array([np.cos(theta), np.sin(theta)])
        # Axis (link 1) direction = from A through C (and beyond both ways)
        AC = self.C - A
        dist_AC = np.linalg.norm(AC)
        if dist_AC < 1e-9:
            u = np.array([1.0, 0.0])
        else:
            u = AC / dist_AC
        # Slider is at fixed C (axis slides through C)
        # Extend axis line well past both A and C
        axis_len = self.r + self.l
        axis_start = A - u * axis_len * 0.5   # behind A
        axis_end   = self.C + u * axis_len * 0.5  # beyond C
        return A, axis_start, axis_end

    def start(self):
        self.k = 1; self.anim.event_source.start()

    def stop(self):
        self.k = 0; self.anim.event_source.stop()

    def _animate(self, theta):
        if not self.k:
            return self.crank_line, self.axis_line, self.slider_sq, self.joint_dots
        A, ax_s, ax_e = self._calc(theta)
        self.crank_line.set_data([self.B[0], A[0]], [self.B[1], A[1]])
        self.axis_line.set_data([ax_s[0], ax_e[0]], [ax_s[1], ax_e[1]])
        self.slider_sq.set_data([self.C[0]], [self.C[1]])
        self.joint_dots.set_data([self.B[0], A[0], self.C[0]],
                                  [self.B[1], A[1], self.C[1]])
        self.lbl.set_text(f"θ = {np.degrees(theta):.0f}°")
        return self.crank_line, self.axis_line, self.slider_sq, self.joint_dots


# ══════════════════════════════════════════════════════════════════════════════
#  INVERSION 4  —  Link 4 (slider / piston) fixed
#
#  Original links:  A──crank(r)──B──rod(l)──C──slider on rail through A
#  Fix link 4 (the slider block at C).  C is nailed to ground at origin.
#
#  What moves:
#   • The slider axis (link 1 / the rail) is no longer fixed — it can rotate.
#     It still passes through A (crank pivot) and C (fixed slider).
#     But C is fixed now, so the axis rotates about C.
#   • As the axis rotates about C by angle ψ, A is the crank pivot on the
#     rotating axis at some distance from C.
#   • Crank AB (length r) rotates about A (the moving crank pivot).
#   • Rod BC (length l) connects crank pin B back to fixed C.
#
#  The distance AC (frame length) is NOT a separate link in the original —
#  it's the distance along the slider axis from the slider to the crank pivot.
#  Per the problem hint: "assume sufficiently large length of sliding axis".
#  We use d = l (a convenient choice that gives a visible mechanism).
#
#  Geometry each frame:
#   ψ = rotation of the frame (axis) about fixed C
#   A = C + d * [cosψ, sinψ]       d = chosen frame length
#   B = crank pin, |AB| = r, |BC| = l
#   Constraint: |B - C| = l
#     B = A + r[cos(ψ+α), sin(ψ+α)]
#     |B - C|² = l²
#     |A - C + r·e|² = l²
#     d² + 2d·r·cos(α) + r² = l²     (using |A-C| = d, e = unit crank vector relative to rail)
#     cos(α) = (l² - d² - r²) / (2dr)
#
#  For this to have a solution: |l² - d² - r²| ≤ 2dr
#  With d = l*0.8: cos(α) = (l² - 0.64l² - r²)/(2*0.8l*r) = (0.36l² - r²)/(1.6lr)
#  Works when r < 0.6l roughly.  If r is large we adjust d automatically.
#
#  Real-world: Gnome Rotary Engine (WWI aircraft)
# ══════════════════════════════════════════════════════════════════════════════
class Inversion4App:
    def __init__(self, master, r, l):
        self.r, self.l, self.k = r, l, 0

        # Choose frame length d so that assembly is possible
        # Need |l² - d² - r²| ≤ 2dr  →  (l-r) ≤ d ≤ (l+r)  and d > 0
        # Simple choice: d = (l + r) * 0.5  always in range
        self.d = (l + r) * 0.5

        self.fig, self.ax = plt.subplots(figsize=(9, 5))
        self.fig.patch.set_facecolor('#f9f9f9')
        self.ax.set_facecolor('#f9f9f9')

        scale = self.d + r
        pad = scale * 0.4
        self.ax.set_xlim(-(scale + pad), scale + pad)
        self.ax.set_ylim(-(scale + pad), scale + pad)
        self.ax.set_aspect('equal')
        self.ax.grid(True, alpha=0.25, linestyle='--')
        self.ax.set_title("Inversion 4 — Link 4 (Slider / Piston) fixed\n"
                          "Slider C fixed at origin | Frame (axis) rotates about C | Entire mechanism revolves\n"
                          "Real-world: Gnome Rotary Engine", fontsize=9)

        # Reference circle: path of crank pivot A
        theta_arr = np.linspace(0, 2 * np.pi, 300)
        self.ax.plot(self.d * np.cos(theta_arr), self.d * np.sin(theta_arr),
                     '--', color='steelblue', lw=0.8, alpha=0.35, zorder=1)

        # Fixed slider C at origin
        self.C = np.array([0.0, 0.0])
        self.ax.plot(*self.C, 'ks', ms=20, zorder=8)
        self.ax.text(0, -scale * 0.14, 'C (fixed slider)', fontsize=9,
                     fontweight='bold', ha='center', color='#333')

        # Artists
        self.rail_line,  = self.ax.plot([], [], '-', color='#aaa',      lw=8, solid_capstyle='round', zorder=2, alpha=0.55)
        self.crank_line, = self.ax.plot([], [], '-', color='royalblue',  lw=5, solid_capstyle='round', zorder=4)
        self.rod_line,   = self.ax.plot([], [], '-', color='darkorange', lw=4, solid_capstyle='round', zorder=4)
        self.joint_dots, = self.ax.plot([], [], 'o', color='#111',       ms=9, zorder=9)
        self.lbl         = self.ax.text(-(scale + pad * 0.5), scale * 0.82, '', fontsize=9, color='#555')

        FigureCanvasTkAgg(self.fig, master=master).get_tk_widget().place(x=0, y=0, height=500, width=800)
        Label(master, text=f"Slider C fixed | Frame rotates about C | d = {self.d:.1f}  |  Crank r={r}, Rod l={l}",
              font=("Arial", 9, "italic"), fg="#555").place(x=80, y=505, width=640, height=18)
        Button(master, text="▶ Start", command=self.start, width=14, bg="#b6e8b6").place(x=150, y=528, height=28)
        Button(master, text="■ Stop",  command=self.stop,  width=14, bg="#e8b6b6").place(x=460, y=528, height=28)

        self.anim = animation.FuncAnimation(self.fig, self._animate,
                                            frames=np.linspace(0, 2 * np.pi, 180, endpoint=False),
                                            interval=20, blit=False, repeat=True)

    def _calc(self, psi):
        # psi = rotation of axis (frame, link 1) about fixed C
        u = np.array([np.cos(psi), np.sin(psi)])   # unit vector along rotating axis
        A = self.C + self.d * u                     # crank pivot on rotating axis

        # Solve for crank angle alpha (measured from axis direction)
        # cos(alpha) = (l² - d² - r²) / (2*d*r)
        numerator = self.l**2 - self.d**2 - self.r**2
        denominator = 2 * self.d * self.r
        cos_alpha = np.clip(numerator / denominator, -1, 1)
        alpha = np.arccos(cos_alpha)

        # Two solutions for B; pick the one that varies smoothly
        # Use psi + alpha (the crank turns relative to the axis)
        phi = psi + alpha
        B = A + self.r * np.array([np.cos(phi), np.sin(phi)])

        # Rail: extend from behind C through A
        rail_start = self.C - u * self.d * 0.3
        rail_end   = A + u * self.r * 0.4

        return A, B, rail_start, rail_end

    def start(self):
        self.k = 1; self.anim.event_source.start()

    def stop(self):
        self.k = 0; self.anim.event_source.stop()

    def _animate(self, psi):
        if not self.k:
            return self.rail_line, self.crank_line, self.rod_line, self.joint_dots
        A, B, rs, re = self._calc(psi)
        self.rail_line.set_data([rs[0], re[0]], [rs[1], re[1]])
        self.crank_line.set_data([A[0], B[0]], [A[1], B[1]])
        self.rod_line.set_data([B[0], self.C[0]], [B[1], self.C[1]])
        self.joint_dots.set_data([A[0], B[0]], [A[1], B[1]])
        self.lbl.set_text(f"ψ = {np.degrees(psi):.0f}°  |  |BC| = {np.linalg.norm(B - self.C):.1f}")
        return self.rail_line, self.crank_line, self.rod_line, self.joint_dots


# ══════════════════════════════════════════════════════════════════════════════
#  LAUNCHER — tabbed window with all 4 inversions
# ══════════════════════════════════════════════════════════════════════════════
def launch_slider_crank_inversions(r, l, parent=None):
    from tkinter import ttk

    win = Toplevel(parent)
    win.title(f"Slider-Crank — All 4 Inversions  (r={r}, l={l})")
    win.geometry("830x580")
    win.resizable(False, False)

    style = ttk.Style()
    style.theme_use('clam')
    style.configure('Inv.TNotebook',     background='#ececec', borderwidth=0)
    style.configure('Inv.TNotebook.Tab', background='#d5d5d5', foreground='#222',
                                         padding=[14, 6], font=('Arial', 9, 'bold'))
    style.map('Inv.TNotebook.Tab',
              background=[('selected', '#ffffff')],
              foreground=[('selected', '#003a8c')])

    nb = ttk.Notebook(win, style='Inv.TNotebook')
    nb.pack(fill=BOTH, expand=True)

    configs = [
        ("Inv 1 — Standard",       Inversion1App),
        ("Inv 2 — Osc. Cylinder",  Inversion2App),
        ("Inv 3 — Whitworth QR",   Inversion3App),
        ("Inv 4 — Rotary Engine",  Inversion4App),
    ]

    for tab_label, AppClass in configs:
        frame = Frame(nb, bg='#f9f9f9', width=830, height=580)
        frame.pack_propagate(False)
        nb.add(frame, text=tab_label)
        AppClass(frame, r, l)


# ══════════════════════════════════════════════════════════════════════════════
#  Standalone test
# ══════════════════════════════════════════════════════════════════════════════
if __name__ == "__main__":
    root = Tk()
    root.withdraw()
    launch_slider_crank_inversions(r=60, l=160, parent=root)
    root.mainloop()