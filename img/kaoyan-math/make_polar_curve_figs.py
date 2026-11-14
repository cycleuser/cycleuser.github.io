import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.family"] = ["PingFang SC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

INK, ORANGE, BLUE = "#2b2b2b", "#d2691e", "#2f4f6f"
CREAM, RED, GREEN, GREY, BROWN = "#f3e3ce", "#b03a2e", "#4a7c59", "#8a8a8a", "#7a5230"
BASE = "/Users/fred/Documents/GitHub/cycleuser/blog/output/img/kaoyan-math/"
F, T = 12, 13


def polar_axes(ax, lim, title):
    th = np.linspace(0, 2 * np.pi, 400)
    for rr in np.arange(0.5, lim + 0.01, 0.5):
        ax.plot(rr * np.cos(th), rr * np.sin(th), color="#ececec", lw=0.8, zorder=0)
    for a in np.arange(0, np.pi, np.pi / 6):
        ax.plot([0, lim * np.cos(a)], [0, lim * np.sin(a)], color="#ececec", lw=0.8, zorder=0)
        ax.plot([0, -lim * np.cos(a)], [0, -lim * np.sin(a)], color="#ececec", lw=0.8, zorder=0)
    ax.axhline(0, color="#d8d8d8", lw=0.9, zorder=1)
    ax.axvline(0, color="#d8d8d8", lw=0.9, zorder=1)
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_color("#cccccc")
    ax.set_title(title, fontsize=T, color=INK, pad=8)


# ============ 1 心形线 ============
a = 1.0
fig, ax = plt.subplots(figsize=(6.2, 5.4), dpi=150)
polar_axes(ax, 2.2, "心形线：$r=a(1+\\cos\\theta)$")
th = np.linspace(0, 2 * np.pi, 1000)
r = a * (1 + np.cos(th))
ax.plot(r * np.cos(th), r * np.sin(th), color=RED, lw=2.6, zorder=3)
ax.plot([0], [0], "o", color=INK, ms=6, zorder=6)
ax.annotate("尖端在极点\n（$\\theta=\\pi$，$r=0$）", xy=(0, 0), xytext=(-2.05, 1.55),
            fontsize=F - 2, color=INK, arrowprops=dict(arrowstyle="->", color=GREY, lw=1.0))
ax.plot([2 * a], [0], "o", color=BLUE, ms=7, zorder=6)
ax.annotate("$\\theta=0$ 时 $r=2a$，最远处", xy=(2 * a, 0), xytext=(0.55, 1.95),
            fontsize=F - 2, color=BLUE, arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.0))
ax.text(-2.1, -1.55, "关于极轴对称，形状像一颗心", fontsize=F - 1.5, color=GREY)
ax.text(-2.1, -1.95, "$\\theta$ 从 $0$ 转到 $2\\pi$ 描出一整圈", fontsize=F - 1.5, color=GREY)
fig.tight_layout(); fig.savefig(BASE + "pc-cardioid.png", dpi=150); plt.close(fig)


# ============ 2 玫瑰线：三叶与四叶 ============
fig, axes = plt.subplots(1, 2, figsize=(11.6, 5.4), dpi=150)
th = np.linspace(0, 2 * np.pi, 2000)

ax = axes[0]
polar_axes(ax, 1.35, "三叶玫瑰线：$r=a\\sin 3\\theta$")
r = np.sin(3 * th)
ax.plot(r * np.cos(th), r * np.sin(th), color=ORANGE, lw=2.4, zorder=3)
for k in range(3):
    ang = np.pi / 6 + k * 2 * np.pi / 3
    ax.plot([0, np.cos(ang)], [0, np.sin(ang)], color=GREY, lw=0.9, ls=":", zorder=2)
    ax.text(0.60 * np.cos(ang), 0.60 * np.sin(ang), "%d" % (k + 1), fontsize=F - 1,
            color=ORANGE, ha="center", va="center")
ax.text(-1.3, -1.22, "$n$ 为奇数：$n$ 片（这里 3 片）", fontsize=F - 2, color=INK)

ax = axes[1]
polar_axes(ax, 1.35, "四叶玫瑰线：$r=a\\cos 2\\theta$")
r = np.cos(2 * th)
ax.plot(r * np.cos(th), r * np.sin(th), color=GREEN, lw=2.4, zorder=3)
for k in range(4):
    ang = k * np.pi / 2
    ax.plot([0, np.cos(ang)], [0, np.sin(ang)], color=GREY, lw=0.9, ls=":", zorder=2)
    ax.text(0.62 * np.cos(ang), 0.62 * np.sin(ang), "%d" % (k + 1), fontsize=F - 1,
            color=GREEN, ha="center", va="center")
ax.text(-1.3, -1.22, "$n$ 为偶数：$2n$ 片（这里 4 片）", fontsize=F - 2, color=INK)
fig.tight_layout(); fig.savefig(BASE + "pc-rose.png", dpi=150); plt.close(fig)


# ============ 3 双纽线 ============
a = 1.2
fig, ax = plt.subplots(figsize=(6.2, 5.0), dpi=150)
polar_axes(ax, 1.6, "双纽线：$r^{2}=a^{2}\\cos 2\\theta$")
t2 = np.concatenate([np.linspace(-np.pi / 4, np.pi / 4, 900),
                     np.linspace(3 * np.pi / 4, 5 * np.pi / 4, 900)])
r2 = a * np.sqrt(np.cos(2 * t2))
ax.plot(r2 * np.cos(t2), r2 * np.sin(t2), color=BLUE, lw=2.6, zorder=3)
ax.plot([0], [0], "o", color=INK, ms=6, zorder=6)
ax.plot([a], [0], "o", color=RED, ms=7, zorder=6)
ax.plot([-a], [0], "o", color=RED, ms=7, zorder=6)
ax.annotate("左右各一个顶点\n$(\\theta=0,\\ \\pi)$", xy=(a, 0), xytext=(0.35, 1.35),
            fontsize=F - 2, color=RED, arrowprops=dict(arrowstyle="->", color=RED, lw=1.0))
ax.text(-1.55, -1.20, "只有 $\\cos 2\\theta\\geq0$ 的部分有图形，", fontsize=F - 2, color=INK)
ax.text(-1.55, -1.45, "即 $\\theta\\in[-\\frac{\\pi}{4},\\frac{\\pi}{4}]\\cup[\\frac{3\\pi}{4},\\frac{5\\pi}{4}]$",
        fontsize=F - 2, color=INK)
ax.text(-1.55, 1.35, "形状像横放的 8 字，两瓣对称", fontsize=F - 2, color=GREY)
fig.tight_layout(); fig.savefig(BASE + "pc-lemniscate.png", dpi=150); plt.close(fig)


# ============ 4 阿基米德螺线 ============
fig, ax = plt.subplots(figsize=(6.2, 5.6), dpi=150)
polar_axes(ax, 4.6, "阿基米德螺线：$r=a\\theta$")
th = np.linspace(0, 3 * np.pi, 1200)
r = 0.5 * th
ax.plot(r * np.cos(th), r * np.sin(th), color=ORANGE, lw=2.4, zorder=3)
for k in range(1, 4):
    ang = k * np.pi / 2
    rr = 0.5 * ang
    ax.plot([0, rr * np.cos(ang)], [0, rr * np.sin(ang)], color=GREY, lw=0.9, ls=":", zorder=2)
    ax.plot([rr * np.cos(ang)], [rr * np.sin(ang)], "o", color=ORANGE, ms=5, zorder=5)
ax.text(-4.4, -3.7, "每转半圈，$r$ 增加同样的量 $\\pi a/2$", fontsize=F - 1.5, color=INK)
ax.text(-4.4, -4.15, "像蚊香的纹路，间距相等", fontsize=F - 1.5, color=GREY)
ax.text(1.2, 3.9, "$r=\\theta$ 时就是它", fontsize=F - 1.5, color=BROWN)
fig.tight_layout(); fig.savefig(BASE + "pc-spiral-arch.png", dpi=150); plt.close(fig)


# ============ 5 对数螺线 ============
fig, ax = plt.subplots(figsize=(6.2, 5.6), dpi=150)
polar_axes(ax, 8.2, "对数螺线：$r=e^{a\\theta}$")
th = np.linspace(0, 3 * np.pi, 1400)
r = np.exp(0.28 * th)
ax.plot(r * np.cos(th), r * np.sin(th), color=GREEN, lw=2.4, zorder=3)
for k in range(1, 4):
    ang = k * np.pi / 2
    rr = np.exp(0.28 * ang)
    ax.plot([0, rr * np.cos(ang)], [0, rr * np.sin(ang)], color=GREY, lw=0.9, ls=":", zorder=2)
    ax.plot([rr * np.cos(ang)], [rr * np.sin(ang)], "o", color=GREEN, ms=5, zorder=5)
ax.text(-8.0, -6.6, "每转半圈，$r$ 按同一个倍数放大", fontsize=F - 1.5, color=INK)
ax.text(-8.0, -7.4, "像鹦鹉螺的壳，越转越大", fontsize=F - 1.5, color=GREY)
ax.text(1.0, 7.0, "等角螺线：所有半径与切线的夹角相同", fontsize=F - 2, color=GREY)
fig.tight_layout(); fig.savefig(BASE + "pc-spiral-log.png", dpi=150); plt.close(fig)

print("polar figs done")
