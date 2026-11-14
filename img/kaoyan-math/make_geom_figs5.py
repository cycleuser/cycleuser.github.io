import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
from matplotlib.patches import Circle, Polygon, Rectangle

plt.rcParams["font.family"] = ["PingFang SC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

INK, ORANGE, BLUE = "#2b2b2b", "#d2691e", "#2f4f6f"
CREAM, RED, GREEN, GREY, BROWN = "#f3e3ce", "#b03a2e", "#4a7c59", "#8a8a8a", "#7a5230"
BASE = "/Users/fred/Documents/GitHub/cycleuser/blog/output/img/kaoyan-math/"

fig, axes = plt.subplots(2, 4, figsize=(15.2, 7.8), dpi=140)


def panel(ax, title, lim=1.55):
    ax.add_patch(Rectangle((-lim - 0.35, -lim - 0.35), 2 * lim + 0.7, 2 * lim + 0.7,
                           facecolor="#fcf9f5", edgecolor="#eeeeee", lw=1.0, zorder=0))
    ax.axhline(0, color="#dcdcdc", lw=0.8, zorder=1)
    ax.axvline(0, color="#dcdcdc", lw=0.8, zorder=1)
    ax.set_xlim(-lim - 0.35, lim + 0.35)
    ax.set_ylim(-lim - 0.35, lim + 0.35)
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)
    ax.set_title(title, fontsize=10.5, color=INK, pad=5)


th = np.linspace(0, 2 * np.pi, 400)

# 1 标准式
ax = axes[0][0]
panel(ax, "标准式：圆心与半径")
O = np.array([0.15, -0.10]); r = 1.0
ax.add_patch(Circle(O, r, facecolor="none", edgecolor=BLUE, lw=2.2, zorder=3))
ax.plot(*O, "o", color=RED, ms=7, zorder=5)
P = O + r * np.array([np.cos(np.deg2rad(38)), np.sin(np.deg2rad(38))])
ax.plot([O[0], P[0]], [O[1], P[1]], color=ORANGE, lw=1.8, zorder=4)
ax.plot(*P, "o", color=GREEN, ms=6, zorder=5)
ax.text(O[0] - 0.40, O[1] - 0.20, "$(a,b)$", fontsize=9.5, color=RED)
ax.text((O[0] + P[0]) / 2 - 0.02, (O[1] + P[1]) / 2 + 0.10, "$r$", fontsize=11, color=ORANGE)
ax.text(-1.80, 1.62, r"$(x-a)^2+(y-b)^2=r^2$", fontsize=10.5, color=BLUE)

# 2 一般式与配方
ax = axes[0][1]
ax.add_patch(Rectangle((-0.75, -3.45), 3.6, 3.9, facecolor="#fcf9f5",
                       edgecolor="#eeeeee", lw=1.0, zorder=0))
ax.axhline(0, color="#dcdcdc", lw=0.8, zorder=1)
ax.axvline(0, color="#dcdcdc", lw=0.8, zorder=1)
O2 = np.array([1.0, -2.0]); r2 = 1.0
ax.add_patch(Circle(O2, r2, facecolor=CREAM, alpha=0.85, edgecolor=BLUE, lw=2.0, zorder=3))
ax.plot(*O2, "o", color=RED, ms=6, zorder=5)
ax.plot([O2[0], O2[0] + r2], [O2[1], O2[1]], color=ORANGE, lw=1.5, zorder=4)
ax.text(O2[0] + 0.42, O2[1] + 0.10, "$r=1$", fontsize=9, color=ORANGE)
ax.text(O2[0] - 0.75, O2[1] - 0.24, "$(1,-2)$", fontsize=9, color=RED)
ax.text(-0.68, 0.30, r"$x^2+y^2-2x+4y+4=0$", fontsize=9, color=INK)
ax.text(-0.68, -0.05, r"$\Downarrow$ 分别配方", fontsize=8.5, color=GREY)
ax.text(-0.68, -0.40, r"$(x-1)^2+(y+2)^2=1$", fontsize=9, color=BLUE)
ax.text(-0.68, -0.75, r"$D=-2,\ E=4,\ F=4$", fontsize=8.5, color=GREY)
ax.text(-0.68, -1.10, r"圆心 $(-\frac{D}{2},-\frac{E}{2})$", fontsize=8.5, color=INK)
ax.set_xlim(-0.75, 2.85); ax.set_ylim(-3.45, 0.45)
ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
for sp in ax.spines.values():
    sp.set_visible(False)
ax.set_title("一般式：配方读出圆心与半径", fontsize=10.5, color=INK, pad=5)

# 3 参数式
ax = axes[0][2]
panel(ax, "参数式：$t$ 是圆心角")
r3 = 1.0
ax.add_patch(Circle((0, 0), r3, facecolor="none", edgecolor=BLUE, lw=2.2, zorder=3))
t0 = np.deg2rad(52)
P = np.array([np.cos(t0), np.sin(t0)])
ax.plot([0, P[0]], [0, P[1]], color=GREY, lw=1.1, ls="--", zorder=4)
ax.plot([0, P[0]], [0, 0], color=GREEN, lw=1.5, zorder=4)
ax.plot([P[0], P[0]], [0, P[1]], color=ORANGE, lw=1.5, zorder=4)
ax.plot(*P, "o", color=RED, ms=6, zorder=5)
ax.add_patch(mpatches.Arc((0, 0), 0.6, 0.6, theta1=0, theta2=52, color=GREY, lw=1.1))
ax.text(0.34, 0.13, "$t$", fontsize=10, color=GREY)
ax.text(P[0] / 2 - 0.04, -0.22, r"$r\cos t$", fontsize=9, color=GREEN)
ax.text(P[0] + 0.06, P[1] / 2, r"$r\sin t$", fontsize=9, color=ORANGE)
ax.text(-1.80, 1.62, r"$x=a+r\cos t$", fontsize=10, color=INK)
ax.text(-1.80, 1.30, r"$y=b+r\sin t$", fontsize=10, color=INK)

# 4 点与圆
ax = axes[0][3]
panel(ax, "点与圆：比 $d$ 与 $r$")
ax.add_patch(Circle((0, 0), 1.0, facecolor="none", edgecolor=BLUE, lw=2.2, zorder=3))
for ang, rad, col, lab in [(0.9, 0.55, GREEN, "$d<r$"), (2.3, 1.0, ORANGE, "$d=r$"),
                            (0.2, 1.42, RED, "$d>r$")]:
    p = rad * np.array([np.cos(ang), np.sin(ang)])
    ax.plot([0, p[0]], [0, p[1]], color=col, lw=1.1, ls="--", zorder=4)
    ax.plot(*p, "o", color=col, ms=6, zorder=5)
ax.text(-0.15, -1.62, "$d<r$ 在圆内，$d=r$ 在圆上，$d>r$ 在圆外", fontsize=8.5, color=INK)

# 5 切线
ax = axes[1][0]
panel(ax, "切线：半径垂直于切线")
O = np.array([0.0, 0.0]); r = 1.0
ax.add_patch(Circle(O, r, facecolor="none", edgecolor=BLUE, lw=2.2, zorder=3))
ta = np.deg2rad(42)
T = r * np.array([np.cos(ta), np.sin(ta)])
d = np.array([-np.sin(ta), np.cos(ta)])
ax.plot([T[0] - 1.0 * d[0], T[0] + 1.0 * d[0]], [T[1] - 1.0 * d[1], T[1] + 1.0 * d[1]],
        color=RED, lw=1.9, zorder=4)
ax.plot([0, T[0]], [0, T[1]], color=ORANGE, lw=1.5, zorder=4)
ax.plot(*T, "o", color=GREEN, ms=6, zorder=5)
s0 = 0.22
p1 = T - s0 * np.array([np.cos(ta), np.sin(ta)])
p2 = p1 + s0 * d
p3 = T + s0 * d
ax.plot([p1[0], p2[0], p3[0]], [p1[1], p2[1], p3[1]], color=RED, lw=1.0, zorder=5)
ax.text(T[0] + 0.10, T[1] + 0.12, "$T$", fontsize=9.5, color=GREEN)
ax.text(-1.80, 1.62, r"$(x_0-a)(x-a)+(y_0-b)(y-b)=r^2$", fontsize=8.5, color=RED)

# 6 切线长
ax = axes[1][1]
panel(ax, "切线长：勾股定理")
O = np.array([-0.25, 0.0]); r = 0.85
ax.add_patch(Circle(O, r, facecolor="none", edgecolor=BLUE, lw=2.2, zorder=3))
P = np.array([1.25, 0.62])
dP = np.linalg.norm(P - O)
al = np.arccos(r / dP)
base = np.arctan2(P[1] - O[1], P[0] - O[0])
for sgn in (1, -1):
    T = O + r * np.array([np.cos(base + sgn * al), np.sin(base + sgn * al)])
    ax.plot([P[0], T[0]], [P[1], T[1]], color=RED, lw=1.6, zorder=4)
    ax.plot([O[0], T[0]], [O[1], T[1]], color=GREY, lw=1.1, ls="--", zorder=4)
    ax.plot(*T, "o", color=GREEN, ms=5, zorder=5)
ax.plot([O[0], P[0]], [O[1], P[1]], color=BROWN, lw=1.3, ls=":", zorder=4)
ax.plot(*P, "o", color=ORANGE, ms=7, zorder=5)
ax.text(P[0] + 0.06, P[1] + 0.10, "$P$", fontsize=9.5, color=ORANGE)
ax.text(-1.80, -1.62, r"$|PT|^2=|PO|^2-r^2$", fontsize=9.5, color=RED)

# 7 弦长
ax = axes[1][2]
panel(ax, "弦长：垂径定理")
O = np.array([0.0, 0.0]); r = 1.0
ax.add_patch(Circle(O, r, facecolor="none", edgecolor=BLUE, lw=2.2, zorder=3))
y0 = 0.42
dx = np.sqrt(r ** 2 - y0 ** 2)
ax.plot([-1.45, 1.45], [y0, y0], color=RED, lw=1.8, zorder=4)
ax.plot([-dx, dx], [y0, y0], color=ORANGE, lw=2.6, zorder=5)
ax.plot([0, 0], [0, y0], color=GREEN, lw=1.4, ls="--", zorder=4)
ax.plot([0, dx], [0, y0], color=GREY, lw=0.9, ls=":", zorder=6)
ax.plot([-dx, dx], [y0, y0], "o", color=ORANGE, ms=5, zorder=6)
ax.text(0.06, y0 / 2 - 0.10, "$d$", fontsize=9.5, color=GREEN)
ax.text(dx / 2 - 0.05, -0.16, r"$\sqrt{r^2-d^2}$", fontsize=9, color=GREY)
ax.text(-1.80, -1.62, r"$L=2\sqrt{r^2-d^2}$", fontsize=9.5, color=ORANGE)

# 8 直线与圆
ax = axes[1][3]
panel(ax, "直线与圆：三种位置")
ax.add_patch(Circle((0, 0), 1.0, facecolor="none", edgecolor=BLUE, lw=2.2, zorder=3))
for y0, col, lab in [(-0.45, RED, "相交"), (1.0, GREEN, "相切"), (1.42, ORANGE, "相离")]:
    ax.plot([-1.35, 1.35], [y0, y0], color=col, lw=1.6, zorder=4)
    ax.text(1.40, y0 - 0.06, lab, fontsize=8.5, color=col, ha="left")
ax.set_xlim(-1.9, 2.1)
ax.text(-1.85, -1.62, "$d<r$ 相交、$d=r$ 相切、$d>r$ 相离", fontsize=8.5, color=INK)

fig.suptitle("圆的六种写法与四个常用量", fontsize=13, color=INK)
fig.tight_layout(rect=(0, 0, 1, 0.95))
fig.savefig(BASE + "geo5-circle-forms.png", dpi=140)
plt.close(fig)
print("ok")
