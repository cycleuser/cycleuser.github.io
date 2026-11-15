"""柯西不等式的几何示意：向量点积不超过长度之积。"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import os

plt.rcParams["font.family"] = ["PingFang SC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
BASE = os.path.dirname(os.path.abspath(__file__)) + "/"
INK, A_C, B_C, PROJ = "#2b2b2b", "#1f2d5a", "#c0504d", "#4a7c59"


def main():
    fig, axes = plt.subplots(1, 2, figsize=(9.6, 4.3), dpi=100)

    # 左：两个向量与夹角
    ax = axes[0]
    a = np.array([3.2, 1.0]); b = np.array([1.4, 2.4])
    ax.annotate("", xy=a, xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=A_C, lw=2.2))
    ax.annotate("", xy=b, xytext=(0, 0),
                arrowprops=dict(arrowstyle="-|>", color=B_C, lw=2.2))
    ax.text(a[0] + 0.08, a[1] - 0.18, r"$\vec a$", fontsize=14, color=A_C)
    ax.text(b[0] + 0.08, b[1], r"$\vec b$", fontsize=14, color=B_C)
    # 夹角弧
    t = np.linspace(np.arctan2(a[1], a[0]), np.arctan2(b[1], b[0]), 60)
    ax.plot(0.8 * np.cos(t), 0.8 * np.sin(t), color="#8a8a8a", lw=1.2)
    ax.text(0.95, 0.42, r"$\theta$", fontsize=13, color="#666")
    # 投影
    proj = b * (a @ b) / (b @ b)
    ax.plot([a[0], proj[0]], [a[1], proj[1]], color=PROJ, lw=1.4, ls="--")
    ax.plot([proj[0]], [proj[1]], "o", color=PROJ, ms=6)
    ax.text(proj[0] - 0.55, proj[1] - 0.32, "投影", fontsize=11, color=PROJ)
    ax.set_xlim(-0.4, 3.8); ax.set_ylim(-0.4, 3.0)
    ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_color("#d8dde3")
    ax.set_title(r"$\vec a\cdot\vec b=|\vec a||\vec b|\cos\theta$", fontsize=13, color=INK, pad=8)

    # 右：点积随夹角变化
    ax = axes[1]
    th = np.linspace(0, np.pi, 300)
    ax.plot(th, np.cos(th), color=A_C, lw=2.0)
    ax.axhline(0, color="#c9d3e2", lw=1.0)
    ax.axhline(1, color=B_C, lw=1.2, ls="--")
    ax.axhline(-1, color=B_C, lw=1.2, ls="--")
    ax.text(0.15, 1.05, "上界 $|\\vec a||\\vec b|$", fontsize=11, color=B_C)
    ax.text(0.15, -1.22, "下界 $-|\\vec a||\\vec b|$", fontsize=11, color=B_C)
    ax.set_xticks([0, np.pi / 2, np.pi])
    ax.set_xticklabels(["0", "π/2", "π"], color="#8a8a8a")
    ax.set_yticks([])
    ax.set_xlim(0, np.pi); ax.set_ylim(-1.45, 1.35)
    for sp in ax.spines.values():
        sp.set_color("#d8dde3")
    ax.set_title("夹角越接近 0 或 π，点积越接近界；等号只在共线时成立",
                 fontsize=11.5, color=INK, pad=8)

    fig.tight_layout()
    fig.savefig(BASE + "cauchy-visual.png", dpi=100)
    plt.close(fig)
    print("ok cauchy-visual.png")


if __name__ == "__main__":
    main()
