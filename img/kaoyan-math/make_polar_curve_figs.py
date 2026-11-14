import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.family"] = ["PingFang SC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

INK, ORANGE, BLUE = "#2b2b2b", "#d2691e", "#2f4f6f"
RED, GREEN, GREY, BROWN = "#b03a2e", "#4a7c59", "#8a8a8a", "#7a5230"
BASE = "/Users/fred/Documents/GitHub/cycleuser/blog/output/img/kaoyan-math/"
F, T = 11.5, 12.5
PI = np.pi


def polar_axes(ax, lim, title):
    th = np.linspace(0, 2 * np.pi, 400)
    for rr in np.arange(0.5, lim + 0.01, 0.5):
        ax.plot(rr * np.cos(th), rr * np.sin(th), color="#ececec", lw=0.8, zorder=0)
    for a0 in np.arange(0, np.pi, np.pi / 6):
        ax.plot([0, lim * np.cos(a0)], [0, lim * np.sin(a0)], color="#ececec", lw=0.8, zorder=0)
        ax.plot([0, -lim * np.cos(a0)], [0, -lim * np.sin(a0)], color="#ececec", lw=0.8, zorder=0)
    ax.axhline(0, color="#c8c8c8", lw=1.0, zorder=1)
    ax.axvline(0, color="#c8c8c8", lw=1.0, zorder=1)
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_color("#cccccc")
    ax.set_title(title + "\n极坐标平面里的图形", fontsize=T, color=INK, pad=6)


def rtheta_axes(ax, trange, rrange, title, ticks=None):
    """直角坐标里把 r 当作 theta 的函数画：横轴 theta，纵轴 r。"""
    ax.set_xlim(*trange); ax.set_ylim(*rrange)
    ax.grid(True, color="#ececec", lw=0.8)
    ax.axhline(0, color="#c8c8c8", lw=1.0, zorder=2)
    ax.axvline(0, color="#c8c8c8", lw=1.0, zorder=2)
    if ticks is None:
        ticks = [(0, "0"), (PI / 2, r"$\frac{\pi}{2}$"), (PI, r"$\pi$"),
                 (3 * PI / 2, r"$\frac{3\pi}{2}$"), (2 * PI, r"$2\pi$")]
    ax.set_xticks([t for t, _ in ticks])
    ax.set_xticklabels([l for _, l in ticks], fontsize=F - 2, color=INK)
    ax.set_yticks([])
    ax.tick_params(axis="x", colors="#bbbbbb", length=3)
    for sp in ax.spines.values():
        sp.set_color("#cccccc")
    ax.set_title(title + "\n直角坐标：$r$ 作为 $\\theta$ 的函数", fontsize=T, color=INK, pad=6)
    ax.set_xlabel(r"$\theta$", fontsize=F - 1, color=INK, labelpad=1)
    ax.set_ylabel(r"$r$", fontsize=F - 1, color=INK, labelpad=1)


# ============ 1 心形线 ============
a = 1.0
th = np.linspace(0, 2 * np.pi, 2000)
r = a * (1 + np.cos(th))
fig, axes = plt.subplots(1, 2, figsize=(12.0, 5.0), dpi=150)

ax = axes[0]
polar_axes(ax, 2.2, "心形线 $r=a(1+\\cos\\theta)$")
ax.plot(r * np.cos(th), r * np.sin(th), color=RED, lw=2.6, zorder=3)
ax.plot([0], [0], "o", color=INK, ms=6, zorder=6)
ax.plot([2 * a], [0], "o", color=BLUE, ms=7, zorder=6)
ax.annotate("$\\theta=0$：$r=2a$", xy=(2 * a, 0), xytext=(0.30, 2.00),
            fontsize=F - 2, color=BLUE, arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.0))
ax.annotate("$\\theta=\\pi$：$r=0$，回到极点", xy=(0, 0), xytext=(-2.10, 1.55),
            fontsize=F - 2, color=INK, arrowprops=dict(arrowstyle="->", color=GREY, lw=1.0))

ax = axes[1]
rtheta_axes(ax, (-0.35, 2 * PI + 0.35), (-0.35, 2.45), "心形线 $r=a(1+\\cos\\theta)$")
ax.plot(th, r, color=RED, lw=2.6, zorder=3)
ax.plot([0, 2 * PI], [2, 2], "o", color=BLUE, ms=6, zorder=5)
ax.plot([PI], [0], "o", color=INK, ms=6, zorder=5)
ax.annotate("$\\theta=\\pi$ 时 $r$ 掉到 $0$，\n曲线的尖端就是这里", xy=(PI, 0), xytext=(3.55, 0.55),
            fontsize=F - 2.5, color=INK, arrowprops=dict(arrowstyle="->", color=GREY, lw=1.0))
fig.tight_layout(); fig.savefig(BASE + "pc-cardioid.png", dpi=150); plt.close(fig)


# ============ 2 玫瑰线 ============
r3 = np.sin(3 * th)
r2 = np.cos(2 * th)
fig, axes = plt.subplots(2, 2, figsize=(11.6, 8.8), dpi=150)

ax = axes[0][0]
polar_axes(ax, 1.35, "三叶玫瑰线 $r=a\\sin 3\\theta$")
ax.plot(r3 * np.cos(th), r3 * np.sin(th), color=ORANGE, lw=2.4, zorder=3)
for k in range(3):
    ang = PI / 6 + k * 2 * PI / 3
    ax.plot([0, np.cos(ang)], [0, np.sin(ang)], color=GREY, lw=0.9, ls=":", zorder=2)
    ax.text(0.60 * np.cos(ang), 0.60 * np.sin(ang), "%d" % (k + 1), fontsize=F - 1,
            color=ORANGE, ha="center", va="center")
ax.text(-1.3, -1.24, "$n$ 为奇数：$n$ 片（这里 3 片）", fontsize=F - 2.5, color=INK)

ax = axes[0][1]
polar_axes(ax, 1.35, "四叶玫瑰线 $r=a\\cos 2\\theta$")
ax.plot(r2 * np.cos(th), r2 * np.sin(th), color=GREEN, lw=2.4, zorder=3)
for k in range(4):
    ang = k * PI / 2
    ax.plot([0, np.cos(ang)], [0, np.sin(ang)], color=GREY, lw=0.9, ls=":", zorder=2)
    ax.text(0.62 * np.cos(ang), 0.62 * np.sin(ang), "%d" % (k + 1), fontsize=F - 1,
            color=GREEN, ha="center", va="center")
ax.text(-1.3, -1.24, "$n$ 为偶数：$2n$ 片（这里 4 片）", fontsize=F - 2.5, color=INK)

ax = axes[1][0]
rtheta_axes(ax, (-0.35, 2 * PI + 0.35), (-1.72, 1.40), "三叶玫瑰线 $r=a\\sin 3\\theta$")
ax.plot(th, r3, color=ORANGE, lw=2.4, zorder=3)
ax.axhline(0, color="#b0b0b0", lw=0.9, zorder=2)
ax.text(-0.25, -1.62, "三个正拱、三个负拱；负的一段 $r<0$，在反方向上画花瓣，所以片数是 3 不是 6", fontsize=F - 3.5, color=INK)

ax = axes[1][1]
rtheta_axes(ax, (-0.35, 2 * PI + 0.35), (-1.72, 1.40), "四叶玫瑰线 $r=a\\cos 2\\theta$")
ax.plot(th, r2, color=GREEN, lw=2.4, zorder=3)
ax.axhline(0, color="#b0b0b0", lw=0.9, zorder=2)
ax.text(-0.25, -1.62, "两正两负，共四个拱，正负各画出两瓣，合起来 4 片", fontsize=F - 3.5, color=INK)

fig.tight_layout(); fig.savefig(BASE + "pc-rose.png", dpi=150); plt.close(fig)


# ============ 3 双纽线 ============
a = 1.2
t2 = np.concatenate([np.linspace(-PI / 4, PI / 4, 900), np.linspace(3 * PI / 4, 5 * PI / 4, 900)])
r2d = a * np.sqrt(np.cos(2 * t2))
fig, axes = plt.subplots(1, 2, figsize=(12.0, 5.0), dpi=150)

ax = axes[0]
polar_axes(ax, 1.75, "双纽线 $r^{2}=a^{2}\\cos 2\\theta$")
ax.plot(r2d * np.cos(t2), r2d * np.sin(t2), color=BLUE, lw=2.6, zorder=3)
ax.plot([0], [0], "o", color=INK, ms=6, zorder=6)
ax.plot([a], [0], "o", color=RED, ms=7, zorder=6)
ax.plot([-a], [0], "o", color=RED, ms=7, zorder=6)
ax.text(a + 0.07, 0.15, "顶点", fontsize=F - 3, color=RED)
ax.text(-a - 0.55, 0.15, "顶点", fontsize=F - 3, color=RED)
ax.text(-1.70, -1.30, "只有 $\\cos 2\\theta\\geq0$ 的部分有图形", fontsize=F - 2.5, color=INK)

ax = axes[1]
rtheta_axes(ax, (-1.15, 4.35), (-1.50, 1.55), r"双纽线 $r^{2}=a^{2}\cos 2\theta$",
            ticks=[(0, "0"), (PI / 2, r"$\frac{\pi}{2}$"), (PI, r"$\pi$")])
tt = np.linspace(-PI / 4, PI / 4, 400)
ax.plot(tt, a * np.sqrt(np.cos(2 * tt)), color=BLUE, lw=2.6, zorder=3)
ax.plot(tt + PI, -a * np.sqrt(np.cos(2 * tt)), color=BLUE, lw=2.6, zorder=3)
for st in (-PI / 4, PI / 4, 3 * PI / 4, 5 * PI / 4):
    ax.axvline(st, color="#e0c8c8", lw=1.0, ls="--", zorder=1)
ax.text(0.55, -0.62, "$\\theta\\in\\left[-\\frac{\\pi}{4},\\frac{\\pi}{4}\\right]$：$r\\geq0$，画出一瓣",
        fontsize=F - 3, color=BLUE)
ax.text(2.60, 0.22, "$\\theta\\in\\left[\\frac{3\\pi}{4},\\frac{5\\pi}{4}\\right]$：$r\\leq0$，\n沿反方向也画出一瓣",
        fontsize=F - 3, color=BLUE)
ax.text(2.30, 1.30, "中间的区间 $\\cos 2\\theta<0$，$r$ 无定义，图上没有曲线",
        fontsize=F - 3, color=GREY)
fig.tight_layout(); fig.savefig(BASE + "pc-lemniscate.png", dpi=150); plt.close(fig)


# ============ 4 阿基米德螺线 ============
fig, axes = plt.subplots(1, 2, figsize=(12.0, 5.2), dpi=150)

ax = axes[0]
polar_axes(ax, 4.6, "阿基米德螺线 $r=a\\theta$")
th3 = np.linspace(0, 3 * PI, 1200)
ax.plot((0.5 * th3) * np.cos(th3), (0.5 * th3) * np.sin(th3), color=ORANGE, lw=2.4, zorder=3)
for k in range(1, 4):
    ang = k * PI / 2
    rr = 0.5 * ang
    ax.plot([0, rr * np.cos(ang)], [0, rr * np.sin(ang)], color=GREY, lw=0.9, ls=":", zorder=2)
    ax.plot([rr * np.cos(ang)], [rr * np.sin(ang)], "o", color=ORANGE, ms=5, zorder=5)
ax.text(-4.4, -3.75, "每转半圈，$r$ 增加同样的量 $\\pi a/2$", fontsize=F - 2, color=INK)
ax.text(-4.4, -4.20, "相邻两圈间距相等", fontsize=F - 2, color=GREY)

ax = axes[1]
rtheta_axes(ax, (-0.35, 3 * PI + 0.35), (-0.6, 5.2), "阿基米德螺线 $r=a\\theta$",
            ticks=[(0, "0"), (PI, r"$\pi$"), (2 * PI, r"$2\pi$"), (3 * PI, r"$3\pi$")])
ax.plot(th3, 0.5 * th3, color=ORANGE, lw=2.6, zorder=3)
ax.text(0.35, 4.3, "在直角坐标里它是一条过原点的直线：\n$r$ 与 $\\theta$ 成正比",
        fontsize=F - 3, color=INK)
fig.tight_layout(); fig.savefig(BASE + "pc-spiral-arch.png", dpi=150); plt.close(fig)


# ============ 5 对数螺线 ============
fig, axes = plt.subplots(1, 2, figsize=(12.0, 5.2), dpi=150)

ax = axes[0]
polar_axes(ax, 8.2, "对数螺线 $r=e^{a\\theta}$")
th4 = np.linspace(0, 3 * PI, 1400)
r4 = np.exp(0.28 * th4)
ax.plot(r4 * np.cos(th4), r4 * np.sin(th4), color=GREEN, lw=2.4, zorder=3)
for k in range(1, 4):
    ang = k * PI / 2
    rr = np.exp(0.28 * ang)
    ax.plot([0, rr * np.cos(ang)], [0, rr * np.sin(ang)], color=GREY, lw=0.9, ls=":", zorder=2)
    ax.plot([rr * np.cos(ang)], [rr * np.sin(ang)], "o", color=GREEN, ms=5, zorder=5)
ax.text(-8.0, -6.9, "每转半圈，$r$ 按同一个倍数放大", fontsize=F - 2, color=INK)
ax.text(-8.0, -7.6, "越往外圈越大", fontsize=F - 2, color=GREY)
ax.text(-8.0, 4.60, "等角螺线：半径与切线的夹角处处相同", fontsize=F - 2, color=GREY)

ax = axes[1]
rtheta_axes(ax, (-0.35, 3 * PI + 0.35), (-0.6, 14.5), "对数螺线 $r=e^{a\\theta}$",
            ticks=[(0, "0"), (PI, r"$\pi$"), (2 * PI, r"$2\pi$"), (3 * PI, r"$3\pi$")])
ax.plot(th4, r4, color=GREEN, lw=2.6, zorder=3)
ax.text(0.30, 9.5, "在直角坐标里它是一条指数曲线：\n转角相同，$r$ 就乘同一个倍数",
        fontsize=F - 3, color=INK)
fig.tight_layout(); fig.savefig(BASE + "pc-spiral-log.png", dpi=150); plt.close(fig)

print("done")
