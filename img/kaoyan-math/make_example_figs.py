import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
from matplotlib.patches import Circle, Polygon

plt.rcParams["font.family"] = ["PingFang SC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

INK, ORANGE, BLUE = "#2b2b2b", "#d2691e", "#2f4f6f"
CREAM, RED, GREEN, GREY, BROWN = "#f3e3ce", "#b03a2e", "#4a7c59", "#8a8a8a", "#7a5230"
BASE = "/Users/fred/Documents/GitHub/cycleuser/blog/output/img/kaoyan-math/"
F, T = 12, 12.5


def frame(ax, xlim, ylim, title=""):
    ax.axhline(0, color="#d8d8d8", lw=0.9, zorder=1)
    ax.axvline(0, color="#d8d8d8", lw=0.9, zorder=1)
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.set_xlabel("$x$", fontsize=10, color=INK)
    ax.set_ylabel("$y$", fontsize=10, color=INK)
    ax.tick_params(colors="#666", labelsize=8.5)
    for sp in ax.spines.values():
        sp.set_color("#bbbbbb")
    if title:
        ax.set_title(title, fontsize=T, color=INK, pad=8)


# ============ 1 例：距离、中点、定比分点 ============
fig, ax = plt.subplots(figsize=(6.4, 5.0), dpi=150)
frame(ax, (-0.6, 5.2), (-0.6, 7.0), "例：A(1,2)、B(4,6)")
A, B = np.array([1, 2]), np.array([4, 6])
ax.plot([A[0], B[0]], [A[1], B[1]], color=BLUE, lw=2.4, zorder=4)
ax.plot([A[0], B[0]], [A[1], A[1]], color=GREY, lw=1.2, ls="--", zorder=2)
ax.plot([B[0], B[0]], [A[1], B[1]], color=GREY, lw=1.2, ls="--", zorder=2)
ax.text(2.5, 1.68, "$4-1=3$", fontsize=F - 1, color=GREY, ha="center")
ax.text(4.12, 4.0, "$6-2=4$", fontsize=F - 1, color=GREY)
M = (A + B) / 2
P = (A + 2 * B) / 3
for pt, lab, col, off in [(A, "$A(1,2)$", ORANGE, (-1.42, -0.05)), (B, "$B(4,6)$", ORANGE, (0.12, 0.12)),
                          (M, "$M(2.5,4)$", GREEN, (-1.85, -0.40)), (P, "$P(3,\\frac{14}{3})$", RED, (0.16, 0.30))]:
    ax.plot(*pt, "o", color=col, ms=9 if pt is not P else 8, zorder=6)
    ax.text(pt[0] + off[0], pt[1] + off[1], lab, fontsize=F - 1, color=col)
ax.text(3.35, 2.55, "$|AB|=5$", fontsize=F, color=BLUE)
ax.annotate("", xy=(3.15, 4.35), xytext=(3.45, 2.75),
            arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.0))
fig.tight_layout(); fig.savefig(BASE + "ex-distance.png", dpi=150); plt.close(fig)


# ============ 2 例：P(2,-1) 到 3x-4y+5=0 ============
fig, ax = plt.subplots(figsize=(6.4, 5.0), dpi=150)
frame(ax, (-1.8, 4.2), (-2.6, 3.0), "例：$P(2,-1)$ 到 $3x-4y+5=0$")
xs = np.linspace(-1.7, 4.1, 10)
ax.plot(xs, (3 * xs + 5) / 4, color=BLUE, lw=2.4, zorder=3)
P = np.array([2.0, -1.0])
A, B, C = 3, -4, 5
t = -(A * P[0] + B * P[1] + C) / (A * A + B * B)
Q = P + t * np.array([A, B])
ax.plot([P[0], Q[0]], [P[1], Q[1]], color=RED, lw=2.4, zorder=4)
ax.plot(*P, "o", color=ORANGE, ms=9, zorder=6)
ax.plot(*Q, "o", color=GREEN, ms=8, zorder=6)
ax.text(P[0] + 0.12, P[1] - 0.12, "$P(2,-1)$", fontsize=F - 1, color=ORANGE)
ax.text(Q[0] - 1.75, Q[1] - 0.05, "$Q(\\frac{1}{5},\\frac{7}{5})$", fontsize=F - 1, color=GREEN)
ax.text((P[0] + Q[0]) / 2 + 0.30, (P[1] + Q[1]) / 2 - 0.52, "$d=3$", fontsize=F + 0.5, color=RED)
w = np.array([A, B]) / np.hypot(A, B)
R = np.array([-0.6, (3 * -0.6 + 5) / 4])
ax.annotate("", xy=R + 1.2 * w, xytext=R, arrowprops=dict(arrowstyle="->", color=BROWN, lw=1.8))
ax.text(R[0] + 1.25 * w[0], R[1] + 1.25 * w[1], "$\\vec{n}=(3,-4)$", fontsize=F - 1, color=BROWN)
ax.text(-1.75, -2.35, "$d=\\dfrac{15}{5}=3$，$t=-\\dfrac{3}{5}$", fontsize=F - 0.5, color=INK)
fig.tight_layout(); fig.savefig(BASE + "ex-point-line2.png", dpi=150); plt.close(fig)


# ============ 3 例：圆拆成四段 ============
fig, axes = plt.subplots(2, 2, figsize=(9.6, 9.0), dpi=140)
O = np.array([1.0, -2.0]); r = 1.0
th_full = np.linspace(0, 2 * np.pi, 400)
cases = [("上半圆 $y=-2+\\sqrt{1-(x-1)^2}$", GREEN, np.linspace(0, np.pi, 300)),
         ("下半圆 $y=-2-\\sqrt{1-(x-1)^2}$", ORANGE, np.linspace(np.pi, 2 * np.pi, 300)),
         ("右半圆 $x=1+\\sqrt{1-(y+2)^2}$", BLUE, np.linspace(-np.pi / 2, np.pi / 2, 300)),
         ("左半圆 $x=1-\\sqrt{1-(y+2)^2}$", BROWN, np.linspace(np.pi / 2, 3 * np.pi / 2, 300))]
for ax, (title, col, tt) in zip(axes.flat, cases):
    frame(ax, (-0.4, 2.4), (-3.4, -0.6), title)
    ax.plot(O[0] + r * np.cos(th_full), O[1] + r * np.sin(th_full),
            color="#cccccc", lw=1.6, ls="--", zorder=2)
    ax.plot(O[0] + r * np.cos(tt), O[1] + r * np.sin(tt), color=col, lw=3.0, zorder=4)
    ax.plot(*O, "o", color=RED, ms=6, zorder=6)
    ax.text(O[0] + 0.10, O[1] - 0.28, "$(1,-2)$", fontsize=9.5, color=RED)
fig.tight_layout(); fig.savefig(BASE + "ex-circle-halves.png", dpi=140); plt.close(fig)


# ============ 4 例：双曲线 9x²-16y²=144 ============
fig, ax = plt.subplots(figsize=(6.6, 5.4), dpi=150)
frame(ax, (-7.2, 7.2), (-5.2, 5.2), "例：$9x^{2}-16y^{2}=144$，即 $\\dfrac{x^{2}}{16}-\\dfrac{y^{2}}{9}=1$")
a, b, c = 4.0, 3.0, 5.0
s = np.linspace(-1.75, 1.75, 500)
xr, yr = a * np.cosh(s), b * np.sinh(s)
for sx in (1, -1):
    ax.plot(sx * xr, yr, color=BLUE, lw=2.4, zorder=3)
    ax.plot(sx * xr, -yr, color=BLUE, lw=2.4, zorder=3)
xx = np.linspace(-6.8, 6.8, 10)
ax.plot(xx, 0.75 * xx, color=GREY, lw=1.3, ls="--", zorder=2)
ax.plot(xx, -0.75 * xx, color=GREY, lw=1.3, ls="--", zorder=2)
ax.text(5.15, 4.60, "$y=\\frac{3}{4}x$", fontsize=F - 1.5, color=GREY)
for sgn in (-1, 1):
    ax.plot([sgn * 16 / 5] * 2, [-3.4, 3.4], color="#c9b295", lw=1.1, ls=":", zorder=2)
ax.text(3.2, 4.60, "$x=\\frac{16}{5}$", fontsize=F - 2, color="#a9814f", ha="right")
ax.plot([c, c], [-b * b / a, b * b / a], color=ORANGE, lw=2.6, zorder=4)
ax.text(c + 0.18, -b * b / a - 0.60, "通径 $\\frac{2b^2}{a}=4.5$", fontsize=F - 1.5, color=ORANGE)
for x0, lab, col, dx0, dy0, ha in [(-a, "$A_1(-4,0)$", GREEN, -0.15, 0.30, "right"),
                                   (a, "$A_2(4,0)$", GREEN, 0.15, -0.52, "left"),
                                   (-c, "$F_1(-5,0)$", RED, 0.0, -0.72, "center"),
                                   (c, "$F_2(5,0)$", RED, 0.0, 0.72, "center")]:
    ax.plot([x0], [0], "o", color=col, ms=8, zorder=6)
    ax.text(x0 + dx0, dy0, lab, fontsize=F - 2, color=col, ha=ha)
ax.plot([a, c], [0, b], color=BROWN, lw=1.6, zorder=4)
ax.plot([a, a], [0, b], color=BROWN, lw=1.4, ls="--", zorder=4)
ax.text(a - 0.16, b / 2, "$b=3$", fontsize=F - 1.5, color=BROWN, ha="right")
ax.text((a + c) / 2, 0.16, "$c=5$", fontsize=F - 2, color=BROWN, ha="center")
ax.text(-7.0, -4.85, "$e=\\frac{c}{a}=1.25$", fontsize=F - 0.5, color=INK)
fig.tight_layout(); fig.savefig(BASE + "ex-hyperbola.png", dpi=150); plt.close(fig)


# ============ 5 例：抛物线 y²=4x 的通径 ============
fig, ax = plt.subplots(figsize=(6.4, 5.0), dpi=150)
frame(ax, (-1.8, 5.2), (-3.0, 3.0), "例：$y^{2}=4x$ 的通径")
yy = np.linspace(-2.7, 2.7, 400)
ax.plot(yy * yy / 4, yy, color=BLUE, lw=2.4, zorder=3)
ax.axvline(-1, color=GREY, lw=1.3, ls="--", zorder=2)
ax.text(-1.05, 2.55, "$x=-1$", fontsize=F - 1.5, color=GREY, ha="right")
ax.plot([1, 1], [-2, 2], color=ORANGE, lw=3.0, zorder=4)
ax.plot([1, 1], [-2, 2], "o", color=ORANGE, ms=8, zorder=5)
ax.plot([1], [0], "o", color=RED, ms=9, zorder=6)
ax.text(1.12, 0.20, "$F(1,0)$", fontsize=F - 1, color=RED)
ax.text(1.12, 1.95, "$A(1,2)$", fontsize=F - 1, color=ORANGE)
ax.text(1.12, -2.35, "$B(1,-2)$", fontsize=F - 1, color=ORANGE)
ax.text(2.15, 0.55, "$|AB|=4=2p$", fontsize=F - 0.5, color=ORANGE)
ax.text(-1.75, -2.75, "$p=2$，通径长 $2p=4$", fontsize=F - 1, color=INK)
fig.tight_layout(); fig.savefig(BASE + "ex-parabola.png", dpi=150); plt.close(fig)


# ============ 6 真题1：过 (4,0) 的椭圆切线 ============
fig, ax = plt.subplots(figsize=(6.4, 5.0), dpi=150)
frame(ax, (-2.6, 4.6), (-2.6, 2.6), "真题：过 $(4,0)$ 与 $\\dfrac{x^2}{4}+\\dfrac{y^2}{3}=1$ 相切")
a, b = 2.0, np.sqrt(3)
th = np.linspace(0, 2 * np.pi, 400)
ax.plot(a * np.cos(th), b * np.sin(th), color=BLUE, lw=2.4, zorder=3)
xs = np.linspace(-1.2, 4.4, 10)
for k in (0.5, -0.5):
    ax.plot(xs, k * (xs - 4), color=RED, lw=2.0, zorder=4)
    tx, ty = 1.0, 1.5 * (1 if k > 0 else -1)
    ax.plot([tx], [ty], "o", color=GREEN, ms=8, zorder=6)
ax.plot([4], [0], "o", color=ORANGE, ms=9, zorder=6)
ax.text(4.06, 0.34, "$(4,0)$", fontsize=F - 1, color=ORANGE)
ax.text(1.10, 1.62, "$(1,\\frac{3}{2})$", fontsize=F - 1.5, color=GREEN)
ax.text(1.10, -1.98, "$(1,-\\frac{3}{2})$", fontsize=F - 1.5, color=GREEN)
ax.text(-2.55, 2.32, "$k=\\pm\\frac{1}{2}$，切点横坐标都是 $x_0=1$", fontsize=F - 1.5, color=INK)
fig.tight_layout(); fig.savefig(BASE + "ex-2009-tangent.png", dpi=150); plt.close(fig)


# ============ 7 真题2：贮油罐截面 ============
fig, ax = plt.subplots(figsize=(7.2, 4.8), dpi=150)
a, b = 2.2, 1.3
xs = np.linspace(-a, a, 400)
yf = b / 2
lower = -b * np.sqrt(1 - (xs / a) ** 2)
upper = b * np.sqrt(1 - (xs / a) ** 2)
top = np.minimum(yf, upper)
ax.add_patch(mpatches.Ellipse((0, 0), 2 * a, 2 * b, facecolor="white", edgecolor="none", zorder=1))
ax.add_patch(mpatches.Polygon(np.vstack([np.column_stack([xs, lower]),
                                         np.column_stack([xs[::-1], top[::-1]])]),
                              facecolor="#7EA6C9", alpha=0.75, edgecolor="none", zorder=3))
ax.add_patch(mpatches.Ellipse((0, 0), 2 * a, 2 * b, facecolor="none", edgecolor=BLUE, lw=2.4, zorder=5))
ax.plot([-a - 0.45, a + 0.45], [yf, yf], color=RED, lw=2.0, zorder=6)
ax.text(a + 0.55, yf + 0.02, "油面", fontsize=F - 1, color=RED)
ax.annotate("", xy=(-a - 0.20, yf), xytext=(-a - 0.20, -b),
            arrowprops=dict(arrowstyle="<->", color=INK, lw=1.2))
ax.text(-a - 0.32, (yf - b) / 2, "$\\frac{3}{2}b$", fontsize=F - 1, color=INK, ha="right", va="center")
ax.annotate("", xy=(a + 0.20, -b), xytext=(a + 0.20, b),
            arrowprops=dict(arrowstyle="<->", color=GREY, lw=1.0))
ax.text(a + 0.32, 0.05, "$2b$", fontsize=F - 1.5, color=GREY, va="center")
ax.annotate("", xy=(-a, -b - 0.35), xytext=(a, -b - 0.35),
            arrowprops=dict(arrowstyle="<->", color=GREY, lw=1.0))
ax.text(0, -b - 0.62, "$2a$", fontsize=F - 1.5, color=GREY, ha="center")
ax.text(-3.05, 1.62, "$A=ab\\left(\\frac{2\\pi}{3}+\\frac{\\sqrt{3}}{4}\\right)$",
        fontsize=F - 0.5, color=INK)
ax.set_xlim(-3.3, 3.4); ax.set_ylim(-2.4, 1.9)
ax.set_aspect("equal"); ax.axis("off")
ax.set_title("真题：平放椭圆柱贮油罐的截面，阴影是液面以下的湿面积", fontsize=T - 0.5, color=INK, pad=4)
fig.tight_layout(); fig.savefig(BASE + "ex-2010-tank.png", dpi=150); plt.close(fig)


# ============ 8 真题3：y=x、x²+y²=2y、y 轴围成的区域 ============
fig, ax = plt.subplots(figsize=(6.0, 5.4), dpi=150)
frame(ax, (-0.6, 1.7), (-0.6, 2.5), "真题：$D$ 由 $y=x$、$x^2+y^2=2y$、$y$ 轴围成")
th = np.linspace(0, 2 * np.pi, 500)
ax.plot(np.cos(th), 1 + np.sin(th), color=BLUE, lw=2.4, zorder=4)
ax.plot([-0.4, 1.5], [-0.4, 1.5], color=RED, lw=2.0, zorder=3)
xs = np.linspace(0, 1, 400)
ax.fill_between(xs, xs, 1 + np.sqrt(1 - xs ** 2), color="#7EA6C9", alpha=0.5, zorder=2)
ax.plot([0, 0], [0, 2], color=BROWN, lw=2.0, zorder=3)
for pt, lab, off, col in [((0, 0), "$(0,0)$", (0.06, -0.22), INK),
                          ((1, 1), "$(1,1)$", (0.10, -0.05), INK),
                          ((0, 2), "$(0,2)$", (0.10, 0.06), INK)]:
    ax.plot(*pt, "o", color=GREEN, ms=7, zorder=6)
    ax.text(pt[0] + off[0], pt[1] + off[1], lab, fontsize=F - 1, color=col)
ax.text(0.15, 1.35, "$D$", fontsize=F + 2, color=BLUE)
ax.text(-0.55, 2.25, "圆 $x^2+(y-1)^2=1$，圆心 $(0,1)$、半径 $1$", fontsize=F - 1.5, color=INK)
ax.text(-0.55, -0.45, "结果 $\\iint_D xy\\,\\mathrm{d}\\sigma=\\frac{7}{12}$", fontsize=F - 1, color=RED)
fig.tight_layout(); fig.savefig(BASE + "ex-2011-region.png", dpi=150); plt.close(fig)

print("example figs done")
