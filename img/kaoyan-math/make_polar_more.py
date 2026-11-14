import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

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
    ax.set_title(title, fontsize=12, color=INK, pad=7)


# ============ 1 过极点的圆与直线 ============
PI = np.pi
fig, axes = plt.subplots(2, 2, figsize=(11.6, 8.6), dpi=150)

# 左上：极坐标平面里的圆
ax = axes[0][0]
ax.set_xlim(-1.4, 3.3); ax.set_ylim(-2.0, 2.0)
ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
for sp in ax.spines.values():
    sp.set_color("#cccccc")
ax.set_title("过极点的圆 $r=2a\\cos\\theta$\n极坐标平面里的图形", fontsize=11.5, color=INK, pad=6)
a = 1.6
tt = np.linspace(-np.pi / 2, np.pi / 2, 400)
ax.plot(2 * a * np.cos(tt) * np.cos(tt), 2 * a * np.cos(tt) * np.sin(tt), color=BLUE, lw=2.6, zorder=3)
ax.plot([0], [0], "o", color=INK, ms=7, zorder=6)
ax.plot([2 * a], [0], "o", color=RED, ms=7, zorder=6)
ax.text(-0.20, -0.26, "$O$", fontsize=F, color=INK, ha="right")
ax.text(2 * a + 0.12, 0.12, "$\\theta=0$ 时 $r=2a$", fontsize=F - 2, color=RED)
ax.text(-1.30, -1.85, "$\\theta$ 取 $\\left[-\\frac{\\pi}{2},\\frac{\\pi}{2}\\right]$ 描完一圈", fontsize=F - 2.5, color=GREY)

# 右上：极坐标平面里的直线
ax = axes[0][1]
ax.set_xlim(-1.6, 3.3); ax.set_ylim(-2.2, 2.2)
ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
for sp in ax.spines.values():
    sp.set_color("#cccccc")
ax.set_title("不过极点的直线 $r=\\sec\\theta$\n极坐标平面里的图形", fontsize=11.5, color=INK, pad=6)
tt = np.linspace(-1.15, 1.15, 300)
ax.plot(np.cos(tt) * 0 + 1.0, np.tan(tt), color=ORANGE, lw=2.6, zorder=3)
ax.plot([0], [0], "o", color=INK, ms=7, zorder=6)
ax.text(-0.20, -0.30, "$O$", fontsize=F, color=INK, ha="right")
ax.text(1.10, 1.80, "$x=1$", fontsize=F - 1, color=ORANGE)
ax.text(-1.55, -2.05, "直线不过极点，$r$ 随 $\\theta$ 变化", fontsize=F - 2.5, color=GREY)

# 左下：r 作为 theta 的函数
ax = axes[1][0]
ax.set_xlim(-2.0, 2.0); ax.set_ylim(-0.35, 3.6)
ax.grid(True, color="#ececec", lw=0.8)
ax.axhline(0, color="#c8c8c8", lw=1.0)
ax.axvline(0, color="#c8c8c8", lw=1.0)
ax.set_xticks([-PI / 2, 0, PI / 2])
ax.set_xticklabels([r"$-\frac{\pi}{2}$", "0", r"$\frac{\pi}{2}$"], fontsize=F - 2, color=INK)
ax.set_yticks([])
for sp in ax.spines.values():
    sp.set_color("#cccccc")
ax.set_title("同一函数：$r=2a\\cos\\theta$\n直角坐标里 $r$ 作为 $\\theta$ 的函数", fontsize=11.5, color=INK, pad=6)
ax.set_xlabel(r"$\theta$", fontsize=F - 1, color=INK, labelpad=1)
ax.set_ylabel(r"$r$", fontsize=F - 1, color=INK, labelpad=1)
tt = np.linspace(-np.pi / 2, np.pi / 2, 400)
ax.plot(tt, 2 * a * np.cos(tt), color=BLUE, lw=2.6, zorder=3)
ax.plot([0], [2 * a], "o", color=RED, ms=7, zorder=5)
ax.text(-1.95, 0.30, "一条余弦拱：$\\theta=0$ 处最高 $2a$，两端落到 $0$", fontsize=F - 2.5, color=INK)

# 右下：sec
ax = axes[1][1]
ax.set_xlim(-1.6, 1.6); ax.set_ylim(-0.6, 5.2)
ax.grid(True, color="#ececec", lw=0.8)
ax.axhline(0, color="#c8c8c8", lw=1.0)
ax.axvline(0, color="#c8c8c8", lw=1.0)
ax.set_xticks([-PI / 2, 0, PI / 2])
ax.set_xticklabels([r"$-\frac{\pi}{2}$", "0", r"$\frac{\pi}{2}$"], fontsize=F - 2, color=INK)
ax.set_yticks([])
for sp in ax.spines.values():
    sp.set_color("#cccccc")
ax.set_title("同一函数：$r=\\sec\\theta$\n直角坐标里 $r$ 作为 $\\theta$ 的函数", fontsize=11.5, color=INK, pad=6)
ax.set_xlabel(r"$\theta$", fontsize=F - 1, color=INK, labelpad=1)
ax.set_ylabel(r"$r$", fontsize=F - 1, color=INK, labelpad=1)
tt = np.linspace(-1.25, 1.25, 400)
rr = 1 / np.cos(tt)
ax.plot(tt, rr, color=ORANGE, lw=2.6, zorder=3)
ax.plot([0], [1], "o", color=RED, ms=7, zorder=5)
ax.text(-1.55, 4.55, "$\\theta=0$ 处 $r=1$ 最小，两端往上冲", fontsize=F - 2.5, color=INK)

fig.tight_layout(); fig.savefig(BASE + "pc-circle-line.png", dpi=150); plt.close(fig)


# ============ 2 面积微元与弧长微元 ============
rfun = lambda t: 1.30 + 0.30 * np.sin(2 * t)
th_all = np.linspace(0, 2 * np.pi, 600)
rr_all = rfun(th_all)

fig, axes = plt.subplots(1, 2, figsize=(12.6, 4.9), dpi=150)

for ax in axes:
    ax.set_xlim(-1.88, 1.88); ax.set_ylim(-1.45, 1.45)
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_color("#cccccc")
    if ax is axes[0]:
        ax.plot(rr_all * np.cos(th_all), rr_all * np.sin(th_all), color=BLUE, lw=2.2, zorder=3)
        ax.plot([0], [0], "o", color=INK, ms=6, zorder=6)

# 左：面积微元
ax = axes[0]
ax.set_title(r"面积微元：一小块扇形 $\frac{1}{2}r^{2}\Delta\theta$", fontsize=11.5, color=INK, pad=6)
t1, t2 = np.deg2rad(55), np.deg2rad(100)
tt = np.linspace(t1, t2, 40)
r_loc = rfun(tt)
ax.fill(np.concatenate([[0], r_loc * np.cos(tt), [0]]),
        np.concatenate([[0], r_loc * np.sin(tt), [0]]),
        color=ORANGE, alpha=0.45, edgecolor=ORANGE, lw=1.0, zorder=4)
ax.text(0.02, 0.94, r"扇形半径 $r(\theta)$，" + "\n" + r"圆心角 $\Delta\theta$",
        transform=ax.transAxes, fontsize=F - 2, color=INK, va="top")
ax.text(0.02, 0.80, r"$\Delta S\approx\frac{1}{2}r^{2}\Delta\theta$" + "\n" + r"$S=\frac{1}{2}\int_{\alpha}^{\beta}r^{2}\,\mathrm{d}\theta$",
        transform=ax.transAxes, fontsize=F - 2, color=GREY, va="top")

# 右：弧长微元
ax = axes[1]
ax.set_title(r"弧长微元：$\mathrm{d}s$ 拆成径向与横向", fontsize=11.5, color=INK, pad=6)
P1 = np.array([0.0, 0.0])
P2 = np.array([0.90, 0.70])
P1r = np.array([0.0, 0.70])
tt = np.linspace(0, 1, 80)
Ctrl = np.array([0.45, 0.0])
curve = ((1 - tt) ** 2)[:, None] * P1 + (2 * tt * (1 - tt))[:, None] * Ctrl + (tt ** 2)[:, None] * P2
ax.plot(curve[:, 0], curve[:, 1], color=BLUE, lw=2.8, zorder=3)
ax.plot([P1[0], P1[0]], [P1[1] - 0.42, P1[1]], color=GREY, lw=1.0, ls="--", zorder=2)
ax.plot([P1[0], P1r[0]], [P1[1], P1r[1]], color=GREEN, lw=3.2, zorder=5)
ax.plot([P1r[0], P2[0]], [P1r[1], P2[1]], color=ORANGE, lw=3.2, zorder=5)
ax.plot([P1[0], P2[0]], [P1[1], P2[1]], color=RED, lw=2.4, ls=(0, (5, 3)), zorder=6)
ax.plot([P1r[0] + 0.11, P1r[0] + 0.11, P1r[0]], [P1r[1], P1r[1] - 0.11, P1r[1] - 0.11],
        color=INK, lw=0.9, zorder=6)
ax.text(P1[0] - 0.26, P1[1] + 0.34, r"$\mathrm{d}r$", fontsize=F + 3, color=GREEN, ha="center")
ax.text(P1r[0] + 0.32, P1r[1] + 0.16, r"$r\,\mathrm{d}\theta$", fontsize=F + 3, color=ORANGE, ha="center")
ax.text(P1[0] + 0.36, P1[1] + 0.16, r"$\mathrm{d}s$", fontsize=F + 3, color=RED, ha="center")
ax.text(P1[0] - 0.14, P1[1] - 0.34, "指向极点 $O$", fontsize=F - 2, color=GREY, ha="center")
ax.text(P1[0] + 0.30, P1[1] + 0.44, "曲线", fontsize=F - 2, color=BLUE, ha="center")
ax.plot([P1[0]], [P1[1]], "o", color=INK, ms=5, zorder=7)
ax.set_xlim(-0.52, 1.55)
ax.set_ylim(-0.46, 1.18)
ax.text(0.02, 0.94, r"$\mathrm{d}s$ 是直角三角形的斜边，" + "\n" + r"两直角边是 $\mathrm{d}r$ 与 $r\,\mathrm{d}\theta$",
        transform=ax.transAxes, fontsize=F - 2, color=INK, va="top")
ax.text(0.02, 0.74, r"$\mathrm{d}s=\sqrt{\left(\mathrm{d}r\right)^{2}+\left(r\,\mathrm{d}\theta\right)^{2}}$",
        transform=ax.transAxes, fontsize=F - 2, color=GREY, va="top")
ax.set_title(r"弧长微元：$\mathrm{d}s$ 拆成径向与横向", fontsize=11.5, color=INK, pad=6)

fig.subplots_adjust(left=0.01, right=0.99, top=0.88, bottom=0.02, wspace=0.06)
fig.savefig(BASE + "pc-area-element.png", dpi=150); plt.close(fig)

print("ok")
