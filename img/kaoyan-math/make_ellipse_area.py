import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle

plt.rcParams["font.family"] = ["PingFang SC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

INK, ORANGE, BLUE = "#2b2b2b", "#d2691e", "#2f4f6f"
CREAM, RED, GREEN, GREY = "#f3e3ce", "#b03a2e", "#4a7c59", "#8a8a8a"
BASE = "/Users/fred/Documents/GitHub/cycleuser/blog/output/img/kaoyan-math/"
F, T = 11.5, 12.5

a, b = 2.0, 1.15
th = np.linspace(0, 2 * np.pi, 400)
xs = np.linspace(-a, a, 13)

fig, axes = plt.subplots(1, 2, figsize=(11.6, 4.6), dpi=150)
for ax, mode in zip(axes, ["circle", "ellipse"]):
    ax.axhline(0, color="#dcdcdc", lw=0.9)
    ax.axvline(0, color="#dcdcdc", lw=0.9)
    ax.set_xlim(-a - 0.45, a + 0.45); ax.set_ylim(-a - 0.30, a + 0.30)
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_color("#bbbbbb")
    ax.set_xlabel("$x$", fontsize=10, color=INK)
    ax.set_ylabel("$y$", fontsize=10, color=INK)

# 左：圆
ax = axes[0]
ax.plot(a * np.cos(th), a * np.sin(th), color=BLUE, lw=2.4, zorder=4)
for i, x0 in enumerate(xs[:-1]):
    x1 = xs[i + 1]
    hh = np.sqrt(max(a * a - x0 * x0, 0))
    if i % 2 == 0:
        ax.add_patch(Rectangle((x0, -hh), x1 - x0, 2 * hh, facecolor=ORANGE,
                               alpha=0.22, edgecolor="none", zorder=2))
ax.plot([xs[3], xs[3]], [-np.sqrt(a*a-xs[3]**2), np.sqrt(a*a-xs[3]**2)],
        color=RED, lw=1.6, zorder=5)

ax.set_title("圆 $x^2+y^2=a^2$：面积 $\\pi a^2$", fontsize=T, color=BLUE)

# 右：椭圆
ax = axes[1]
ax.plot(a * np.cos(th), b * np.sin(th), color=BLUE, lw=2.4, zorder=4)
for i, x0 in enumerate(xs[:-1]):
    x1 = xs[i + 1]
    hh = b * np.sqrt(max(1 - (x0 / a) ** 2, 0))
    if i % 2 == 0:
        ax.add_patch(Rectangle((x0, -hh), x1 - x0, 2 * hh, facecolor=GREEN,
                               alpha=0.22, edgecolor="none", zorder=2))
hh3 = b * np.sqrt(1 - (xs[3] / a) ** 2)
ax.plot([xs[3], xs[3]], [-hh3, hh3], color=RED, lw=1.6, zorder=5)

ax.set_title("椭圆：竖条高度乘 $\\dfrac{b}{a}$，面积 $\\pi ab$", fontsize=T, color=GREEN)

fig.suptitle("同一条竖条：圆的高度按 $\\dfrac{b}{a}$ 缩小，面积也按这个比例缩小",
             fontsize=T + 0.5, color=INK)
fig.tight_layout(rect=(0, 0, 1, 0.92))
fig.savefig(BASE + "ellipse-area.png", dpi=150)
plt.close(fig)
print("ok")
