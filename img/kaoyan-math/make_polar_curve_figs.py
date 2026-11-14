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
BOX = dict(boxstyle="round,pad=0.32", facecolor="white", edgecolor="#dddddd")

POL_N = "极坐标"


def combo(name, fname, lim, polar, cart, eq_p, eq_c, extra_notes=(), eqfont=None):
    """同一张开两格：左极坐标平面(彩色)，右直角坐标平面(另一种颜色)，两公式都放图上。"""
    fig, axes = plt.subplots(1, 2, figsize=(12.6, 5.6), dpi=150)
    axp, axc = axes

    # 左：极坐标
    th = np.linspace(0, 2 * np.pi, 400)
    step = 0.5 if lim <= 6 else 2.0
    for rr in np.arange(step, lim + 0.01, step):
        axp.plot(rr * np.cos(th), rr * np.sin(th), color="#ececec", lw=0.8, zorder=0)
    for a0 in np.arange(0, np.pi, np.pi / 6):
        for sg in (1, -1):
            axp.plot([0, lim * np.cos(a0) * sg], [0, lim * np.sin(a0) * sg],
                     color="#ececec", lw=0.8, zorder=0)
    axp.axhline(0, color="#c8c8c8", lw=1.0, zorder=1)
    axp.axvline(0, color="#c8c8c8", lw=1.0, zorder=1)
    axp.set_xlim(-lim, lim); axp.set_ylim(-lim, lim)
    axp.set_aspect("equal"); axp.set_xticks([]); axp.set_yticks([])
    for sp in axp.spines.values():
        sp.set_color("#cccccc")
    axp.set_title(f"{name}\n极坐标平面", fontsize=T, color=INK, pad=6)
    axp.text(0.97, 0.03, eq_p, transform=axp.transAxes,
             fontsize=(eqfont if eqfont else F - 2.5), color=INK,
             ha="right", va="bottom", bbox=BOX)
    polar(axp)

    # 右：直角坐标
    axc.set_xlim(-lim, lim); axc.set_ylim(-lim, lim)
    axc.set_aspect("equal")
    axc.grid(True, color="#ececec", lw=0.8)
    axc.axhline(0, color="#c8c8c8", lw=1.0, zorder=1)
    axc.axvline(0, color="#c8c8c8", lw=1.0, zorder=1)
    tk = [-4, -2, 0, 2, 4] if lim > 6 else [-2, -1, 0, 1, 2]
    tk = [t for t in tk if -lim < t < lim]
    axc.set_xticks(tk); axc.set_yticks(tk)
    axc.set_xticklabels([str(t) for t in tk], fontsize=F - 3.5, color="#999999")
    axc.set_yticklabels([str(t) for t in tk], fontsize=F - 3.5, color="#999999")
    axc.tick_params(length=2, colors="#cccccc")
    for sp in axc.spines.values():
        sp.set_color("#cccccc")
    axc.set_title(f"{name}\n直角坐标平面", fontsize=T, color=INK, pad=6)
    axc.set_xlabel("$x$", fontsize=F - 1, color=INK, labelpad=0)
    axc.set_ylabel("$y$", fontsize=F - 1, color=INK, labelpad=0)
    axc.text(0.97, 0.03, eq_c, transform=axc.transAxes,
             fontsize=(eqfont if eqfont else F - 2.5), color=INK,
             ha="right", va="bottom", bbox=BOX)
    cart(axc)

    for xy, txt, col in extra_notes:
        axp.annotate(txt, xy=xy, fontsize=F - 2.5, color=col,
                     ha="center", va="center",
                     arrowprops=dict(arrowstyle="->", color=col, lw=1.0))
    fig.tight_layout()
    fig.savefig(BASE + fname, dpi=150)
    plt.close(fig)


a = 1.0
th = np.linspace(0, 2 * np.pi, 2000)

combo("心形线", "pc-cardioid-step1.png", 2.5,
    lambda ax: ax.plot(r * np.cos(th), r * np.sin(th), color=RED, lw=2.6, zorder=3),
    None, r"$r=a(1+\cos\theta)$", None)
