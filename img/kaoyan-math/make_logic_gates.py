import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Polygon
from matplotlib.path import Path
import matplotlib.patches as mpatches
import os

plt.rcParams["font.family"] = ["PingFang SC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
INK, BLUE, RED, GREY = "#2b2b2b", "#2f4f6f", "#b03a2e", "#8a8a8a"
BASE = "/Users/fred/Documents/GitHub/cycleuser/blog/output/img/kaoyan-math/"
F = 15.0
LW = 3.0

def shape_and(ax, x, y, w=2.8, h=2.0):
    """闭合 D 形：左边直线、右上右下直线、右侧半圆"""
    t = np.linspace(-np.pi/2, np.pi/2, 120)
    arc_x = x + w*0.58 + (w*0.42)*np.cos(t)
    arc_y = y + h/2 + (h/2)*np.sin(t)
    xs = [x, x] + list(arc_x) + [x]
    ys = [y, y+h] + list(arc_y) + [y]
    # 注意：从底部起始
    xs = [x, x + w*0.58] + list(arc_x) + [x + w*0.58, x, x]
    ys = [y, y] + list(arc_y[::-1]) + [y+h, y+h, y]
    # 用 path 绘制：底边 → 右下弧 → 顶边 → 左边
    verts = [(x, y), (x + w*0.58, y)]
    codes = [Path.MOVETO, Path.LINETO]
    tt = np.linspace(-np.pi/2, np.pi/2, 120)
    for a, b in zip(x + w*0.58 + (w*0.42)*np.cos(tt), y + h/2 + (h/2)*np.sin(tt)):
        verts.append((a, b)); codes.append(Path.LINETO)
    verts += [(x + w*0.58, y + h), (x, y + h), (x, y)]
    codes += [Path.LINETO, Path.LINETO, Path.CLOSEPOLY]
    ax.add_patch(mpatches.PathPatch(Path(verts, codes), fill=False, edgecolor=BLUE, lw=LW,
                                    joinstyle="miter", capstyle="butt", zorder=4))

def shape_or(ax, x, y, w=3.0, h=2.0, xor=False):
    """后弧 + 上下弧收成尖"""
    t = np.linspace(-1, 1, 160)
    back_x = x + 0.55*(1 - t**2)
    back_y = y + h/2 + (h/2)*t
    if xor:
        back2_x = x - 0.30 + 0.55*(1 - t**2)
        ax.plot(back2_x, back_y, color=BLUE, lw=LW, solid_capstyle="butt")
    ax.plot(back_x, back_y, color=BLUE, lw=LW, solid_capstyle="butt")
    s = np.linspace(0, 1, 160)
    top_x = x + 0.55 + (w - 0.55)*s
    top_y = y + h - (h/2)*(s**1.75)
    bot_y = y + (h/2)*(s**1.75)
    ax.plot(top_x, top_y, color=BLUE, lw=LW, solid_capstyle="butt")
    ax.plot(top_x, bot_y, color=BLUE, lw=LW, solid_capstyle="butt")

def shape_not(ax, x, y, w=1.8, h=1.9):
    ax.add_patch(Polygon([(x, y+h/2+0.5), (x, y+h/2-0.5), (x+w, y+h/2)],
                         closed=True, fill=False, edgecolor=BLUE, lw=LW, joinstyle="miter"))
    ax.add_patch(Circle((x+w+0.17, y+h/2), 0.17, fill=False, edgecolor=BLUE, lw=LW-0.3, zorder=5))

def hw(ax, a, b, y, lw=2.6):
    ax.plot([a, b], [y, y], color=INK, lw=lw, solid_capstyle="butt")

def T(ax, x, y, s, color=INK, size=F, ha="center", va="center"):
    ax.text(x, y, s, fontsize=size, color=color, ha=ha, va=va)

# ================= 2x2 =================
fig, axes = plt.subplots(2, 2, figsize=(12.6, 8.4), dpi=170)
for ax in axes.ravel():
    ax.set_xlim(0.1, 7.3); ax.set_ylim(1.0, 6.1); ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    for sp_ in ax.spines.values(): sp_.set_color("none")

# --- 与门 ---
ax = axes[0][0]
shape_and(ax, 2.35, 2.9)
hw(ax, 0.85, 2.35, 4.15); hw(ax, 0.85, 2.35, 3.65)
hw(ax, 2.35+2.8*0.98, 2.35+2.8+0.75, 3.9)
T(ax, 0.5, 4.15, "A"); T(ax, 0.5, 3.65, "B")
T(ax, 2.35+2.8+1.15, 3.9, "A·B", color=RED, ha="left")
T(ax, 3.7, 5.55, "与门  AND", size=F+2)
T(ax, 3.7, 1.75, "1·1=1   1·0=0\n0·1=0   0·0=0", size=F-3, color=GREY)

# --- 或门 ---
ax = axes[0][1]
shape_or(ax, 2.0, 2.9)
hw(ax, 0.55, 2.20, 4.18); hw(ax, 0.55, 2.20, 3.60)
hw(ax, 2.0+3.0, 2.0+3.0+0.75, 3.9)
T(ax, 0.2, 4.18, "A"); T(ax, 0.2, 3.60, "B")
T(ax, 2.0+3.0+1.15, 3.9, "A+B", color=RED, ha="left")
T(ax, 3.7, 5.55, "或门  OR", size=F+2)
T(ax, 3.7, 1.75, "1+1=1   1+0=1\n0+1=1   0+0=0", size=F-3, color=GREY)

# --- 非门 ---
ax = axes[1][0]
shape_not(ax, 2.45, 2.85)
hw(ax, 1.05, 2.45, 3.8); hw(ax, 2.45+1.8+0.34, 2.45+1.8+1.05, 3.8)
T(ax, 0.7, 3.8, "A")
T(ax, 2.45+1.8+1.45, 3.8, "Ā", color=RED, ha="left")
T(ax, 3.7, 5.55, "非门  NOT", size=F+2)
T(ax, 3.7, 1.75, "0 → 1\n1 → 0", size=F-3, color=GREY)

# --- 异或门 ---
ax = axes[1][1]
shape_or(ax, 2.3, 2.9, xor=True)
hw(ax, 0.85, 2.48, 4.18); hw(ax, 0.85, 2.48, 3.60)
hw(ax, 2.3+3.0, 2.3+3.0+0.75, 3.9)
T(ax, 0.5, 4.18, "A"); T(ax, 0.5, 3.60, "B")
T(ax, 2.3+3.0+1.15, 3.9, "A⊕B", color=RED, ha="left")
T(ax, 3.9, 5.55, "异或门  XOR", size=F+2)
T(ax, 3.9, 1.75, "1⊕1=0   1⊕0=1\n0⊕1=1   0⊕0=0", size=F-3, color=GREY)

fig.subplots_adjust(left=0.01, right=0.99, top=0.99, bottom=0.01, wspace=0.02, hspace=0.04)
fig.savefig(BASE + "logic-gates.png", dpi=170)
print("ok gates v3")
