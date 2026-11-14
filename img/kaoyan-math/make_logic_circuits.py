"""附录7 电路图：异或实现（拆两张）、半加器、全加器、加法器动画"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Polygon, FancyBboxPatch
from matplotlib.path import Path
import matplotlib.patches as mpatches
from PIL import Image
import os

plt.rcParams["font.family"] = ["PingFang SC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
INK, BLUE, RED, GREEN, GREY, ORANGE = "#2b2b2b", "#2f4f6f", "#b03a2e", "#4a7c59", "#8a8a8a", "#d2691e"
BASE = "/Users/fred/Documents/GitHub/cycleuser/blog/output/img/kaoyan-math/"
F = 14.0
LW = 2.8

# ---------------- 门符号 ----------------
def g_and(ax, x, y, w=2.2, h=1.6, color=BLUE, lw=LW):
    t = np.linspace(-np.pi/2, np.pi/2, 100)
    verts = [(x, y), (x + w*0.58, y)]
    codes = [Path.MOVETO, Path.LINETO]
    for a, b in zip(x + w*0.58 + (w*0.42)*np.cos(t), y + h/2 + (h/2)*np.sin(t)):
        verts.append((a, b)); codes.append(Path.LINETO)
    verts += [(x + w*0.58, y + h), (x, y + h), (x, y)]
    codes += [Path.LINETO, Path.LINETO, Path.CLOSEPOLY]
    ax.add_patch(mpatches.PathPatch(Path(verts, codes), fill=False, edgecolor=color,
                                    lw=lw, joinstyle="miter", capstyle="butt", zorder=5))
    return x + w, y + h/2

def g_or(ax, x, y, w=2.3, h=1.6, color=BLUE, lw=LW, xor=False):
    t = np.linspace(-1, 1, 140)
    ax.plot(x + 0.42*(1 - t**2), y + h/2 + (h/2)*t, color=color, lw=lw, zorder=5)
    if xor:
        ax.plot(x - 0.24 + 0.42*(1 - t**2), y + h/2 + (h/2)*t, color=color, lw=lw, zorder=5)
    s = np.linspace(0, 1, 140)
    xt = x + 0.42 + (w - 0.42)*s
    ax.plot(xt, y + h - (h/2)*(s**1.75), color=color, lw=lw, zorder=5)
    ax.plot(xt, y + (h/2)*(s**1.75), color=color, lw=lw, zorder=5)
    return x + w, y + h/2

def g_not(ax, x, y, w=1.3, h=1.3, color=BLUE, lw=LW):
    ax.add_patch(Polygon([(x, y+h/2+0.34), (x, y+h/2-0.34), (x+w, y+h/2)],
                         closed=True, fill=False, edgecolor=color, lw=lw, joinstyle="miter", zorder=5))
    ax.add_patch(Circle((x+w+0.13, y+h/2), 0.13, fill=False, edgecolor=color, lw=lw-0.3, zorder=5))
    return x + w + 0.26, y + h/2

def wire(ax, pts, lw=2.4, color=INK):
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    ax.plot(xs, ys, color=color, lw=lw, solid_capstyle="round", zorder=3)

def dot(ax, x, y):
    ax.plot([x], [y], "o", color=INK, ms=7, zorder=6)

def T(ax, x, y, s, size=F, color=INK, ha="center", va="center"):
    ax.text(x, y, s, fontsize=size, color=color, ha=ha, va=va, zorder=7)

def new_ax(w, h, xlim, ylim):
    fig, ax = plt.subplots(figsize=(w, h), dpi=170)
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values(): sp.set_color("none")
    return fig, ax

# =========================================================
# 图 A：异或的实现
# =========================================================
fig, ax = new_ax(10.6, 6.2, (0, 16.4), (0, 9.4))

def lead_not(ax, x, y, label, size=F):
    """一条带非门的输入引线：标签 → 线 → 非门 → 线"""
    T(ax, x - 0.30, y, label, size=size, ha="right")
    wire(ax, [(x, y), (x + 0.55, y)])
    o, yy = g_not(ax, x + 0.55, y - 0.55, w=1.0, h=1.1)
    wire(ax, [(o, y), (x + 3.2, y)])

def lead_plain(ax, x, y, label, size=F):
    T(ax, x - 0.30, y, label, size=size, ha="right")
    wire(ax, [(x, y), (x + 3.2, y)])

# 与门 1（上）：Ā · B
g1x, g1y, g1w, g1h = 6.4, 5.55, 2.4, 2.1
lead_not(ax, 3.05, 7.20, "$A$")
lead_plain(ax, 3.05, 6.30, "$B$")
o1, y1 = g_and(ax, g1x, g1y, w=g1w, h=g1h)
T(ax, g1x + 1.15, g1y + g1h + 0.55, "$\\overline{A}\\cdot B$", size=F, color=GREY)

# 与门 2（下）：A · B̄
g2y = 2.10
lead_plain(ax, 3.05, 3.75, "$A$")
lead_not(ax, 3.05, 2.85, "$B$")
o2, y2 = g_and(ax, g1x, g2y, w=g1w, h=g1h)
T(ax, g1x + 1.15, g2y + g1h + 0.55, "$A\\cdot\\overline{B}$", size=F, color=GREY)

# 汇到或门
wire(ax, [(o1, y1), (11.4, y1), (11.4, 5.55), (11.8, 5.55)])
wire(ax, [(o2, y2), (11.4, y2), (11.4, 4.35), (11.8, 4.35)])
oR, yR = g_or(ax, 11.8, 4.05, w=2.5, h=1.8)
wire(ax, [(oR, yR), (15.2, yR)])
T(ax, 15.2, yR, "$A\\oplus B$", size=F+2, color=RED, ha="left")
T(ax, 8.0, 9.0, "$A\\oplus B=(\\overline{A}\\cdot B)+(A\\cdot\\overline{B})$", size=F+1)
fig.subplots_adjust(0.01, 0.01, 0.99, 0.99)
fig.savefig(BASE + "logic-xor-impl.png", dpi=170); plt.close(fig)
print("ok xor impl")

# =========================================================
# 图 B：半加器
# =========================================================
fig, ax = new_ax(9.4, 5.6, (0, 15.4), (0.8, 9.2))

T(ax, 0.55, 6.60, "$A$", size=F+2, ha="left")
T(ax, 0.55, 2.20, "$B$", size=F+2, ha="left")

# A 干线：→ 异或上输入；并下引到与门上输入
wire(ax, [(1.05, 6.60), (4.35, 6.60)])
wire(ax, [(1.05, 6.60), (1.05, 4.10), (5.15, 4.10)])
# B 干线：→ 与门下输入；并上引到异或下输入
wire(ax, [(1.05, 2.20), (4.70, 2.20)])
wire(ax, [(1.55, 2.20), (1.55, 5.60), (4.35, 5.60)])
dot(ax, 1.55, 2.20)
wire(ax, [(4.70, 2.20), (4.70, 3.00), (5.15, 3.00)])

# 异或门
oX, yX = g_or(ax, 4.30, 4.95, w=2.6, h=2.3, xor=True)
wire(ax, [(oX, yX), (12.6, yX)])
T(ax, 12.75, yX, "$S=A\\oplus B$", size=F+1, color=RED, ha="left")

# 与门
oA, yA2 = g_and(ax, 5.15, 2.55, w=2.3, h=1.9)
wire(ax, [(oA, yA2), (12.6, yA2)])
T(ax, 12.75, yA2, "$C=A\\cdot B$", size=F+1, color=RED, ha="left")

T(ax, 7.3, 8.75, "半加器：异或门给和 S，与门给进位 C", size=F-1)
fig.subplots_adjust(0.01, 0.01, 0.99, 0.99)
fig.savefig(BASE + "logic-halfadder.png", dpi=170); plt.close(fig)
print("ok half adder")

# =========================================================
# 图 C：全加器（两个半加器 + 或门）
# =========================================================
fig, ax = new_ax(10.8, 4.9, (0, 17.6), (0, 7.9))

def box(ax, x, y, w, h, label, sub=None, color=BLUE):
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.10",
                                facecolor="#f2f5f9", edgecolor=color, lw=2.4, zorder=3))
    T(ax, x + w/2, y + h/2 + (0.25 if sub else 0), label, size=F-1, color=color)
    if sub:
        T(ax, x + w/2, y + h/2 - 0.45, sub, size=F-4, color=GREY)

box(ax, 2.3, 4.00, 3.6, 2.90, "半加器 1", "异或门 + 与门")
box(ax, 8.3, 2.35, 3.6, 2.90, "半加器 2", "异或门 + 与门")

# 输入
T(ax, 0.45, 6.30, "$A$", size=F+1, ha="left")
T(ax, 0.45, 4.55, "$B$", size=F+1, ha="left")
wire(ax, [(0.95, 6.30), (2.30, 6.30)])
wire(ax, [(0.95, 4.55), (2.30, 4.55)])

# HA1 → HA2
wire(ax, [(5.90, 6.30), (8.45, 6.30)])
T(ax, 6.30, 6.62, "$S_1=A\\oplus B$", size=F-3, color=GREY, ha="left")
wire(ax, [(5.90, 4.55), (7.15, 4.55), (7.15, 1.45), (13.9, 1.45)])
T(ax, 7.30, 4.20, "$C_1=A\\cdot B$", size=F-3, color=GREY, ha="left")

# Cin
T(ax, 0.45, 3.45, "$C_{in}$", size=F-1, ha="left")
wire(ax, [(1.15, 3.45), (8.30, 3.45)])

# HA2 输出
wire(ax, [(11.90, 4.55), (15.0, 4.55)])
T(ax, 15.15, 4.55, "$S$", size=F+2, color=RED, ha="left")
wire(ax, [(11.90, 2.95), (12.9, 2.95), (12.9, 2.05), (13.9, 2.05)])
T(ax, 12.05, 2.62, "$C_2$", size=F-3, color=GREY, ha="left")

oO, yO = g_or(ax, 13.9, 1.20, w=2.3, h=1.7)
wire(ax, [(oO, yO), (16.7, yO)])
T(ax, 16.85, yO, "$C_{out}$", size=F+1, color=RED, ha="left")

T(ax, 8.4, 7.45, "全加器：两个半加器 + 一个或门", size=F+1)
T(ax, 8.4, 0.35, "$S=A\\oplus B\\oplus C_{in}$，$C_{out}=A\\cdot B+C_{in}\\cdot(A\\oplus B)$", size=F-2, color=GREY)
fig.subplots_adjust(0.01, 0.01, 0.99, 0.99)
fig.savefig(BASE + "logic-fulladder.png", dpi=170); plt.close(fig)
print("ok full adder")
