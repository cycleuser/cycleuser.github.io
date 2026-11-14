import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.family"] = ["PingFang SC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
INK, ORANGE, BLUE, RED, GREEN, GREY = "#2b2b2b", "#d2691e", "#2f4f6f", "#b03a2e", "#4a7c59", "#8a8a8a"
BASE = "/Users/fred/Documents/GitHub/cycleuser/blog/output/img/kaoyan-math/"
F = 11.5

fig, ax = plt.subplots(figsize=(6.8, 6.6), dpi=150)
ax.set_xlim(-4.2, 4.2); ax.set_ylim(-4.2, 4.2)
ax.set_aspect("equal")
ax.grid(True, color="#eeeeee", lw=0.8)
ax.axhline(0, color="#c8c8c8", lw=1.2, zorder=2)
ax.axvline(0, color="#c8c8c8", lw=1.2, zorder=2)
ax.set_xticks([]); ax.set_yticks([])
for sp in ax.spines.values():
    sp.set_color("#cccccc")

x = np.linspace(0.22, 4.1, 400)
ax.plot(x, 1 / x, color=BLUE, lw=2.8, zorder=4)
ax.plot(-x, -1 / x, color=BLUE, lw=2.8, zorder=4)

# 旋转 45 度后的两条轴 u, v
s = np.linspace(-4.0, 4.0, 10)
ax.plot(s, s, color=GREEN, lw=1.2, ls="--", zorder=3)
ax.plot(s, -s, color=GREEN, lw=1.2, ls="--", zorder=3)
ax.plot([1, -1], [1, -1], "o", color=RED, ms=8, zorder=6)
ax.text(1.10, 1.06, "$(1,1)$", fontsize=F - 1, color=RED)
ax.text(-1.95, -1.14, "$(-1,-1)$", fontsize=F - 1, color=RED)
ax.text(3.35, 3.30, "$u$ 轴", fontsize=F - 2, color=GREEN)
ax.text(-4.05, 3.30, "$v$ 轴", fontsize=F - 2, color=GREEN)
ax.text(1.95, 2.62, "两条坐标轴都是渐近线", fontsize=F - 2.5, color=GREY)
ax.text(-4.05, -3.95, "$xy=1$：等轴双曲线，渐近线是两条坐标轴", fontsize=F - 2.5, color=INK)
ax.set_title("$xy=1$ 与旋转 $45^{\\circ}$ 后的 $u^{2}-v^{2}=2$", fontsize=13, color=INK, pad=10)
fig.tight_layout()
fig.savefig(BASE + "ex-xy1-hyperbola.png", dpi=150)
print("ok")
