import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.family"] = ["PingFang SC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

INK, ORANGE, BLUE, RED, GREEN, GREY = "#2b2b2b", "#d2691e", "#2f4f6f", "#b03a2e", "#4a7c59", "#8a8a8a"
BASE = "/Users/fred/Documents/GitHub/cycleuser/blog/output/img/kaoyan-math/"
F, T = 11.5, 12.0
PI = np.pi
BOX = dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#dddddd")


def polar_axes(ax, lim, title):
    th = np.linspace(0, 2 * np.pi, 400)
    step = 0.5 if lim <= 6 else 2.0
    for rr in np.arange(step, lim + 0.01, step):
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
    ax.set_title(title + "\n极坐标平面：$r$ 随 $\\theta$ 变化", fontsize=T, color=INK, pad=6)


def yx_axes(ax, xlim, ylim, title, eq, ticks=None, ticks_are_pi=True):
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    ax.grid(True, color="#ececec", lw=0.8)
    ax.axhline(0, color="#c8c8c8", lw=1.1, zorder=2)
    ax.axvline(0, color="#c8c8c8", lw=1.1, zorder=2)
    if ticks is None:
        ticks = [0, PI / 2, PI, 3 * PI / 2, 2 * PI]
    labels = [r"$0$", r"$\frac{\pi}{2}$", r"$\pi$", r"$\frac{3\pi}{2}$", r"$2\pi$"]
    if ticks_are_pi:
        ax.set_xticks(ticks)
        ax.set_xticklabels(labels[:len(ticks)], fontsize=F - 2.5, color=INK)
    ax.set_yticks([])
    ax.tick_params(axis="x", colors="#bbbbbb", length=3)
    for sp in ax.spines.values():
        sp.set_color("#cccccc")
    ax.set_title(title + "\n直角坐标：把 $r,\\theta$ 换成 $y,x$", fontsize=T, color=INK, pad=6)
    ax.set_xlabel("$x$", fontsize=F, color=INK, labelpad=1)
    ax.set_ylabel("$y$", fontsize=F, color=INK, labelpad=1)
    ax.text(0.5, 0.94, eq, transform=ax.transAxes, fontsize=F - 1, color=INK,
            ha="center", va="top", bbox=BOX)


# ============ 1 心形线 ============
a = 1.0
th = np.linspace(0, 2 * np.pi, 2000)
r = a * (1 + np.cos(th))
fig, axes = plt.subplots(1, 2, figsize=(12.6, 4.8), dpi=150)

ax = axes[0]
polar_axes(ax, 2.2, "心形线 $r=a(1+\\cos\\theta)$")
ax.plot(r * np.cos(th), r * np.sin(th), color=RED, lw=2.6, zorder=3)
ax.plot([0], [0], "o", color=INK, ms=6, zorder=6)
ax.plot([2 * a], [0], "o", color=BLUE, ms=7, zorder=6)
ax.text(1.75, 0.32, "$\\theta=0$：$r=2a$", fontsize=F - 2, color=BLUE)
ax.text(-2.05, 1.75, "$\\theta=\\pi$：$r=0$", fontsize=F - 2, color=INK)

ax = axes[1]
yx_axes(ax, (-0.35, 2 * PI + 0.35), (-0.4, 2.5), "心形线的式子里 $r\\to y$、$\\theta\\to x$",
        "$y=a(1+\\cos x)$")
ax.plot(th, r, color=RED, lw=2.6, zorder=3)
ax.plot([0, 2 * PI], [2, 2], "o", color=BLUE, ms=6, zorder=5)
ax.plot([PI], [0], "o", color=INK, ms=6, zorder=5)
ax.text(PI + 0.25, 0.42, "$x=\\pi$ 时 $y=0$", fontsize=F - 2.5, color=INK)

fig.tight_layout(); fig.savefig(BASE + "pc-cardioid.png", dpi=150); plt.close(fig)


# ============ 2 玫瑰线 ============
r3 = np.sin(3 * th)
r4 = np.cos(2 * th)
fig, axes = plt.subplots(2, 2, figsize=(12.6, 9.2), dpi=150)

ax = axes[0][0]
polar_axes(ax, 1.35, "三叶玫瑰线 $r=a\\sin 3\\theta$")
ax.plot(r3 * np.cos(th), r3 * np.sin(th), color=ORANGE, lw=2.4, zorder=3)
ax.text(-1.30, -1.22, "$n$ 为奇数：3 片", fontsize=F - 2.5, color=INK)

ax = axes[0][1]
yx_axes(ax, (-0.35, 2 * PI + 0.35), (-1.45, 1.45), "三叶玫瑰线的式子里 $r\\to y$、$\\theta\\to x$",
        "$y=a\\sin 3x$")
ax.plot(th, r3, color=ORANGE, lw=2.4, zorder=3)

ax = axes[1][0]
polar_axes(ax, 1.35, "四叶玫瑰线 $r=a\\cos 2\\theta$")
ax.plot(r4 * np.cos(th), r4 * np.sin(th), color=GREEN, lw=2.4, zorder=3)
ax.text(-1.30, -1.22, "$n$ 为偶数：4 片", fontsize=F - 2.5, color=INK)

ax = axes[1][1]
yx_axes(ax, (-0.35, 2 * PI + 0.35), (-1.45, 1.45), "四叶玫瑰线的式子里 $r\\to y$、$\\theta\\to x$",
        "$y=a\\cos 2x$")
ax.plot(th, r4, color=GREEN, lw=2.4, zorder=3)

fig.tight_layout(); fig.savefig(BASE + "pc-rose.png", dpi=150); plt.close(fig)


# ============ 3 双纽线 ============
a = 1.2
t2 = np.concatenate([np.linspace(-PI / 4, PI / 4, 900), np.linspace(3 * PI / 4, 5 * PI / 4, 900)])
r2 = a * np.sqrt(np.cos(2 * t2))
fig, axes = plt.subplots(1, 2, figsize=(12.6, 4.8), dpi=150)

ax = axes[0]
polar_axes(ax, 1.75, "双纽线 $r^{2}=a^{2}\\cos 2\\theta$")
ax.plot(r2 * np.cos(t2), r2 * np.sin(t2), color=BLUE, lw=2.6, zorder=3)
ax.plot([0], [0], "o", color=INK, ms=6, zorder=6)
ax.plot([a, -a], [0, 0], "o", color=RED, ms=7, zorder=6)
ax.text(-1.70, -1.32, "只在 $\\cos 2\\theta\\geq0$ 处有图形", fontsize=F - 2.5, color=INK)

ax = axes[1]
yx_axes(ax, (-1.15, 4.35), (-1.50, 1.55), "双纽线的式子里 $r\\to y$、$\\theta\\to x$",
        "$y^{2}=a^{2}\\cos 2x$", ticks=[0, PI / 2, PI], )
ax.set_xticks([0, PI / 2, PI])
ax.set_xticklabels([r"$0$", r"$\frac{\pi}{2}$", r"$\pi$"], fontsize=F - 2.5, color=INK)
tt = np.linspace(-PI / 4, PI / 4, 500)
ax.plot(tt, a * np.sqrt(np.cos(2 * tt)), color=BLUE, lw=2.6, zorder=3)
ax.plot(tt, -a * np.sqrt(np.cos(2 * tt)), color=BLUE, lw=2.6, zorder=3)
tt2 = np.linspace(3 * PI / 4, 5 * PI / 4, 500)
ax.plot(tt2, a * np.sqrt(np.cos(2 * tt2)), color=BLUE, lw=2.6, zorder=3)
ax.plot(tt2, -a * np.sqrt(np.cos(2 * tt2)), color=BLUE, lw=2.6, zorder=3)
for st in (-PI / 4, PI / 4, 3 * PI / 4, 5 * PI / 4):
    ax.axvline(st, color="#e0c8c8", lw=1.0, ls="--", zorder=1)
ax.text(0.15, 1.32, "$\\cos 2x\\geq0$ 的两段各画出一对分支", fontsize=F - 3, color=BLUE)

fig.tight_layout(); fig.savefig(BASE + "pc-lemniscate.png", dpi=150); plt.close(fig)


# ============ 4 阿基米德螺线 ============
fig, axes = plt.subplots(1, 2, figsize=(12.6, 4.8), dpi=150)
th3 = np.linspace(0, 3 * PI, 1200)
r3s = 0.5 * th3

ax = axes[0]
polar_axes(ax, 5.0, "阿基米德螺线 $r=a\\theta$")
ax.plot(r3s * np.cos(th3), r3s * np.sin(th3), color=ORANGE, lw=2.4, zorder=3)
ax.text(-4.85, 4.55, "每转一圈，$r$ 加 $2\\pi a$", fontsize=F - 2, color=INK)

ax = axes[1]
yx_axes(ax, (-0.35, 3 * PI + 0.35), (-0.6, 5.4), "阿基米德螺线的式子里 $r\\to y$、$\\theta\\to x$",
        "$y=ax$", ticks=[0, PI, 2 * PI, 3 * PI])
ax.set_xticks([0, PI, 2 * PI, 3 * PI])
ax.set_xticklabels([r"$0$", r"$\pi$", r"$2\pi$", r"$3\pi$"], fontsize=F - 2.5, color=INK)
ax.plot(th3, r3s, color=ORANGE, lw=2.6, zorder=3)

fig.tight_layout(); fig.savefig(BASE + "pc-spiral-arch.png", dpi=150); plt.close(fig)


# ============ 5 对数螺线 ============
fig, axes = plt.subplots(1, 2, figsize=(12.6, 4.8), dpi=150)
th4 = np.linspace(0, 3 * PI, 1600)
r4s = np.exp(0.28 * th4)

ax = axes[0]
polar_axes(ax, 14.6, "对数螺线 $r=e^{a\\theta}$")
ax.plot(r4s * np.cos(th4), r4s * np.sin(th4), color=GREEN, lw=2.2, zorder=3)
ax.text(-14.2, 12.2, "每转一圈，$r$ 乘 $e^{2\\pi a}$", fontsize=F - 2, color=INK)

ax = axes[1]
yx_axes(ax, (-0.35, 3 * PI + 0.35), (-0.6, 15.2), "对数螺线的式子里 $r\\to y$、$\\theta\\to x$",
        "$y=e^{ax}$", ticks=[0, PI, 2 * PI, 3 * PI])
ax.set_xticks([0, PI, 2 * PI, 3 * PI])
ax.set_xticklabels([r"$0$", r"$\pi$", r"$2\pi$", r"$3\pi$"], fontsize=F - 2.5, color=INK)
ax.plot(th4, r4s, color=GREEN, lw=2.6, zorder=3)

fig.tight_layout(); fig.savefig(BASE + "pc-spiral-log.png", dpi=150); plt.close(fig)
print("done")
