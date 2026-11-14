import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
from matplotlib.patches import Circle, Rectangle

plt.rcParams["font.family"] = ["PingFang SC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

INK, ORANGE, BLUE = "#2b2b2b", "#d2691e", "#2f4f6f"
CREAM, RED, GREEN, GREY, BROWN = "#f3e3ce", "#b03a2e", "#4a7c59", "#8a8a8a", "#7a5230"
BASE = "/Users/fred/Documents/GitHub/cycleuser/blog/output/img/kaoyan-math/"
F = 12          # 注释字号
T = 13.5        # 标题字号


def frame(ax, xlim, ylim, title):
    ax.axhline(0, color="#d8d8d8", lw=0.9, zorder=1)
    ax.axvline(0, color="#d8d8d8", lw=0.9, zorder=1)
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.set_xlabel("$x$", fontsize=11, color=INK)
    ax.set_ylabel("$y$", fontsize=11, color=INK)
    ax.tick_params(colors="#666", labelsize=9)
    for sp in ax.spines.values():
        sp.set_color("#bbbbbb")
    ax.set_title(title, fontsize=T, color=INK, pad=10)


def right_angle(ax, corner, u, v, s=0.20, color=RED):
    p1 = corner + s * u
    p2 = p1 + s * v
    p3 = corner + s * v
    ax.plot([p1[0], p2[0], p3[0]], [p1[1], p2[1], p3[1]], color=color, lw=1.1, zorder=6)


# ============ 1 标准式 ============
fig, ax = plt.subplots(figsize=(6.8, 5.4), dpi=150)
a, b, r = 0.9, -0.7, 1.6
frame(ax, (-1.8, 3.4), (-3.9, 1.6), "标准式：圆心与半径")
ax.add_patch(Circle((a, b), r, facecolor="none", edgecolor=BLUE, lw=2.6, zorder=3))
ax.plot([a, a], [b, 0], color=GREY, lw=1.2, ls="--", zorder=2)
ax.plot([0, a], [0, 0], color=GREY, lw=1.2, ls="--", zorder=2)
ax.plot([0, a], [b, b], color=GREY, lw=1.2, ls="--", zorder=2)
ax.plot([a], [0], "o", color=GREY, ms=5, zorder=4)
ax.plot([a], [b], "o", color=RED, ms=10, zorder=6)
ang = np.deg2rad(58)
P = (a + r * np.cos(ang), b + r * np.sin(ang))
ax.plot([a, P[0]], [b, P[1]], color=ORANGE, lw=2.4, zorder=5)
ax.plot(*P, "o", color=GREEN, ms=8, zorder=6)
ax.text(a - 0.14, b - 0.42, "$(a,b)$", fontsize=F, color=RED, ha="center")
ax.text((a + P[0]) / 2 - 0.05, (b + P[1]) / 2 + 0.12, "$r$", fontsize=F + 1, color=ORANGE)
ax.text(a / 2 - 0.05, -0.36, "$a$", fontsize=F, color=GREY)
ax.text(a - 0.22, b / 2 - 0.06, "$b$", fontsize=F, color=GREY)
ax.text(-1.75, -2.75, r"$(x-a)^2+(y-b)^2=r^2$", fontsize=F + 1, color=BLUE)
ax.text(-1.75, -3.20, "圆上每一点到 $(a,b)$ 的距离都等于 $r$", fontsize=F - 1.5, color=INK)
ax.text(-1.75, -3.65, "把左边展开就得到一般式", fontsize=F - 1.5, color=GREY)
fig.tight_layout(); fig.savefig(BASE + "circle-standard.png", dpi=150); plt.close(fig)


# ============ 2 一般式与配方 ============
fig, ax = plt.subplots(figsize=(6.8, 5.4), dpi=150)
frame(ax, (-3.9, 2.4), (-3.6, 0.4), "一般式：配方读出圆心与半径")
O = np.array([1.0, -2.0]); r = 1.0
ax.add_patch(Circle(O, r, facecolor=CREAM, alpha=0.9, edgecolor=BLUE, lw=2.6, zorder=3))
ax.plot([O[0], O[0]], [O[1], 0], color=GREY, lw=1.0, ls="--", zorder=2)
ax.plot([0, O[0]], [O[1], O[1]], color=GREY, lw=1.0, ls="--", zorder=2)
ax.plot(*O, "o", color=RED, ms=9, zorder=6)
ax.plot([O[0], O[0] + r], [O[1], O[1]], color=ORANGE, lw=2.2, zorder=5)
ax.text(O[0] + 0.45, O[1] + 0.12, "$r=1$", fontsize=F - 0.5, color=ORANGE)
ax.text(O[0] + 0.10, O[1] - 0.38, "$(1,-2)$", fontsize=F - 0.5, color=RED)
ax.text(-3.85, -0.10, r"$x^2+y^2-2x+4y+4=0$", fontsize=F, color=INK)
ax.text(-3.85, -0.68, r"$(x^2-2x+1)+(y^2+4y+4)=1$", fontsize=F - 1, color=INK)
ax.text(-3.85, -1.20, r"$(x-1)^2+(y+2)^2=1$", fontsize=F + 1, color=BLUE)
ax.text(-3.85, -1.75, r"$D=-2,\quad E=4,\quad F=4$", fontsize=F - 1, color=GREY)
ax.text(-3.85, -2.30, r"圆心 $\left(-\frac{D}{2},-\frac{E}{2}\right)=(1,-2)$", fontsize=F - 2, color=INK)
ax.text(-3.85, -2.85, r"半径 $\frac{1}{2}\sqrt{D^2+E^2-4F}=1$", fontsize=F - 2, color=INK)
fig.tight_layout(); fig.savefig(BASE + "circle-general.png", dpi=150); plt.close(fig)


# ============ 3 参数式 ============
fig, ax = plt.subplots(figsize=(6.8, 5.4), dpi=150)
frame(ax, (-1.8, 2.0), (-1.7, 2.2), "参数式：$t$ 是圆心角")
r = 1.2
ax.add_patch(Circle((0, 0), r, facecolor="none", edgecolor=BLUE, lw=2.6, zorder=3))
t0 = np.deg2rad(54)
P = np.array([r * np.cos(t0), r * np.sin(t0)])
ax.plot([0, P[0]], [0, P[1]], color=GREY, lw=1.4, ls="--", zorder=4)
ax.plot([0, P[0]], [0, 0], color=GREEN, lw=2.0, zorder=4)
ax.plot([P[0], P[0]], [0, P[1]], color=ORANGE, lw=2.0, zorder=4)
ax.plot(*P, "o", color=RED, ms=9, zorder=6)
ax.add_patch(mpatches.Arc((0, 0), 0.75, 0.75, theta1=0, theta2=54, color=GREY, lw=1.4))
ax.text(0.44, 0.16, "$t$", fontsize=F + 1, color=GREY)
ax.text(P[0] / 2 - 0.10, -0.30, r"$r\cos t$", fontsize=F - 0.5, color=GREEN)
ax.text(P[0] + 0.09, P[1] * 0.42, r"$r\sin t$", fontsize=F - 1, color=ORANGE, rotation=90)
ax.text(P[0] + 0.12, P[1] + 0.12, "$P$", fontsize=F, color=RED)
ax.text(-1.75, 1.95, r"$x=a+r\cos t$", fontsize=F, color=INK)
ax.text(-1.75, 1.58, r"$y=b+r\sin t$", fontsize=F, color=INK)
fig.tight_layout(); fig.savefig(BASE + "circle-parametric.png", dpi=150); plt.close(fig)


# ============ 4 切线 ============
fig, ax = plt.subplots(figsize=(6.8, 5.4), dpi=150)
frame(ax, (-2.2, 2.6), (-2.0, 2.0), "切线：半径与切线垂直")
r = 1.2
ax.add_patch(Circle((0, 0), r, facecolor="none", edgecolor=BLUE, lw=2.6, zorder=3))
ta = np.deg2rad(42)
TP = np.array([r * np.cos(ta), r * np.sin(ta)])
d = np.array([-np.sin(ta), np.cos(ta)])
ax.plot([TP[0] - 1.25 * d[0], TP[0] + 1.25 * d[0]],
        [TP[1] - 1.25 * d[1], TP[1] + 1.25 * d[1]], color=RED, lw=2.4, zorder=4)
ax.plot([0, TP[0]], [0, TP[1]], color=ORANGE, lw=2.0, zorder=4)
ax.plot(*TP, "o", color=GREEN, ms=9, zorder=6)
right_angle(ax, TP, -np.array([np.cos(ta), np.sin(ta)]), d, s=0.24)
ax.text(TP[0] + 0.14, TP[1] + 0.14, "$T(x_0,y_0)$", fontsize=F - 0.5, color=GREEN)
ax.text(0.12, r / 2 - 0.10, "$r$", fontsize=F + 1, color=ORANGE)
ax.text(-2.10, 1.75, r"$(x_0-a)(x-a)+(y_0-b)(y-b)=r^2$", fontsize=F - 1, color=RED)
ax.text(-2.10, 1.30, "切线方向垂直于半径方向", fontsize=F - 1.5, color=INK)
fig.tight_layout(); fig.savefig(BASE + "circle-tangent.png", dpi=150); plt.close(fig)


# ============ 5 切线长 ============
fig, ax = plt.subplots(figsize=(6.8, 5.4), dpi=150)
frame(ax, (-2.0, 3.0), (-2.0, 2.4), "切线长：用直角三角形算")
O = np.array([-0.55, -0.15]); r = 1.05
ax.add_patch(Circle(O, r, facecolor="none", edgecolor=BLUE, lw=2.6, zorder=3))
P = np.array([1.55, 0.85])
dP = np.linalg.norm(P - O)
al = np.arccos(r / dP)
base = np.arctan2(P[1] - O[1], P[0] - O[0])
for sgn in (1, -1):
    TP = O + r * np.array([np.cos(base + sgn * al), np.sin(base + sgn * al)])
    ax.plot([P[0], TP[0]], [P[1], TP[1]], color=RED, lw=2.2, zorder=4)
    ax.plot([O[0], TP[0]], [O[1], TP[1]], color=ORANGE, lw=1.8, zorder=4)
    ax.plot(*TP, "o", color=GREEN, ms=8, zorder=6)
    u = (TP - O) / np.linalg.norm(TP - O)
    v = (P - TP) / np.linalg.norm(P - TP)
    right_angle(ax, TP, -u, v, s=0.22)
ax.plot([O[0], P[0]], [O[1], P[1]], color=BROWN, lw=1.4, ls=":", zorder=4)
ax.plot(*O, "o", color=BLUE, ms=7, zorder=6)
ax.plot(*P, "o", color=RED, ms=9, zorder=6)
ax.text(O[0] - 0.05, O[1] - 0.38, "$O$", fontsize=F, color=BLUE)
ax.text(P[0] + 0.12, P[1] + 0.10, "$P$", fontsize=F, color=RED)
ax.text((O[0] + P[0]) / 2 - 0.15, (O[1] + P[1]) / 2 - 0.42, "$|PO|$", fontsize=F - 0.5, color=BROWN)
ax.text(-2.05, 2.05, r"$|PT|^2=|PO|^2-r^2$", fontsize=F + 1, color=RED)
ax.text(-2.05, 1.58, "两条切线一样长", fontsize=F - 1.5, color=INK)
fig.tight_layout(); fig.savefig(BASE + "circle-tangent-length.png", dpi=150); plt.close(fig)


# ============ 6 弦长 ============
fig, ax = plt.subplots(figsize=(6.8, 5.4), dpi=150)
frame(ax, (-2.2, 2.6), (-2.6, 2.0), "弦长：垂径定理")
r = 1.3
ax.add_patch(Circle((0, 0), r, facecolor="none", edgecolor=BLUE, lw=2.6, zorder=3))
y0 = 0.55
dx = np.sqrt(r ** 2 - y0 ** 2)
ax.plot([-1.95, 1.95], [y0, y0], color=GREY, lw=1.2, ls="--", zorder=2)
ax.plot([-dx, dx], [y0, y0], color=ORANGE, lw=3.2, zorder=5)
ax.plot([0, 0], [0, y0], color=GREEN, lw=2.0, zorder=4)
ax.plot([0, dx], [0, y0], color=BLUE, lw=1.6, ls=":", zorder=4)
ax.plot([-dx, dx], [y0, y0], "o", color=ORANGE, ms=7, zorder=6)
ax.plot([0], [0], "o", color=BLUE, ms=7, zorder=6)
right_angle(ax, np.array([0, y0]), np.array([1, 0]), np.array([0, 1]), s=0.18, color=GREEN)
ax.text(0.10, y0 / 2 - 0.05, "$d$", fontsize=F + 1, color=GREEN)
ax.text(dx / 2 - 0.30, y0 + 0.14, r"$\sqrt{r^2-d^2}$", fontsize=F - 1, color=ORANGE)
ax.text(0.78, 0.16, "$r$", fontsize=F, color=BLUE)
ax.text(-2.15, -1.85, r"$L=2\sqrt{r^2-d^2}$", fontsize=F + 1, color=ORANGE)
ax.text(-2.15, -2.35, "半弦、圆心距、半径构成直角三角形", fontsize=F - 2, color=INK)
fig.tight_layout(); fig.savefig(BASE + "circle-chord.png", dpi=150); plt.close(fig)


# ============ 7 点与圆 ============
fig, ax = plt.subplots(figsize=(6.8, 5.4), dpi=150)
frame(ax, (-2.2, 2.6), (-2.0, 2.0), "点与圆：比 $d$ 与 $r$")
r = 1.2
ax.add_patch(Circle((0, 0), r, facecolor="none", edgecolor=BLUE, lw=2.6, zorder=3))
cases = [(np.deg2rad(105), 0.6, GREEN, "$d<r$", (0.10, 0.22), "圆内"),
         (np.deg2rad(20), r, ORANGE, "$d=r$", (-0.55, 0.30), "圆上"),
         (np.deg2rad(-38), 1.95, RED, "$d>r$", (-1.30, 0.30), "圆外")]
for ang, rad, col, lab, (ox, oy), where in cases:
    p = rad * np.array([np.cos(ang), np.sin(ang)])
    ax.plot([0, p[0]], [0, p[1]], color=col, lw=1.6, ls="--", zorder=4)
    ax.plot(*p, "o", color=col, ms=9, zorder=6)
    ax.text(p[0] + ox, p[1] + oy, lab, fontsize=F - 1, color=col)
    ax.text(p[0] + ox, p[1] + oy - 0.28, where, fontsize=F - 2, color=col)
ax.text(-2.15, 1.70, r"$d=|PO|$，$r$ 是半径", fontsize=F - 1, color=INK)
fig.tight_layout(); fig.savefig(BASE + "circle-point-position.png", dpi=150); plt.close(fig)


# ============ 8 直线与圆 ============
fig, ax = plt.subplots(figsize=(6.8, 5.4), dpi=150)
frame(ax, (-2.0, 3.4), (-2.2, 2.4), "直线与圆：三种位置")
r = 1.2
ax.add_patch(Circle((0, 0), r, facecolor="none", edgecolor=BLUE, lw=2.6, zorder=3))
for y0, col, lab in [(-0.55, RED, "$d<r$：相交，两个交点"),
                     (r, GREEN, "$d=r$：相切，一个交点"),
                     (1.75, ORANGE, "$d>r$：相离，没有交点")]:
    ax.plot([-1.55, 1.55], [y0, y0], color=col, lw=2.0, zorder=4)
    ax.text(1.65, y0 - 0.08, lab, fontsize=F - 1.5, color=col)
ax.set_xlim(-2.0, 4.6)
fig.tight_layout(); fig.savefig(BASE + "circle-line-position.png", dpi=150); plt.close(fig)

print("circle figs done")
