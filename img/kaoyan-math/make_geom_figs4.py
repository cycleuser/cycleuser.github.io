import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.family"] = ["PingFang SC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

INK    = "#2b2b2b"
ORANGE = "#d2691e"
BLUE   = "#2f4f6f"
CREAM  = "#f3e3ce"
RED    = "#b03a2e"
GREEN  = "#4a7c59"
GREY   = "#8a8a8a"
BROWN  = "#7a5230"

BASE = "/Users/fred/Documents/GitHub/cycleuser/blog/output/img/kaoyan-math/"


def style(ax):
    ax.spines[["top", "right"]].set_visible(False)
    for s in ax.spines.values():
        s.set_color(GREY)
    ax.tick_params(colors="#555")


A, B, C = 3.0, 4.0, -12.0
n = np.array([A, B]) / np.hypot(A, B)


def line(ax):
    xs = np.linspace(0.2, 7.4, 10)
    ax.plot(xs, (A * xs + C) / (-B), color=BLUE, lw=2.4)


fig, axes = plt.subplots(1, 2, figsize=(12.6, 5.2), dpi=150)

# 左：法向量
ax = axes[0]
line(ax)
M = np.array([2.0, (A * 2.0 + C) / (-B)])
ax.annotate("", xy=M + 1.9 * n, xytext=M,
            arrowprops=dict(arrowstyle="->", color=BROWN, lw=2.2))
ax.text(M[0] + 1.95 * n[0], M[1] + 1.95 * n[1], r"$\vec{n}=(A,B)$", fontsize=11.5, color=BROWN)
ax.plot(*M, "o", color=ORANGE, ms=7, zorder=6)
ax.text(M[0] - 0.55, M[1] - 0.30, "$M$", fontsize=10.5, color=ORANGE)
# 直角标记
w = n
u = np.array([-B, A]) / np.hypot(A, B)
s0 = 0.30
p1 = M + s0 * w
p2 = p1 + s0 * u
p3 = M + s0 * u
ax.plot([p1[0], p2[0], p3[0]], [p1[1], p2[1], p3[1]], color=RED, lw=1.1)
ax.text(0.35, 4.60, r"$Ax+By+C=0$", fontsize=11.5, color=BLUE)
ax.text(0.35, 3.95, r"法向量 $\vec{n}=(A,B)$", fontsize=11.5, color=BROWN)
ax.text(0.35, -0.55, r"直线斜率 $k=-A/B$", fontsize=11, color=INK)
ax.text(0.35, -1.15, r"法向量斜率 $B/A$，两者乘积为 $-1$", fontsize=11, color=INK)
ax.set_title("直线的法向量", fontsize=12, color=INK)
ax.set_aspect("equal"); ax.axhline(0, color=GREY, lw=0.9)
ax.set_xlim(0.0, 7.6); ax.set_ylim(-2.4, 5.2)
ax.set_xlabel("$x$", fontsize=10, color=INK); ax.set_ylabel("$y$", fontsize=10, color=INK)
style(ax)

# 右：过一点作法线
ax = axes[1]
line(ax)
P = np.array([6.0, 4.0])
t = -(A * P[0] + B * P[1] + C) / (A * A + B * B)
Q = P + t * np.array([A, B])
ax.plot([P[0], Q[0]], [P[1], Q[1]], color=RED, lw=2.4)
tt = np.linspace(-1.6, 1.0, 10)
ax.plot(P[0] + tt * A, P[1] + tt * B, color=RED, lw=1.2, ls="--", alpha=0.8)
ax.plot(*P, "o", color=ORANGE, ms=9, zorder=6)
ax.plot(*Q, "o", color=GREEN, ms=8, zorder=6)
ax.text(P[0] - 1.05, P[1] + 0.16, "$P(6,4)$", fontsize=11, color=ORANGE)
ax.text(Q[0] - 1.95, Q[1] - 0.85, "$Q(3.36,0.48)$", fontsize=10, color=GREEN)
ax.text(2.35, 4.55, "法线：$4x-3y-12=0$", fontsize=11.5, color=RED)
ax.text(2.35, 3.90, r"方向取 $(A,B)=(3,4)$", fontsize=10.5, color=INK)
ax.text(0.30, -1.35, r"$3x+4y-12=0$", fontsize=11, color=BLUE)
ax.set_title("过一点作已知直线的法线", fontsize=12, color=INK)
ax.set_aspect("equal"); ax.axhline(0, color=GREY, lw=0.9)
ax.set_xlim(0.0, 7.8); ax.set_ylim(-2.4, 5.2)
ax.set_xlabel("$x$", fontsize=10, color=INK); ax.set_ylabel("$y$", fontsize=10, color=INK)
style(ax)

fig.tight_layout()
fig.savefig(BASE + "geo4-line-normal.png", dpi=150)
plt.close(fig)
print("ok")
