"""弧长与旋转体积的三张动画（参数方程一节用）。

- ga-ds-element.gif     一小段弧放大成直角三角形
- ga-ds-accumulate.gif  t 从 0 走到 2π，已画弧长实时累加
- ga-volume-sweep-3d.gif 圆盘沿 x 轴扫过一摆线，体积层层累加（3D）
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import os

plt.rcParams["font.family"] = ["PingFang SC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
BASE = os.path.dirname(os.path.abspath(__file__)) + "/"
INK, ORANGE, BLUE = "#2b2b2b", "#d2691e", "#2f4f6f"
RED, GREEN, GREY, BROWN = "#b03a2e", "#4a7c59", "#8a8a8a", "#7a5230"


def save_gif(frames, name, dur=450):
    pal = [f.convert("P", palette=Image.ADAPTIVE) for f in frames]
    pal[0].save(BASE + name, save_all=True, append_images=pal[1:], duration=dur,
                loop=0, optimize=True)
    print("ok", name, len(frames))


def grab(fig):
    fig.canvas.draw()
    img = Image.fromarray(np.asarray(fig.canvas.buffer_rgba())[:, :, :3])
    plt.close(fig)
    return img


def cycloid(t, a=1.0):
    return a * (t - np.sin(t)), a * (1 - np.cos(t))


def ds_element():
    a = 1.0
    tt = np.linspace(0, 2 * np.pi, 600)
    xs, ys = cycloid(tt, a)
    frames = []
    for k in range(18):
        width = 0.12 + 1.3 * k / 17
        t0 = 3.2
        seg = np.linspace(t0, t0 + width, 40)
        px, py = cycloid(seg, a)
        fig, ax = plt.subplots(figsize=(6.4, 4.2), dpi=100)
        ax.plot(xs, ys, color=BLUE, lw=1.8, alpha=0.55)
        ax.plot(px, py, color=RED, lw=3.4, solid_capstyle="round")
        dx, dy = px[-1] - px[0], py[-1] - py[0]
        ox, oy = px[0], py[0] - 0.35
        ax.plot([ox, ox + dx], [oy, oy], color=GREEN, lw=2.0)
        ax.plot([ox + dx, ox + dx], [oy, oy + dy], color=ORANGE, lw=2.0)
        ax.plot([ox, ox + dx], [oy, oy + dy], color=RED, lw=2.0)
        ax.text(ox + dx / 2, oy - 0.18, r"$\mathrm{d}x$", color=GREEN,
                fontsize=11, ha="center")
        ax.text(ox + dx + 0.1, oy + dy / 2, r"$\mathrm{d}y$", color=ORANGE, fontsize=11)
        ax.text(ox - 0.42, oy + dy / 2, r"$\mathrm{d}s$", color=RED, fontsize=12)
        ax.set_xlim(-0.3, 6.6); ax.set_ylim(-0.9, 2.5)
        ax.set_aspect("equal")
        ax.set_xticks([]); ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_color("#d8dde3")
        ax.set_title("弧长元素：一小段弧 ≈ 直角三角形斜边", fontsize=12, color=INK)
        fig.tight_layout()
        frames.append(grab(fig))
    save_gif(frames, "ga-ds-element.gif", dur=380)


def ds_accumulate():
    a = 1.0
    tt = np.linspace(0, 2 * np.pi, 800)
    xs, ys = cycloid(tt, a)
    speed = np.hypot(np.gradient(xs, tt), np.gradient(ys, tt))
    cum = np.concatenate([[0], np.cumsum((speed[1:] + speed[:-1]) / 2 * np.diff(tt))])
    frames = []
    for k in range(26):
        t_end = 2 * np.pi * k / 25
        idx = tt <= t_end
        fig, ax = plt.subplots(figsize=(6.4, 4.2), dpi=100)
        ax.plot(xs, ys, color=BLUE, lw=1.6, alpha=0.35)
        ax.plot(xs[idx], ys[idx], color=RED, lw=3.0)
        ax.text(0.2, 2.25, "已累加弧长 $L=%.3f$" % cum[idx][-1] if idx.any() else "",
                fontsize=12, color=RED)
        ax.set_xlim(-0.3, 6.6); ax.set_ylim(-0.7, 2.5)
        ax.set_aspect("equal")
        ax.set_xticks([]); ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_color("#d8dde3")
        ax.set_title("弧长累加：$t$ 走到 %.2f" % t_end, fontsize=12, color=INK)
        fig.tight_layout()
        frames.append(grab(fig))
    save_gif(frames, "ga-ds-accumulate.gif", dur=420)


def volume_3d():
    a = 1.0
    frames = []
    for k in range(24):
        t_end = 0.05 + (2 * np.pi - 0.1) * k / 23
        tt = np.linspace(0.001, t_end, 60)
        cx, cy = cycloid(tt, a)
        phi = np.linspace(0, 2 * np.pi, 40)
        XX = np.tile(cx[:, None], (1, phi.size))
        YY = cy[:, None] * np.cos(phi)[None, :]
        ZZ = cy[:, None] * np.sin(phi)[None, :]

        fig = plt.figure(figsize=(6.6, 5.0), dpi=100)
        ax = fig.add_subplot(111, projection="3d")
        ax.plot_surface(XX, YY, ZZ, color=ORANGE, alpha=0.55, linewidth=0)
        # 当前截面圆盘
        x0, y0 = cycloid(np.array([t_end]), a)[0][0], cycloid(np.array([t_end]), a)[1][0]
        ax.plot(np.full_like(phi, x0), y0 * np.cos(phi), y0 * np.sin(phi),
                color=BROWN, lw=2.0)
        ax.plot(cx, cy, np.zeros_like(cx), color=RED, lw=1.6)
        ax.set_xlim(0, 2 * np.pi); ax.set_ylim(-2.2, 2.2); ax.set_zlim(-2.2, 2.2)
        ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
        ax.view_init(elev=18, azim=-52)
        ax.set_title("绕 $x$ 轴旋转：圆盘扫过一拱，$t=%.2f$" % t_end, fontsize=11.5, color=INK)
        fig.tight_layout()
        frames.append(grab(fig))
    save_gif(frames, "ga-volume-sweep-3d.gif", dur=450)


if __name__ == "__main__":
    ds_element()
    ds_accumulate()
    volume_3d()
