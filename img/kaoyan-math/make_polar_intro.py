import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

plt.rcParams["font.family"] = ["PingFang SC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

INK, ORANGE, BLUE = "#2b2b2b", "#d2691e", "#2f4f6f"
RED, GREEN, GREY = "#b03a2e", "#4a7c59", "#8a8a8a"
BASE = "/Users/fred/Documents/GitHub/cycleuser/blog/output/img/kaoyan-math/"
F = 11.5


def pad(ax, xlim, ylim, title):
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_color("#cccccc")
    ax.set_title(title, fontsize=12.5, color=INK, pad=6)


def draw_axes(ax, lim, grid=False, labels=False):
    if grid:
        th = np.linspace(0, 2 * np.pi, 400)
        for rr in np.arange(1, lim + 0.01, 1):
            ax.plot(rr * np.cos(th), rr * np.sin(th), color="#ebebeb", lw=1.0, zorder=0)
        for a in np.arange(0, 2 * np.pi, np.pi / 6):
            ax.plot([0, lim * np.cos(a)], [0, lim * np.sin(a)], color="#ebebeb", lw=1.0, zorder=0)
    ax.annotate("", xy=(lim + 0.35, 0), xytext=(-0.30, 0),
                arrowprops=dict(arrowstyle="->", color=INK, lw=1.6))
    ax.plot([0], [0], "o", color=INK, ms=7, zorder=6)
    ax.text(-0.20, -0.26, "$O$", fontsize=F + 1, color=INK, ha="right", va="top")
    ax.text(lim * 0.62, -0.28, "极轴", fontsize=F, color=INK, ha="center", va="top")


fig, axes = plt.subplots(2, 2, figsize=(11.8, 10.6), dpi=140)

# ---------- (1) 两个数 ----------
ax = axes[0][0]
pad(ax, (-1.0, 3.9), (-2.9, 3.2), "读法：先转 $\\theta$，再走 $r$")
draw_axes(ax, 3.4)
r0, t0 = 2.9, np.deg2rad(48)
P = np.array([r0 * np.cos(t0), r0 * np.sin(t0)])
ax.plot([0, P[0]], [0, P[1]], color=BLUE, lw=2.6, zorder=4)
ax.plot(*P, "o", color=RED, ms=9, zorder=6)
ax.text(P[0] + 0.12, P[1] + 0.10, "$P(r,\\theta)$", fontsize=F + 0.5, color=RED)
ax.add_patch(mpatches.Arc((0, 0), 1.35, 1.35, theta1=0, theta2=48, color=ORANGE, lw=2.2))
ax.text(0.86, 0.34, "$\\theta$", fontsize=F + 2.5, color=ORANGE)
mid = np.array([P[0] / 2, P[1] / 2])
ax.text(mid[0] - 0.42, mid[1] + 0.26, "$r$", fontsize=F + 2.5, color=BLUE)
ax.text(-0.95, -1.55, "$\\theta$ 从极轴逆时针转", fontsize=F - 0.5, color=ORANGE)
ax.text(-0.95, -2.05, "$r$ 是这一段长度", fontsize=F - 0.5, color=BLUE)
ax.text(-0.95, -2.60, "极点 $O$、极轴、$r$、$\\theta$ 合起来就是一个极坐标系",
        fontsize=F - 2, color=GREY)

# ---------- (2) 网格 ----------
ax = axes[0][1]
pad(ax, (-3.9, 3.9), (-3.9, 3.5), "网格：一圈圈同心圆 + 一条条射线")
draw_axes(ax, 3.4, grid=True)
for rr in (1, 2, 3):
    ax.text(rr * np.cos(np.deg2rad(112)), rr * np.sin(np.deg2rad(112)), "$r=%d$" % rr,
            fontsize=F - 1.5, color=GREY, ha="center", va="center")
for deg in (30, 60):
    a = np.deg2rad(deg)
    ax.text(3.55 * np.cos(a), 3.55 * np.sin(a), "$%d^\\circ$" % deg, fontsize=F - 2,
            color="#9a9a9a", ha="center", va="center")
ax.plot([2.6 * np.cos(np.deg2rad(60))], [2.6 * np.sin(np.deg2rad(60))], "o",
        color=RED, ms=8, zorder=6)
ax.text(2.6 * np.cos(np.deg2rad(60)) - 0.18, 2.6 * np.sin(np.deg2rad(60)) + 0.26,
        "$(r,\\theta)$", fontsize=F - 0.5, color=RED, ha="right")
ax.text(-3.85, -2.55, "同一个圆上：$r$ 不变、$\\theta$ 任意", fontsize=F - 1, color=BLUE)
ax.text(-3.85, -3.10, "同一条射线上：$\\theta$ 不变、$r$ 任意", fontsize=F - 1, color=ORANGE)

# ---------- (3) 多种写法 ----------
ax = axes[1][0]
pad(ax, (-2.6, 3.9), (-3.6, 3.2), "同一个点不止一种写法")
draw_axes(ax, 3.4)
r0, t0 = 2.7, np.deg2rad(36)
P = np.array([r0 * np.cos(t0), r0 * np.sin(t0)])
ax.plot([0, P[0]], [0, P[1]], color=BLUE, lw=2.4, zorder=4)
ax.plot(*P, "o", color=RED, ms=9, zorder=6)
ax.text(P[0] + 0.12, P[1] + 0.10, "$P$", fontsize=F + 1.5, color=RED)
ax.annotate("", xy=(r0 * np.cos(t0 + np.pi), r0 * np.sin(t0 + np.pi)), xytext=(0, 0),
            arrowprops=dict(arrowstyle="<-", color=GREEN, lw=1.8, ls="--"))
ax.text(r0 * np.cos(t0 + np.pi) + 0.15, r0 * np.sin(t0 + np.pi) + 0.22,
        "$-r$ 的方向", fontsize=F - 1.5, color=GREEN, ha="left")
ax.text(-2.55, -2.20, "$(r,\\ \\theta)$ 与 $(r,\\ \\theta+2k\\pi)$：同一点",
        fontsize=F - 1, color=BLUE)
ax.text(-2.55, -2.70, "$(r,\\ \\theta)$ 与 $(-r,\\ \\theta+(2k+1)\\pi)$：也同一点",
        fontsize=F - 1, color=GREEN)
ax.text(-2.55, -3.20, "$k$ 取整数：多转几整圈回到原处", fontsize=F - 2, color=GREY)

# ---------- (4) 为什么引入 ----------
ax = axes[1][1]
pad(ax, (-3.6, 4.0), (-3.3, 3.3), "为什么引入：绕中心转的图形更好写")
th = np.linspace(0, 2 * np.pi, 400)
a = 2.4
ax.plot(a * np.cos(th), a * np.sin(th), color=BLUE, lw=2.6, zorder=3)
ax.plot([0, 3.3 * np.cos(np.pi / 4)], [0, 3.3 * np.sin(np.pi / 4)], color=ORANGE, lw=2.4, zorder=3)
tt = np.linspace(0, 2.3 * np.pi, 900)
rr = 0.30 * tt
ax.plot(rr * np.cos(tt), rr * np.sin(tt), color=GREEN, lw=2.0, zorder=4)
ax.plot([0], [0], "o", color=INK, ms=6, zorder=6)
ax.text(-3.45, 2.25, "圆：$r=a$", fontsize=F - 0.5, color=BLUE)
ax.text(2.55, 1.35, "射线：$\\theta=\\frac{\\pi}{4}$", fontsize=F - 0.5, color=ORANGE)
ax.text(-3.45, -1.90, "螺线：$r=a\\theta$", fontsize=F - 0.5, color=GREEN)
ax.text(-3.45, -2.55, "同一个圆：$x^{2}+y^{2}=a^{2}$ 与 $r=a$", fontsize=F - 2, color=GREY)
ax.text(-3.45, -3.00, "射线本来要写 $y=x\\ (x\\geq0)$，极坐标只写 $\\theta=\\frac{\\pi}{4}$",
        fontsize=F - 2.5, color=GREY)

fig.suptitle("极坐标：用距离与方向定位一个点", fontsize=14.5, color=INK)
fig.tight_layout(rect=(0, 0, 1, 0.955))
fig.savefig(BASE + "polar-intro.png", dpi=140)
plt.close(fig)
print("ok")
