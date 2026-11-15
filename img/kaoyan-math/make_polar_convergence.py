"""极坐标面积：小扇形拼图随 N 增大逼近真实区域的对比图。"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import os

plt.rcParams["font.family"] = ["PingFang SC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
BASE = os.path.dirname(os.path.abspath(__file__)) + "/"
INK, BLUE, ORANGE = "#2b2b2b", "#2f4f6f", "#d2691e"


def main():
    r = lambda t: 1.0 + 0.5 * np.sin(t)      # 心形线示例曲线
    th = np.linspace(0, 2 * np.pi, 800)
    rr = r(th)
    fig, axes = plt.subplots(1, 3, figsize=(13.5, 4.8), dpi=170)
    S_true = 0.5 * np.trapezoid(rr ** 2, th)
    for ax, N in zip(axes, [4, 8, 24]):
        dth = 2 * np.pi / N
        for i in range(N):
            t0 = i * dth
            t1 = t0 + dth
            ri = r(0.5 * (t0 + t1))
            seg = np.linspace(t0, t1, 30)
            ax.fill(np.concatenate([[0], ri * np.cos(seg), [0]]),
                    np.concatenate([[0], ri * np.sin(seg), [0]]),
                    color=ORANGE, alpha=0.5, edgecolor=ORANGE, lw=0.7)
        ax.plot(rr * np.cos(th), rr * np.sin(th), color=BLUE, lw=2.0)
        ax.plot([0], [0], "o", color=INK, ms=4)
        ax.set_xlim(-1.9, 1.9); ax.set_ylim(-1.6, 2.1)
        ax.set_aspect("equal")
        ax.set_xticks([]); ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_color("#d8dde3")
        ax.set_title("$N=%d$：扇形拼图与蓝线贴合" % N, fontsize=12, color=INK)
    fig.suptitle("极坐标面积：把角度切成 $N$ 份，小扇形拼出的区域随 $N$ 增大逼近真实面积"
                 "（$S=\\frac{3\\pi}{2}\\approx%.3f$）" % S_true,
                 fontsize=13, color=INK, y=0.99)
    fig.tight_layout(rect=(0, 0, 1, 0.94))
    fig.savefig(BASE + "pc-area-convergence.png", dpi=170)
    plt.close(fig)
    print("ok pc-area-convergence.png")


if __name__ == "__main__":
    main()
