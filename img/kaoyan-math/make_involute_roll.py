"""圆的渐开线生成过程动画：细线从基圆上绷紧拉开。"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import os

plt.rcParams["font.family"] = ["PingFang SC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
BASE = os.path.dirname(os.path.abspath(__file__)) + "/"
INK, RED, GREEN, BROWN = "#2b2b2b", "#b03a2e", "#4a7c59", "#7a5230"
R = 1.0


def grab(fig):
    fig.canvas.draw()
    img = Image.fromarray(np.asarray(fig.canvas.buffer_rgba())[:, :, :3])
    plt.close(fig)
    return img


def main(frames_n=40):
    t_all = np.linspace(0, 2 * np.pi, 800)
    X = R * (np.cos(t_all) + t_all * np.sin(t_all))
    Y = R * (np.sin(t_all) - t_all * np.cos(t_all))
    th = np.linspace(0, 2 * np.pi, 200)
    frames = []
    for k in range(frames_n):
        t = 2 * np.pi * k / (frames_n - 1)
        fig, ax = plt.subplots(figsize=(6.4, 6.0), dpi=100)
        ax.plot(R * np.cos(th), R * np.sin(th), color="#c9a887", lw=1.6, ls="--")
        idx = t_all <= t + 1e-9
        ax.plot(X[idx], Y[idx], color=RED, lw=2.4)
        P0 = np.array([R * np.cos(t), R * np.sin(t)])
        Tv = np.array([np.sin(t), -np.cos(t)])
        P1 = P0 + t * R * Tv
        ax.plot([P0[0], P1[0]], [P0[1], P1[1]], color=BROWN, lw=2.0)
        ax.plot([P0[0]], [P0[1]], "o", color=GREEN, ms=6)
        ax.plot([P1[0]], [P1[1]], "o", color=RED, ms=7)
        arc = np.linspace(0, t, 60)
        ax.plot(R * 0.95 * np.cos(arc), R * 0.95 * np.sin(arc), color=GREEN, lw=2.2)
        ax.plot([0], [0], "o", color=INK, ms=4)
        ax.text(-7.0, 6.6, "$t=%.2f$" % t, fontsize=11, color=INK)
        ax.set_xlim(-7.6, 7.6); ax.set_ylim(-7.8, 7.6)
        ax.set_aspect("equal")
        ax.set_xticks([]); ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_color("#d8dde3")
        ax.set_title("圆的渐开线：细线从基圆上绷紧拉开（线长 = 弧长 $Rt$）",
                     fontsize=11.5, color=INK, pad=8)
        fig.tight_layout()
        frames.append(grab(fig))
    pal = [f.convert("P", palette=Image.ADAPTIVE) for f in frames]
    pal[0].save(BASE + "geo2-involute-roll.gif", save_all=True, append_images=pal[1:],
                duration=220, loop=0, optimize=True)
    print("ok geo2-involute-roll.gif", len(frames))


if __name__ == "__main__":
    main()
