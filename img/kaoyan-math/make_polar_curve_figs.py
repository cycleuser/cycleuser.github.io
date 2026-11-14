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
    ax.set_title(title + "\n极坐标平面", fontsize=T, color=INK, pad=6)


def cart_axes(ax, lim, title, eq, note="", eqfont=None):
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)
    ax.set_aspect("equal")
    ax.grid(True, color="#ececec", lw=0.8)
    ax.axhline(0, color="#c8c8c8", lw=1.0, zorder=1)
    ax.axvline(0, color="#c8c8c8", lw=1.0, zorder=1)
    tk = [t for t in (-2, -1, 0, 1, 2, 3) if -lim < t < lim]
    ax.set_xticks(tk); ax.set_yticks(tk)
    ax.set_xticklabels([str(t) for t in tk], fontsize=F - 3.5, color="#999999")
    ax.set_yticklabels([str(t) for t in tk], fontsize=F - 3.5, color="#999999")
    ax.tick_params(length=2, colors="#cccccc")
    for sp in ax.spines.values():
        sp.set_color("#cccccc")
    ax.set_xlabel("$x$", fontsize=F - 1, color=INK, labelpad=0)
    ax.set_ylabel("$y$", fontsize=F - 1, color=INK, labelpad=0)
    ax.set_title(title + "\n代入后得到的 $x$–$y$ 关系", fontsize=T, color=INK, pad=6)
    ax.text(0.5, 0.035, eq, transform=ax.transAxes,
            fontsize=(eqfont if eqfont else F - 2), color=INK,
            ha="center", va="bottom", bbox=BOX)
    if note:
        ax.text(0.5, 0.135, note, transform=ax.transAxes, fontsize=F - 3.5,
                color=GREY, ha="center", va="bottom")


# ============ 1 心形线 ============
a = 1.0
th = np.linspace(0, 2 * np.pi, 2000)
r = a * (1 + np.cos(th))
fig, axes = plt.subplots(1, 2, figsize=(12.6, 5.0), dpi=150)

ax = axes[0]
polar_axes(ax, 2.2, "心形线 $r=a(1+\\cos\\theta)$")
ax.plot(r * np.cos(th), r * np.sin(th), color=RED, lw=2.6, zorder=3)
ax.plot([0], [0], "o", color=INK, ms=6, zorder=6)
ax.plot([2 * a], [0], "o", color=BLUE, ms=7, zorder=6)
ax.text(1.60, 0.32, "$\\theta=0$：$r=2a$", fontsize=F - 2, color=BLUE)
ax.text(-2.05, 1.62, "$\\theta=\\pi$：$r=0$", fontsize=F - 2, color=INK)

ax = axes[1]
cart_axes(ax, 2.4, "心形线",
          "$y=\\pm\\sqrt{\\left(\\dfrac{a\\pm\\sqrt{a^{2}+4ax}}{2}\\right)^{2}-x^{2}}$", eqfont=F - 4.5)
xs = np.linspace(-a / 4, 2 * a, 3000)
sp = np.sqrt(a * a + 4 * a * xs)
for sgn in (1, -1):
    t = (a + sgn * sp) / 2
    y2 = t * t - xs * xs
    m = y2 >= 0
    ax.plot(xs[m], np.sqrt(y2[m]), color=RED, lw=2.6, zorder=3)
    ax.plot(xs[m], -np.sqrt(y2[m]), color=RED, lw=2.6, zorder=3)
ax.plot([0], [0], "o", color=INK, ms=6, zorder=6)
ax.plot([2 * a], [0], "o", color=BLUE, ms=7, zorder=6)

fig.tight_layout(); fig.savefig(BASE + "pc-cardioid.png", dpi=150); plt.close(fig)


# ============ 2 玫瑰线 ============
r3 = np.sin(3 * th)
r4 = np.cos(2 * th)
fig, axes = plt.subplots(2, 2, figsize=(12.6, 9.6), dpi=150)

ax = axes[0][0]
polar_axes(ax, 1.35, "三叶玫瑰线 $r=a\\sin 3\\theta$")
ax.plot(r3 * np.cos(th), r3 * np.sin(th), color=ORANGE, lw=2.4, zorder=3)
ax.text(-1.30, -1.22, "3 片", fontsize=F - 2.5, color=INK)

ax = axes[0][1]
cart_axes(ax, 1.45, "三叶玫瑰线", "$\\left(x^{2}+y^{2}\\right)^{2}=ay\\left(3x^{2}-y^{2}\\right)$",
          note="关于 $y$ 是四次方程，解不成 $y=f(x)$", eqfont=F - 3.5)
ax.plot(r3 * np.cos(th), r3 * np.sin(th), color=ORANGE, lw=2.4, zorder=3)

ax = axes[1][0]
polar_axes(ax, 1.35, "四叶玫瑰线 $r=a\\cos 2\\theta$")
ax.plot(r4 * np.cos(th), r4 * np.sin(th), color=GREEN, lw=2.4, zorder=3)
ax.text(-1.30, -1.22, "4 片", fontsize=F - 2.5, color=INK)

ax = axes[1][1]
cart_axes(ax, 1.45, "四叶玫瑰线", "$\\left(x^{2}+y^{2}\\right)^{3}=a^{2}\\left(x^{2}-y^{2}\\right)^{2}$",
          note="关于 $y$ 是六次方程，解不成 $y=f(x)$", eqfont=F - 3.5)
ax.plot(r4 * np.cos(th), r4 * np.sin(th), color=GREEN, lw=2.4, zorder=3)

fig.tight_layout(); fig.savefig(BASE + "pc-rose.png", dpi=150); plt.close(fig)


# ============ 3 双纽线 ============
a = 1.2
fig, axes = plt.subplots(1, 2, figsize=(12.6, 5.0), dpi=150)

ax = axes[0]
polar_axes(ax, 1.75, "双纽线 $r^{2}=a^{2}\\cos 2\\theta$")
t2 = np.concatenate([np.linspace(-PI / 4, PI / 4, 900), np.linspace(3 * PI / 4, 5 * PI / 4, 900)])
r2 = a * np.sqrt(np.cos(2 * t2))
ax.plot(r2 * np.cos(t2), r2 * np.sin(t2), color=BLUE, lw=2.6, zorder=3)
ax.plot([0], [0], "o", color=INK, ms=6, zorder=6)
ax.plot([a, -a], [0, 0], "o", color=RED, ms=7, zorder=6)
ax.text(-1.70, -1.32, "只在 $\\cos 2\\theta\\geq0$ 处有图形", fontsize=F - 2.5, color=INK)

ax = axes[1]
cart_axes(ax, 1.85, "双纽线", "$y=\\pm\\sqrt{\\dfrac{a\\sqrt{8x^{2}+a^{2}}-\\left(2x^{2}+a^{2}\\right)}{2}}$", eqfont=F - 4.5)
xs = np.linspace(-a, a, 3000)
ys = np.sqrt(np.maximum((a * np.sqrt(8 * xs * xs + a * a) - (2 * xs * xs + a * a)) / 2, 0))
ax.plot(xs, ys, color=BLUE, lw=2.6, zorder=3)
ax.plot(xs, -ys, color=BLUE, lw=2.6, zorder=3)
ax.plot([0], [0], "o", color=INK, ms=6, zorder=6)
ax.plot([a, -a], [0, 0], "o", color=RED, ms=7, zorder=6)

fig.tight_layout(); fig.savefig(BASE + "pc-lemniscate.png", dpi=150); plt.close(fig)


# ============ 4 阿基米德螺线 ============
fig, axes = plt.subplots(1, 2, figsize=(12.6, 5.0), dpi=150)
th3 = np.linspace(0, 3 * PI, 1200)
r3s = 0.5 * th3

ax = axes[0]
polar_axes(ax, 5.0, "阿基米德螺线 $r=a\\theta$")
ax.plot(r3s * np.cos(th3), r3s * np.sin(th3), color=ORANGE, lw=2.4, zorder=3)
ax.text(-4.85, 4.55, "每转一圈，$r$ 加 $2\\pi a$", fontsize=F - 2, color=INK)

ax = axes[1]
cart_axes(ax, 5.0, "阿基米德螺线", "$\\sqrt{x^{2}+y^{2}}=a\\arctan\\dfrac{y}{x}$",
          note="左端含反正切，解不成 $y=f(x)$", eqfont=F - 3.5)
ax.plot(r3s * np.cos(th3), r3s * np.sin(th3), color=ORANGE, lw=2.4, zorder=3)

fig.tight_layout(); fig.savefig(BASE + "pc-spiral-arch.png", dpi=150); plt.close(fig)


# ============ 5 对数螺线 ============
fig, axes = plt.subplots(1, 2, figsize=(12.6, 5.0), dpi=150)
th4 = np.linspace(0, 3 * PI, 1600)
r4s = np.exp(0.28 * th4)

ax = axes[0]
polar_axes(ax, 14.6, "对数螺线 $r=e^{a\\theta}$")
ax.plot(r4s * np.cos(th4), r4s * np.sin(th4), color=GREEN, lw=2.2, zorder=3)
ax.text(-14.2, 12.2, "每转一圈，$r$ 乘 $e^{2\\pi a}$", fontsize=F - 2, color=INK)

ax = axes[1]
cart_axes(ax, 14.6, "对数螺线", "$\\sqrt{x^{2}+y^{2}}=e^{a\\arctan\\frac{y}{x}}$",
          note="同样带反正切，解不成 $y=f(x)$", eqfont=F - 3.5)
ax.plot(r4s * np.cos(th4), r4s * np.sin(th4), color=GREEN, lw=2.2, zorder=3)

fig.tight_layout(); fig.savefig(BASE + "pc-spiral-log.png", dpi=150); plt.close(fig)
print("done")
