import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Polygon, Ellipse
import os

plt.rcParams["font.family"] = ["PingFang SC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
INK, ORANGE, BLUE = "#2b2b2b", "#d2691e", "#2f4f6f"
RED, GREEN, GREY, BROWN, CREAM = "#b03a2e", "#4a7c59", "#8a8a8a", "#7a5230", "#e8ddd0"
BASE = "/Users/fred/Documents/GitHub/cycleuser/blog/output/img/kaoyan-math/"
F, T = 11.5, 12.0

a = 1.0
t_all = np.linspace(0, 2*np.pi, 800)
X = a*(t_all - np.sin(t_all))
Y = a*(1 - np.cos(t_all))

fig, axes = plt.subplots(1, 3, figsize=(15.6, 5.0), dpi=170)

# 左：弧长元素 ds —— 一小段弧放大
ax = axes[0]
ax.set_xlim(-0.5, 7.0); ax.set_ylim(-0.7, 2.6)
ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
for sp_ in ax.spines.values():
    sp_.set_color("#cccccc")
ax.axhline(0, color="#c9a887", lw=1.2)
ax.plot(X, Y, color=BLUE, lw=2.0)
# 取 t0 处一段弧
t0 = np.pi/2.5
t1 = t0 + 0.75
seg = np.linspace(t0, t1, 30)
xs = a*(seg - np.sin(seg)); ys = a*(1 - np.cos(seg))
ax.plot(xs, ys, color=RED, lw=3.4, zorder=6)
ax.annotate("$\\mathrm{d}s$（一小段弧，近似直的）", xy=((xs[0]+xs[-1])/2, (ys[0]+ys[-1])/2 + 0.03),
            xytext=(0.15, 2.35), fontsize=F-1.5, color=RED,
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.0))
# 放大三角形：dx 水平、dy 竖直，斜边近似弧
P0 = np.array([xs[0], ys[0]]); P1 = np.array([xs[-1], ys[-1]])
dx, dy = P1 - P0
sc = 1.15
ax.plot([P0[0]*0.5, P0[0]*0.5 + 0.0], [0,0])
tri0 = (4.55, 0.72)
ax.plot([tri0[0], tri0[0]+sc*dx], [tri0[1], tri0[1]], color=GREEN, lw=2.6)
ax.plot([tri0[0]+sc*dx, tri0[0]+sc*dx], [tri0[1], tri0[1]+sc*dy], color=ORANGE, lw=2.6)
ax.plot([tri0[0], tri0[0]+sc*dx], [tri0[1], tri0[1]+sc*dy], color=RED, lw=2.6)
ax.text(tri0[0]+sc*dx/2, tri0[1]-0.24, "$\\mathrm{d}x=x'(t)\\mathrm{d}t$", fontsize=F-2, color=GREEN, ha="center")
ax.text(tri0[0]+sc*dx+0.12, tri0[1]+sc*dy/2, "$\\mathrm{d}y=y'(t)\\mathrm{d}t$", fontsize=F-2, color=ORANGE)
ax.text(tri0[0]-0.12, tri0[1]+sc*dy/2+0.10, "$\\mathrm{d}s$", fontsize=F-1, color=RED)
ax.text(tri0[0]-0.30, tri0[1]-0.42, "放大看：", fontsize=F-2.5, color=GREY)
ax.set_title("弧长元素：一小段弧 ≈ 直角三角形斜边\n勾股定理 $\\mathrm{d}s=\\sqrt{\\mathrm{d}x^{2}+\\mathrm{d}y^{2}}$",
             fontsize=T-1.2, color=INK, pad=8)

# 中：弧长是一段一段 ds 加起来的
ax = axes[1]
ax.set_xlim(-0.5, 7.0); ax.set_ylim(-0.7, 2.6)
ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
for sp_ in ax.spines.values():
    sp_.set_color("#cccccc")
ax.axhline(0, color="#c9a887", lw=1.2)
ax.plot(X, Y, color=BLUE, lw=2.0, alpha=0.85)
# 分段染色（用红-青交替太花，用同色深浅）：
segs = 10
cmap = plt.cm.Oranges
for i in range(segs):
    ta = 2*np.pi*i/segs; tb = 2*np.pi*(i+1)/segs
    sg = np.linspace(ta, tb, 20)
    xs = a*(sg-np.sin(sg)); ys = a*(1-np.cos(sg))
    ax.plot(xs, ys, color=cmap(0.35 + 0.5*i/segs), lw=4.2, solid_capstyle="round")
ax.annotate("$L=\\int\\mathrm{d}s$：把每小段加起来", xy=(X[400], Y[400]+0.06),
            xytext=(3.2, 2.35), fontsize=F-1.5, color=INK,
            arrowprops=dict(arrowstyle="->", color=INK, lw=1.0))
ax.text(0.1, -0.55, "$t$ 从 $0$ 走到 $2\\pi$，一拱", fontsize=F-2.5, color=GREY)
ax.set_title("弧长 = 每小段 $\\mathrm{d}s$ 累加\n$\\mathrm{d}s=\\sqrt{x'(t)^{2}+y'(t)^{2}}\\,\\mathrm{d}t$",
             fontsize=T-1.2, color=INK, pad=8)

# 右：绕 x 轴旋转的体积
ax = axes[2]
ax.set_xlim(-0.4, 6.9); ax.set_ylim(-2.6, 2.6)
ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
for sp_ in ax.spines.values():
    sp_.set_color("#cccccc")
ax.axhline(0, color="#c9a887", lw=1.2)
# 旋转体的轮廓：以某 t0 为截面画一个椭圆表示"圆盘"
# 先画整个旋转体轮廓（上下对称的 y 和 -y）
T3 = np.linspace(0, 2*np.pi, 400)
X3 = a*(T3-np.sin(T3)); Y3 = a*(1-np.cos(T3))
ax.fill_between(X3, Y3, -Y3, color=CREAM, alpha=0.75, zorder=1)
ax.plot(X3, Y3, color=BLUE, lw=2.0)
ax.plot(X3, -Y3, color=BLUE, lw=2.0, alpha=0.55)
# 某个 t0 处的截面圆盘（椭圆表示）
t0 = 2.4
x0 = a*(t0-np.sin(t0)); y0 = a*(1-np.cos(t0))
ell = Ellipse((x0, 0), width=0.34, height=2*y0, facecolor=ORANGE, alpha=0.65, edgecolor=BROWN, lw=1.4, zorder=5)
ax.add_patch(ell)
ax.plot([x0], [y0], "o", color=RED, ms=5, zorder=6)
ax.annotate("截面半径 $y(t)$", xy=(x0, y0*0.5), xytext=(3.6, 2.1),
            fontsize=F-1.5, color=BROWN, arrowprops=dict(arrowstyle="->", color=BROWN, lw=1.0))
ax.text(x0+0.12, 0.10, "$\\mathrm{d}V=\\pi y^{2}\\,\mathrm{d}x$", fontsize=F-1.5, color=BROWN)
ax.text(0.1, -2.28, "每个截面是一个圆盘，沿 $x$ 方向积累 $\\mathrm{d}V=\\pi y^{2}\\,\\mathrm{d}x$",
        fontsize=F-2.5, color=GREY)
ax.set_title("绕 $x$ 轴旋转：一拱转成橄榄状旋转体，\n体积由一层层圆盘 $\\mathrm{d}V=\\pi y^{2}\\,\\mathrm{d}x$ 累加",
             fontsize=T-1.2, color=INK, pad=8)

fig.tight_layout()
fig.savefig(BASE + "ex-cycloid-3panel.png", dpi=170)
plt.close(fig)
print("ok 3panel")
