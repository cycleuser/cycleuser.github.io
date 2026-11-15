"""摆线一拱：左为曲线本身（标注拱宽、最高点、弧长），右为绕 x 轴的旋转体。"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import os

plt.rcParams["font.family"] = ["PingFang SC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
BASE = os.path.dirname(os.path.abspath(__file__)) + "/"
INK, ORANGE, RED, GREEN = "#2b2b2b", "#d2691e", "#b03a2e", "#4a7c59"
a = 1.0


def main():
    t = np.linspace(0, 2 * np.pi, 600)
    x = a * (t - np.sin(t))
    y = a * (1 - np.cos(t))
    fig = plt.figure(figsize=(12.6, 4.9), dpi=170)

    ax = fig.add_subplot(1, 2, 1)
    ax.plot(x, y, color=RED, lw=2.6)
    ax.annotate("", xy=(2 * np.pi * a, -0.45), xytext=(0, -0.45),
                arrowprops=dict(arrowstyle="<->", color=GREEN, lw=1.6))
    ax.text(np.pi * a, -0.72, "一拱宽 $2\\pi a$", fontsize=11, color=GREEN, ha="center")
    ax.annotate("", xy=(x[300], y[300]), xytext=(x[300], 2.15),
                arrowprops=dict(arrowstyle="<->", color=ORANGE, lw=1.6))
    ax.text(x[300] + 0.12, 1.98, "最高 $2a$", fontsize=11, color=ORANGE)
    ax.text(2.2, 1.62, "一拱长度\n$L=8a$", fontsize=12, color=RED, ha="center")
    ax.set_xlim(-0.55, 7.1); ax.set_ylim(-0.75, 2.6)
    ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_color("#d8dde3")
    ax.set_title("一拱（$a=1$ 时 $L=8$）", fontsize=13, color=INK, pad=8)

    ax3 = fig.add_subplot(1, 2, 2, projection="3d")
    tt = np.linspace(0.001, 2 * np.pi, 60)
    phi = np.linspace(0, 2 * np.pi, 48)
    XX = np.tile((a * (tt - np.sin(tt)))[:, None], (1, phi.size))
    YY = a * (1 - np.cos(tt))[:, None] * np.cos(phi)
    ZZ = a * (1 - np.cos(tt))[:, None] * np.sin(phi)
    ax3.plot_surface(XX, YY, ZZ, color=ORANGE, alpha=0.6, linewidth=0)
    ax3.plot(x, y, np.zeros_like(x), color=RED, lw=2.0)
    ax3.set_xlim(0, 2 * np.pi); ax3.set_ylim(-2.2, 2.2); ax3.set_zlim(-2.2, 2.2)
    ax3.set_xticks([]); ax3.set_yticks([]); ax3.set_zticks([])
    ax3.view_init(elev=16, azim=-50)
    ax3.set_title("绕 $x$ 轴旋转：$V=5\\pi^{2}a^{3}$（$a=1$ 时 $\\approx49.3$）",
                  fontsize=12.5, color=INK, pad=2)

    fig.tight_layout()
    fig.savefig(BASE + "ex-cycloid-arc-vol.png", dpi=170)
    plt.close(fig)
    print("ok ex-cycloid-arc-vol.png")


if __name__ == "__main__":
    main()
