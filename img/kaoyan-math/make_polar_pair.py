import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.family"] = ["PingFang SC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

INK, ORANGE, BLUE, RED, GREEN, GREY, PURPLE = (
    "#2b2b2b", "#d2691e", "#2f4f6f", "#b03a2e", "#4a7c59", "#8a8a8a", "#7d3c98")
BASE = "/Users/fred/Documents/GitHub/cycleuser/blog/output/img/kaoyan-math/"
F, T = 11.0, 12.0
PI = np.pi
BOXP = dict(boxstyle="round,pad=0.28", facecolor="#fdf2e3", edgecolor="#e0b48a")
BOXC = dict(boxstyle="round,pad=0.28", facecolor="#eef2f7", edgecolor="#9ab0c9")


def single(fname, lim, eq_p, eq_c, draw_p, draw_c, note_p="", note_c="", eqfont=None):
    """一张图：极坐标网格作淡底、红色曲线（按极坐标方程）；
    直角坐标网格作淡底、蓝色曲线（按代入后的方程）；两者叠在同一坐标系。"""
    fig, ax = plt.subplots(figsize=(7.2, 7.2), dpi=170)
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)
    ax.set_aspect("equal")

    # 极坐标网（浅棕）
    th = np.linspace(0, 2 * np.pi, 400)
    step = 0.5 if lim <= 6 else 2.0
    for rr in np.arange(step, lim + 0.01, step):
        ax.plot(rr * np.cos(th), rr * np.sin(th), color="#eadfd0", lw=0.9, zorder=0)
    for a0 in np.arange(0, np.pi, np.pi / 6):
        for sg in (1, -1):
            ax.plot([0, lim * np.cos(a0) * sg], [0, lim * np.sin(a0) * sg],
                    color="#eadfd0", lw=0.9, zorder=0)

    # 直角坐标网（浅蓝）
    tk = [-4, -2, 0, 2, 4] if lim > 6 else [-2, -1, 0, 1, 2]
    tk = [t for t in tk if -lim < t < lim]
    for t in tk:
        ax.plot([t, t], [-lim, lim], color="#dbe4ee", lw=1.0, zorder=0)
        ax.plot([-lim, lim], [t, t], color="#dbe4ee", lw=1.0, zorder=0)

    ax.axhline(0, color="#c8c8c8", lw=1.1, zorder=1)
    ax.axvline(0, color="#c8c8c8", lw=1.1, zorder=1)
    ax.set_xticks(tk); ax.set_yticks(tk)
    ax.set_xticklabels([str(t) for t in tk], fontsize=F - 3.5, color="#999999")
    ax.set_yticklabels([str(t) for t in tk], fontsize=F - 3.5, color="#999999")
    ax.tick_params(length=2, colors="#cccccc")
    for sp in ax.spines.values():
        sp.set_color("#cccccc")
    ax.set_xlabel("$x$", fontsize=F, color=INK, labelpad=0)
    ax.set_ylabel("$y$", fontsize=F, color=INK, labelpad=0)
    ax.set_title("极坐标网与直角坐标网叠加\n红实线：按极坐标式画；蓝虚线：按代入后的方程画——两线重合",
                 fontsize=T - 1, color=INK, pad=8)

    draw_p(ax)
    draw_c(ax)

    ax.text(0.03, 0.975, eq_p, transform=ax.transAxes,
            fontsize=(eqfont if eqfont else F - 2.5), color="#a05a2c",
            ha="left", va="top", bbox=BOXP)
    ax.text(0.03, 0.90, eq_c, transform=ax.transAxes,
            fontsize=(eqfont if eqfont else F - 2.5), color=BLUE,
            ha="left", va="top", bbox=BOXC)
    if note_p:
        ax.text(0.03, 0.825, note_p, transform=ax.transAxes, fontsize=F - 3,
                color=RED, ha="left", va="top")
    fig.subplots_adjust(left=0.06, right=0.97, top=0.88, bottom=0.06)
    fig.savefig(BASE + fname, dpi=170)
    plt.close(fig)


a = 1.0
th = np.linspace(0, 2 * np.pi, 2000)
r = a * (1 + np.cos(th))
X0, Y0 = r * np.cos(th), r * np.sin(th)

def p_card(ax):
    ax.plot(X0, Y0, color=RED, lw=2.6, zorder=4, alpha=0.9)
    ax.plot([0], [0], "s", color=RED, ms=7, zorder=6)
def c_card(ax):
    xs = np.linspace(-a / 4, 2 * a, 4000)
    sp = np.sqrt(a * a + 4 * a * xs)
    for sgn in (1, -1):
        t = (a + sgn * sp) / 2
        y2 = np.maximum(t * t - xs * xs, 0)
        m = y2 >= 0
        ax.plot(xs[m], np.sqrt(y2[m]), color=BLUE, lw=1.6, ls=(0, (5, 3)), zorder=3)
        ax.plot(xs[m], -np.sqrt(y2[m]), color=BLUE, lw=1.6, ls=(0, (5, 3)), zorder=3)

single("pc-cardioid-pair.png", 2.3,
       r"$r=a(1+\cos\theta)$",
       r"$\left(x^{2}+y^{2}-ax\right)^{2}=a^{2}\left(x^{2}+y^{2}\right)$",
       p_card, c_card,
       note_p="")

a1 = 1.0
r3 = a1 * np.sin(3 * th)
X3, Y3 = r3 * np.cos(th), r3 * np.sin(th)
r4 = a1 * np.cos(2 * th)
X4, Y4 = r4 * np.cos(th), r4 * np.sin(th)

def p3(ax):
    ax.plot(X3, Y3, color=RED, lw=2.6, zorder=4, alpha=0.9)
def c3(ax):
    X, Y = np.meshgrid(np.linspace(-1.9, 1.9, 1100), np.linspace(-1.9, 1.9, 1100))
    Fg = (X * X + Y * Y) ** 2 - a1 * Y * (3 * X * X - Y * Y)
    ax.contour(X, Y, Fg, levels=[0], colors=[BLUE], linewidths=1.6, linestyles="dashed")

single("pc-rose3-pair.png", 1.6,
       r"$r=a\sin 3\theta$",
       r"$\left(x^{2}+y^{2}\right)^{2}=ay\left(3x^{2}-y^{2}\right)$",
       p3, c3,
       note_p="")

def p4(ax):
    ax.plot(X4, Y4, color=RED, lw=2.6, zorder=4, alpha=0.9)
def c4(ax):
    X, Y = np.meshgrid(np.linspace(-1.9, 1.9, 1100), np.linspace(-1.9, 1.9, 1100))
    Fg = (X * X + Y * Y) ** 3 - a1 ** 2 * (X * X - Y * Y) ** 2
    ax.contour(X, Y, Fg, levels=[0], colors=[BLUE], linewidths=1.6, linestyles="dashed")

single("pc-rose4-pair.png", 1.7,
       r"$r=a\cos 2\theta$",
       r"$\left(x^{2}+y^{2}\right)^{3}=a^{2}\left(x^{2}-y^{2}\right)^{2}$",
       p4, c4,
       note_p="")

a2 = 1.2
def p_lem(ax):
    t2 = np.concatenate([np.linspace(-PI / 4, PI / 4, 900), np.linspace(3 * PI / 4, 5 * PI / 4, 900)])
    r = a2 * np.sqrt(np.cos(2 * t2))
    ax.plot(r * np.cos(t2), r * np.sin(t2), color=RED, lw=2.6, zorder=4, alpha=0.9)
    ax.plot([a2, -a2], [0, 0], "o", color=RED, ms=7, zorder=6)
def c_lem(ax):
    xs = np.linspace(-a2, a2, 3000)
    ys = np.sqrt(np.maximum((a2 * np.sqrt(8 * xs * xs + a2 * a2) - (2 * xs * xs + a2 * a2)) / 2, 0))
    ax.plot(xs, ys, color=BLUE, lw=1.6, ls=(0, (5, 3)), zorder=3)
    ax.plot(xs, -ys, color=BLUE, lw=1.6, ls=(0, (5, 3)), zorder=3)

single("pc-lemniscate-pair.png", 2.4,
       r"$r^{2}=a^{2}\cos 2\theta$",
       r"$y=\pm\sqrt{\dfrac{a\sqrt{8x^{2}+a^{2}}-\left(2x^{2}+a^{2}\right)}{2}}$",
       p_lem, c_lem,
       eqfont=F - 3.5)

a3 = 0.5
th3 = np.linspace(0, 3 * PI, 2400)     # θ≥0，r≥0，单向展开
r = a3 * th3
def p_arch(ax):
    th3 = np.linspace(0, 3 * PI, 2400)
    r = a3 * th3
    ax.plot(r * np.cos(th3), r * np.sin(th3), color=RED, lw=2.4, zorder=4)
def c_arch(ax):
    ax.plot(r * np.cos(th3), r * np.sin(th3), color=BLUE, lw=1.5, ls=(0, (5, 3)), zorder=3)

single("pc-arch-pair.png", 5.4,
       r"$r=a\theta$",
       r"$\sqrt{x^{2}+y^{2}}=a\left(\arctan\frac{y}{x}+k\pi\right)$",
       p_arch, c_arch)

a4 = 0.28
th4 = np.linspace(0, 4 * PI, 3000)
r = np.exp(a4 * th4)
def p_log(ax):
    th4 = np.linspace(0, 4 * PI, 3000)
    r = np.exp(a4 * th4)
    ax.plot(r * np.cos(th4), r * np.sin(th4), color=RED, lw=2.2, zorder=4)
def c_log(ax):
    ax.plot(r * np.cos(th4), r * np.sin(th4), color=BLUE, lw=1.5, ls=(0, (5, 3)), zorder=3)

single("pc-log-pair.png", 26.0,
       r"$r=e^{a\theta}$",
       r"$\sqrt{x^{2}+y^{2}}=e^{a\left(\arctan\frac{y}{x}+k\pi\right)}$",
       p_log, c_log, eqfont=F - 3)

a5 = 1.6
tt = np.linspace(-PI / 2, 3 * PI / 2, 800)
XC = 2 * a5 * np.cos(tt) ** 2
YC = 2 * a5 * np.cos(tt) * np.sin(tt)

def p_cir(ax):
    ax.plot(XC, YC, color=RED, lw=2.6, zorder=4, alpha=0.9)
    ax.plot([0], [0], "s", color=RED, ms=7, zorder=6)
    ax.plot([2 * a5], [0], "o", color=RED, ms=6, zorder=6)
def c_cir(ax):
    ax.plot(XC, YC, color=BLUE, lw=1.6, ls=(0, (5, 3)), zorder=3)

single("pc-circle-pair.png", 3.4,
       r"$r=2a\cos\theta$",
       r"$y=\pm\sqrt{a^{2}-\left(x-a\right)^{2}}$",
       p_cir, c_cir)

def p_line(ax):
    tt2 = np.linspace(-1.2, 1.2, 300)
    ax.plot(np.ones_like(tt2), np.tan(tt2), color=RED, lw=2.6, zorder=4)
    ax.plot([0], [0], "s", color=RED, ms=7, zorder=6)
def c_line(ax):
    ax.plot([1, 1], [-2.1, 2.1], color=BLUE, lw=1.6, ls=(0, (5, 3)), zorder=3)

single("pc-line-pair.png", 2.6,
       r"$r=\sec\theta$",
       r"$x=1$",
       p_line, c_line)

print("ok 8 single")
