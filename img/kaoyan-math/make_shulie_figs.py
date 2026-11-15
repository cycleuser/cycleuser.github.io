"""数列极限的两张示意图：ε-N 定义、单调有界准则。"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import os

plt.rcParams["font.family"] = ["PingFang SC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
BASE = os.path.dirname(os.path.abspath(__file__)) + "/"
INK, CURVE, BAND = "#2b2b2b", "#1f2d5a", "#dbe4f3"


def epsilon_n():
    fig, ax = plt.subplots(figsize=(9.6, 5.1), dpi=100)
    n = np.arange(1, 17)
    a = 1 + (-1) ** n * 0.62 / n ** 0.85
    ax.axhspan(0.78, 1.22, color=BAND, zorder=0)
    ax.axhline(1.0, color=CURVE, lw=1.2, ls="--")
    ax.vlines(n, 1.0, a, color="#c9d3e2", lw=1.0, zorder=1)
    ax.plot(n, a, "o", color=CURVE, ms=7, zorder=3)
    ax.axvline(4.4, color="#c0504d", lw=1.4, ls=":")
    ax.text(4.6, 0.27, "$N$", fontsize=15, color="#c0504d")
    ax.text(0.6, 1.245, "A + ε", fontsize=12, color=INK)
    ax.text(0.6, 0.715, "A − ε", fontsize=12, color=INK)
    ax.text(17, 1.0, "$A$", fontsize=13, color=CURVE, va="center")
    ax.text(8.6, 1.62, "从第 $N$ 项起，所有点都落进带内", fontsize=13, color=INK)
    ax.set_xlim(0, 17.6); ax.set_ylim(0.2, 1.8)
    ax.set_xlabel("$n$", fontsize=12)
    ax.set_ylabel("$a_n$", fontsize=12)
    ax.set_xticks([2, 4, 6, 8, 10, 12, 14, 16])
    ax.set_yticks([0.2, 0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8])
    ax.tick_params(colors="#8a8a8a")
    for sp in ax.spines.values():
        sp.set_color("#d8dde3")
    fig.tight_layout()
    fig.savefig(BASE + "shulie-epsilon-n.png", dpi=100)
    plt.close(fig)
    print("ok shulie-epsilon-n.png")


def monotone():
    fig, ax = plt.subplots(figsize=(9.6, 5.1), dpi=100)
    n = np.arange(1, 18)
    a = 2 - 1.2 / n ** 0.8
    ax.plot(n, a, "o-", color=CURVE, ms=6, lw=1.6)
    ax.axhline(2.0, color="#c0504d", lw=1.4, ls="--")
    ax.text(11, 2.04, "上界 $M=2$", fontsize=12, color="#c0504d")
    ax.annotate("", xy=(6, a[5] + 0.02), xytext=(6, a[5] - 0.18),
                arrowprops=dict(arrowstyle="->", color="#4a7c59", lw=1.4))
    ax.text(4.2, 1.05, "单调增加且有上界 ⇒ 收敛", fontsize=13, color="#4a7c59")
    ax.set_xlim(0, 18); ax.set_ylim(0, 2.3)
    ax.set_xlabel("$n$", fontsize=12)
    ax.set_ylabel("$a_n$", fontsize=12)
    ax.set_xticks([]); ax.set_yticks([0, 0.5, 1.0, 1.5, 2.0])
    ax.tick_params(colors="#8a8a8a")
    for sp in ax.spines.values():
        sp.set_color("#d8dde3")
    fig.tight_layout()
    fig.savefig(BASE + "shulie-monotone.png", dpi=100)
    plt.close(fig)
    print("ok shulie-monotone.png")


if __name__ == "__main__":
    epsilon_n()
    monotone()
