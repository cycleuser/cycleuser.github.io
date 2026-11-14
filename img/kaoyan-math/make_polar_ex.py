import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Ellipse, Polygon

plt.rcParams["font.family"] = ["PingFang SC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

INK, ORANGE, BLUE = "#2b2b2b", "#d2691e", "#2f4f6f"
RED, GREEN, GREY, BROWN = "#b03a2e", "#4a7c59", "#8a8a8a", "#7a5230"
BASE = "/Users/fred/Documents/GitHub/cycleuser/blog/output/img/kaoyan-math/"
F = 11.5


def frame(ax, xlim, ylim, title):
    ax.axhline(0, color="#dcdcdc", lw=0.9)
    ax.axvline(0, color="#dcdcdc", lw=0.9)
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_color("#cccccc")
    ax.set_title(title, fontsize=12, color=INK, pad=8)


# ========== (1) 心形线面积 ==========
fig, ax = plt.subplots(figsize=(7.0, 4.6), dpi=150)
th = np.linspace(0, 2 * np.pi, 900)
r = 1 + np.cos(th)
X, Y = r * np.cos(th), r * np.sin(th)
frame(ax, (-0.95, 3.05), (-1.62, 1.30), "心形线 $r=a(1+\\cos\\theta)$ 围成的面积")
ax.fill(X, Y, color=ORANGE, alpha=0.26, edgecolor="none", zorder=2)
ax.plot(X, Y, color=BLUE, lw=2.6, zorder=3)
ax.plot([0], [0], "o", color=INK, ms=7, zorder=6)
ax.plot([2], [0], "o", color=RED, ms=6, zorder=6)
ax.annotate("极点在曲线上：\n$\\theta=\\pi$ 时 $r=0$", xy=(0.02, 0.02), xytext=(-0.92, -1.45),
            fontsize=F - 2.5, color=INK, arrowprops=dict(arrowstyle="->", color=GREY, lw=1.0))
ax.annotate("$\\theta=0$ 时\n$r=2a$", xy=(1.98, 0.03), xytext=(2.18, 0.72),
            fontsize=F - 2.5, color=RED, arrowprops=dict(arrowstyle="->", color=RED, lw=1.0))
ax.text(0.5, 0.035, "$S=\\frac{1}{2}\\int_{0}^{2\\pi}a^{2}(1+\\cos\\theta)^{2}\\,\\mathrm{d}\\theta=\\frac{3\\pi a^{2}}{2}$",
        transform=ax.transAxes, fontsize=F - 2, color=INK, ha="center", va="bottom",
        bbox=dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#dddddd"))
fig.subplots_adjust(left=0.02, right=0.98, top=0.90, bottom=0.02)
fig.savefig(BASE + "ex-cardioid-area.png", dpi=150); plt.close(fig)


# ========== (2) 摆线一拱：弧长与旋转体 ==========
fig, axes = plt.subplots(1, 2, figsize=(12.0, 4.6), dpi=150)

ax = axes[0]
t = np.linspace(0, 2 * np.pi, 800)
x, y = t - np.sin(t), 1 - np.cos(t)
frame(ax, (-0.7, 6.9), (-1.1, 2.9), "一拱：$x=a(t-\\sin t),\\ y=a(1-\\cos t)$")
ax.plot(x, y, color=BLUE, lw=2.8, zorder=3)
ax.fill_between(x, 0, y, color=ORANGE, alpha=0.20, zorder=2)
ax.plot([0], [0], "o", color=RED, ms=6, zorder=5)
ax.plot([2 * np.pi], [0], "o", color=RED, ms=6, zorder=5)
ax.plot([np.pi], [2], "o", color=GREEN, ms=6, zorder=5)
ax.annotate("", xy=(2 * np.pi, -0.35), xytext=(0, -0.35),
            arrowprops=dict(arrowstyle="<->", color=GREY, lw=1.0))
ax.text(np.pi, -0.85, "底边 $2\\pi a$", fontsize=F - 2, color=GREY, ha="center")
ax.annotate("", xy=(np.pi + 0.30, 2.0), xytext=(np.pi + 0.30, 0),
            arrowprops=dict(arrowstyle="<->", color=GREY, lw=1.0))
ax.text(np.pi + 0.40, 1.00, "$2a$", fontsize=F - 2, color=GREY)
ax.text(0.25, 2.55, "弧长 $L=8a$", fontsize=F - 1.5, color=BLUE)

ax = axes[1]
frame(ax, (-0.7, 6.9), (-2.1, 2.1), "绕 $x$ 轴旋转：$V=5\\pi^{2}a^{3}$")
for xv, yv in zip(x[::22], y[::22]):
    if yv < 1e-3:
        continue
    ax.add_patch(Ellipse((xv, 0), 0.13, 2 * yv, facecolor="none", edgecolor=ORANGE, lw=0.8, alpha=0.45, zorder=2))
ax.plot(x, y, color=BLUE, lw=2.4, zorder=4)
ax.plot(x, -y, color=BLUE, lw=1.4, ls="--", zorder=3)
ax.plot([x[0], x[-1]], [0, 0], color=INK, lw=1.6, zorder=5)
ax.text(-0.60, 1.75, "截面是圆，半径 $y(t)$", fontsize=F - 2, color=ORANGE)
ax.text(-0.60, -1.95, "$V=\\pi\\int_{0}^{2\\pi}y^{2}x'\\,\\mathrm{d}t=5\\pi^{2}a^{3}$", fontsize=F - 2.5, color=INK)

fig.subplots_adjust(left=0.01, right=0.99, top=0.88, bottom=0.02, wspace=0.04)
fig.savefig(BASE + "ex-cycloid-volume.png", dpi=150); plt.close(fig)


# ========== (3) 星形线：全长与面积 ==========
fig, ax = plt.subplots(figsize=(6.2, 5.4), dpi=150)
t = np.linspace(0, 2 * np.pi, 1200)
x, y = np.cos(t) ** 3, np.sin(t) ** 3
frame(ax, (-1.55, 1.75), (-1.45, 1.45), "星形线 $x=a\\cos^{3}t,\\ y=a\\sin^{3}t$")
ax.fill(x, y, color=ORANGE, alpha=0.25, edgecolor="none", zorder=2)
ax.plot(x, y, color=BLUE, lw=2.6, zorder=3)
tq = np.linspace(0, np.pi / 2, 400)
ax.plot(np.cos(tq) ** 3, np.sin(tq) ** 3, color=RED, lw=3.0, zorder=4)
for ang in (0, np.pi / 2):
    ax.plot([np.cos(ang) ** 3], [np.sin(ang) ** 3], "o", color=RED, ms=6, zorder=5)
ax.text(1.02, 0.08, "$(a,0)$", fontsize=F - 2, color=RED)
ax.text(-0.12, 1.12, "$(0,a)$", fontsize=F - 2, color=RED)
ax.annotate("第一象限这一段，代进弧长公式再乘 $4$", xy=(0.36, 0.36), xytext=(-1.50, 1.22),
            fontsize=F - 2.5, color=RED, arrowprops=dict(arrowstyle="->", color=RED, lw=1.0))
ax.text(-1.50, -1.35, "$L=4\\cdot\\frac{3a}{2}\\int_{0}^{\\frac{\\pi}{2}}\\sin 2t\\,\\mathrm{d}t=6a$，$S=\\frac{3\\pi a^{2}}{8}$",
        fontsize=F - 3, color=INK)
fig.tight_layout(); fig.savefig(BASE + "ex-astroid-len.png", dpi=150); plt.close(fig)
print("ok")
