import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.family"] = ["PingFang SC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

INK, ORANGE, BLUE, RED, GREY = "#2b2b2b", "#d2691e", "#2f4f6f", "#b03a2e", "#8a8a8a"
BASE = "/Users/fred/Documents/GitHub/cycleuser/blog/output/img/kaoyan-math/"
F = 11.0

def cart(ax, lim, title, note=""):
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)
    ax.set_aspect("equal")
    ax.grid(True, color="#e6e6e6", lw=0.8)
    ax.axhline(0, color="#c8c8c8", lw=1.0, zorder=2)
    ax.axvline(0, color="#c8c8c8", lw=1.0, zorder=2)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_color("#cccccc")
    ax.set_title(title, fontsize=11.0, color=INK, pad=6)
    if note:
        ax.text(0.03, 0.04, note, transform=ax.transAxes, fontsize=F - 3,
                color=INK, va="bottom",
                bbox=dict(boxstyle="round,pad=0.2", facecolor="white", edgecolor="none", alpha=0.85))

fig, axes = plt.subplots(2, 4, figsize=(15.4, 7.6), dpi=140)
th = np.linspace(0, 2 * np.pi, 1500)

# 1 圆 r=a
ax = axes[0][0]
cart(ax, 1.9, "圆 $r=a$", "$x^{2}+y^{2}=a^{2}$")
ax.plot(np.cos(th), np.sin(th), color=BLUE, lw=2.6, zorder=3)

# 2 过极点的圆
ax = axes[0][1]
cart(ax, 2.25, "过极点的圆 $r=2a\\cos\\theta$", "$(x-a)^{2}+y^{2}=a^{2}$")
ax.plot(1 + np.cos(th), np.sin(th), color=BLUE, lw=2.6, zorder=3)

# 3 直线 r=secθ
ax = axes[0][2]
cart(ax, 1.9, "直线 $r=\\sec\\theta$", "$x=1$")
ax.plot([1, 1], [-1.85, 1.85], color=ORANGE, lw=2.6, zorder=3)

# 4 心形线
ax = axes[0][3]
cart(ax, 2.25, "心形线 $r=a(1+\\cos\\theta)$", "$\\left(x^{2}+y^{2}-ax\\right)^{2}=a^{2}\\left(x^{2}+y^{2}\\right)$")
r = 1 + np.cos(th)
ax.plot(r * np.cos(th), r * np.sin(th), color=BLUE, lw=2.6, zorder=3)

# 5 双纽线
ax = axes[1][0]
cart(ax, 1.9, "双纽线 $r^{2}=a^{2}\\cos 2\\theta$", "$\\left(x^{2}+y^{2}\\right)^{2}=a^{2}\\left(x^{2}-y^{2}\\right)$")
m = np.cos(2 * th) >= 0
rr = np.sqrt(np.cos(2 * th[m]))
tm = th[m]
ax.plot(rr * np.cos(tm), rr * np.sin(tm), color=BLUE, lw=2.6, zorder=3)
ax.plot(rr * np.cos(tm + np.pi), rr * np.sin(tm + np.pi), color=BLUE, lw=2.6, zorder=3)

# 6 玫瑰线
ax = axes[1][1]
cart(ax, 1.9, "玫瑰线 $r=a\\sin 3\\theta$", "$\\left(x^{2}+y^{2}\\right)^{2}=ay\\left(3x^{2}-y^{2}\\right)$")
r = np.sin(3 * th)
ax.plot(r * np.cos(th), r * np.sin(th), color=BLUE, lw=2.6, zorder=3)

# 7 阿基米德螺线
ax = axes[1][2]
cart(ax, 1.9, "阿基米德螺线 $r=a\\theta$", "没有 $y=f(x)$ 这样的显式式")
tt = np.linspace(0, 2.75 * np.pi, 900)
ax.plot(0.24 * tt * np.cos(tt), 0.24 * tt * np.sin(tt), color=BLUE, lw=2.2, zorder=3)

# 8 对数螺线
ax = axes[1][3]
cart(ax, 1.9, "对数螺线 $r=e^{a\\theta}$", "没有 $y=f(x)$ 这样的显式式")
tt = np.linspace(-2.2 * np.pi, 1.6 * np.pi, 900)
rr = np.exp(0.16 * tt)
ax.plot(rr * np.cos(tt), rr * np.sin(tt), color=BLUE, lw=2.2, zorder=3)

fig.suptitle("同一批曲线放进直角坐标系：能写成 $x,y$ 的方程的，就写成方程", fontsize=14, color=INK)
fig.subplots_adjust(left=0.01, right=0.99, top=0.88, bottom=0.02, wspace=0.06, hspace=0.20)
fig.savefig(BASE + "pc-cartesian.png", dpi=140); plt.close(fig)
print("ok")
