import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, Circle, PathPatch
from matplotlib.path import Path
from matplotlib.lines import Line2D
import os

plt.rcParams["font.family"] = ["PingFang SC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
INK, ORANGE, BLUE = "#2b2b2b", "#d2691e", "#2f4f6f"
RED, GREEN, GREY, BROWN, CREAM = "#b03a2e", "#4a7c59", "#8a8a8a", "#7a5230", "#e8ddd0"
BASE = "/Users/fred/Documents/GitHub/cycleuser/blog/output/img/kaoyan-math/"
F = 11.5

def and_gate(ax, x, y, w=1.6, h=1.0, color=BLUE):
    """AND 门：矩形 + 半圆"""
    verts = [(x, y+h), (x, y), (x+w*0.5, y), (x+w, y+h/2), (x+w*0.5, y+h), (x, y+h)]
    codes = [Path.MOVETO, Path.LINETO, Path.CURVE3, Path.CURVE3, Path.CURVE3, Path.CURVE3]
    ax.add_patch(plt.Polygon([(x,y),(x, y+h),(x+w*0.45, y+h),(x+w, y+h/2),(x+w*0.45, y),(x,y)],
                             closed=True, fill=False, edgecolor=color, lw=2.4))
def or_gate(ax, x, y, w=1.6, h=1.0, color=BLUE):
    verts = [(x,y),(x+w*0.55,y),(x+w,y+h/2),(x+w*0.55,y+h),(x,y+h)]
    codes = [Path.MOVETO, Path.CURVE3, Path.CURVE3, Path.CURVE3, Path.CURVE3]
    # 简化：用二次曲线近似
    ax.add_patch(plt.Polygon([(x,y),(x+w*0.35, y+h*0.12),(x+w, y+h/2),(x+w*0.35, y+h*0.88),(x,y+h)],
                             closed=True, fill=False, edgecolor=color, lw=2.4))
def wire(ax, x1, y1, x2, y2, color=INK, lw=1.8, ls="-"):
    ax.plot([x1, x2], [y1, y2], color=color, lw=lw, ls=ls)
def dot(ax, x, y, color=INK):
    ax.plot([x],[y], "o", color=color, ms=4)

# ============ 图 1: 三个基本门 ============
fig, axes = plt.subplots(1, 4, figsize=(15.6, 4.0), dpi=170)

# AND
ax = axes[0]
ax.set_xlim(0, 4.4); ax.set_ylim(0, 2.6); ax.set_aspect("equal")
ax.set_xticks([]); ax.set_yticks([])
for sp_ in ax.spines.values(): sp_.set_color("none")
# 门体
t = np.linspace(-np.pi/2, np.pi/2, 60)
gx, gy = 1.5, 0.8; W, H = 1.7, 1.0
ax.plot([gx, gx], [gy, gy+H], color=BLUE, lw=2.4)
# AND: 左边直线 + 右半圆
ax.plot(gx, gy, color=BLUE, lw=2.4); ax.plot(gx, gy+H, color=BLUE, lw=2.4)
ax.plot(gx + W/2 + (W/2)*np.cos(t), gy + H/2 + (H/2)*np.sin(t), color=BLUE, lw=2.4)

# 输入输出
ax.plot([0.45, gx], [gy+0.72, gy+0.72], color=INK, lw=1.8)
ax.plot([0.45, gx], [gy+0.28, gy+0.28], color=INK, lw=1.8)
ax.plot([gx+W*0.985, 3.6], [gy+H/2, gy+H/2], color=INK, lw=1.8)
ax.text(0.15, gy+0.72, "A", fontsize=F, color=INK, va="center")
ax.text(0.15, gy+0.28, "B", fontsize=F, color=INK, va="center")
ax.text(3.8, gy+H/2, "A·B", fontsize=F, color=RED, va="center")
ax.text(1.75, gy+H/2, "&", fontsize=13, color=BLUE, ha="center", va="center")
ax.set_title("与门 AND\nA·B：两个输入都是 1 才输出 1", fontsize=F+0.8, color=INK, pad=6)
# 真值表小注
ax.text(2.2, 2.25, "1·1=1  1·0=0\n0·1=0  0·0=0", fontsize=F-3, color=GREY, ha="center")

# OR
ax = axes[1]
ax.set_xlim(0, 4.4); ax.set_ylim(0, 2.6); ax.set_aspect("equal")
ax.set_xticks([]); ax.set_yticks([])
for sp_ in ax.spines.values(): sp_.set_color("none")
gx, gy = 1.4, 0.8
# OR 门：后掠形
ax.plot([gx, gx+0.5], [gy, gy], color=BLUE, lw=2.4)
# 手画 OR：两条弧
xs = np.linspace(0, 1, 40)
upper_b = gy+H - 0.12
ax.plot(gx + 0.5 + (W-0.5)*(xs), gy + H - (H*(xs**1.6)), color=BLUE, lw=2.4)
lower_b = gy + 0.12
ax.plot(gx + 0.5 + (W-0.5)*(xs), gy + (H*(xs**1.6)) - 0.0 + 0, color=BLUE, lw=2.4)
# 底部前弧
ax.plot(gx + 0.5 - (0.5)*(np.cos(t)/1), gy+H/2 + (H/2)*np.sin(t), color=BLUE, lw=2.4)
ax.plot([0.55, gx+0.18], [gy+0.72, gy+0.72], color=INK, lw=1.8)
ax.plot([0.55, gx+0.18], [gy+0.28, gy+0.28], color=INK, lw=1.8)
ax.plot([gx+W, 3.5], [gy+H/2, gy+H/2], color=INK, lw=1.8)
ax.text(0.2, gy+0.72, "A", fontsize=F, color=INK, va="center")
ax.text(0.2, gy+0.28, "B", fontsize=F, color=INK, va="center")
ax.text(3.75, gy+H/2, "A+B", fontsize=F, color=RED, va="center")
ax.text(1.85, gy+H/2, "≥1", fontsize=11, color=BLUE, ha="center", va="center")
ax.set_title("或门 OR\nA+B：有 1 就输出 1", fontsize=F+0.8, color=INK, pad=6)
ax.text(2.1, 2.25, "1+1=1  1+0=1\n0+1=1  0+0=0", fontsize=F-3, color=GREY, ha="center")

# NOT
ax = axes[2]
ax.set_xlim(0, 4.4); ax.set_ylim(0, 2.6); ax.set_aspect("equal")
ax.set_xticks([]); ax.set_yticks([])
for sp_ in ax.spines.values(): sp_.set_color("none")
gx, gy = 1.3, 1.0
ax.plot([gx, gx+1.5], [gy, gy+0.62], color=BLUE, lw=2.4)
ax.plot([gx, gx+1.5], [gy, gy-0.62], color=BLUE, lw=2.4)
c2 = Circle((gx+1.62, gy), 0.12, fill=False, edgecolor=BLUE, lw=2.2)
ax.add_patch(c2)
ax.plot([0.5, gx], [gy, gy], color=INK, lw=1.8)
ax.plot([gx+1.75, 3.5], [gy, gy], color=INK, lw=1.8)
ax.text(0.2, gy, "A", fontsize=F, color=INK, va="center")
ax.text(3.75, gy, "Ā", fontsize=F, color=RED, va="center")
ax.set_title("非门 NOT\nĀ：0 变 1、1 变 0", fontsize=F+0.8, color=INK, pad=6)
ax.text(2.05, 2.25, "Ā=1−A：0→1，1→0", fontsize=F-3, color=GREY, ha="center")

# XOR
ax = axes[3]
ax.set_xlim(0, 4.4); ax.set_ylim(0, 2.6); ax.set_aspect("equal")
ax.set_xticks([]); ax.set_yticks([])
for sp_ in ax.spines.values(): sp_.set_color("none")
gx, gy = 1.4, 0.8
# 双线 OR（XOR 画第二条弧）
ax.plot(gx + 0.5 + (W-0.5)*(xs), gy + H - (H*(xs**1.6)), color=BLUE, lw=2.4)
ax.plot(gx + 0.5 + (W-0.5)*(xs), gy + (H*(xs**1.6)), color=BLUE, lw=2.4)
ax.plot(gx + 0.5 - (0.5)*(np.cos(t)), gy+H/2 + (H/2)*np.sin(t), color=BLUE, lw=2.4)
ax.plot(gx + 0.42 - (0.5)*(np.cos(t)), gy+H/2 + (H/2)*np.sin(t), color=BLUE, lw=2.4)
ax.plot([0.75, gx+0.14], [gy+0.72, gy+0.72], color=INK, lw=1.8)
ax.plot([0.75, gx+0.14], [gy+0.28, gy+0.28], color=INK, lw=1.8)
ax.plot([gx+W, 3.4], [gy+H/2, gy+H/2], color=INK, lw=1.8)
ax.text(0.4, gy+0.72, "A", fontsize=F, color=INK, va="center")
ax.text(0.4, gy+0.28, "B", fontsize=F, color=INK, va="center")
ax.text(3.65, gy+H/2, "A⊕B", fontsize=F, color=RED, va="center")
ax.set_title("异或 XOR\nA⊕B：不同才输出 1", fontsize=F+0.8, color=INK, pad=6)
ax.text(2.1, 2.25, "1⊕1=0  1⊕0=1\n0⊕1=1  0⊕0=0", fontsize=F-3, color=GREY, ha="center")

fig.tight_layout()
fig.savefig(BASE + "logic-gates.png", dpi=170)
plt.close(fig)
print("ok gates")

# ============ 图 2: XOR 用基本门实现 ============
fig, ax = plt.subplots(figsize=(10.2, 5.6), dpi=170)
ax.set_xlim(0, 12); ax.set_ylim(0, 6.8); ax.set_aspect("equal")
ax.set_xticks([]); ax.set_yticks([])
for sp_ in ax.spines.values(): sp_.set_color("none")

W = 1.5; H = 1.0
def small_and(cx, cy):
    ax.plot([cx, cx], [cy, cy+H], color=BLUE, lw=2.4)
    ax.plot(cx + W/2 + (W/2)*np.cos(t), cy + H/2 + (H/2)*np.sin(t), color=BLUE, lw=2.4)
    ax.text(cx+W*0.40, cy+H/2, "&", fontsize=11, color=BLUE, ha="center", va="center")
    return cx+W
def small_or(cx, cy):
    xs_ = np.linspace(0, 1, 40)
    ax.plot(cx + 0.5 + (W-0.5)*xs_, cy + H - H*(xs_**1.55), color=BLUE, lw=2.4)
    ax.plot(cx + 0.5 + (W-0.5)*xs_, cy + H*(xs_**1.55), color=BLUE, lw=2.4)
    ax.plot(cx + 0.5 - 0.5*np.cos(t), cy+H/2 + (H/2)*np.sin(t), color=BLUE, lw=2.4)
    return cx+W
def small_not(cx, cy):
    L = 0.9
    ax.plot([cx, cx+L], [cy, cy+0.34], color=BLUE, lw=2.4)
    ax.plot([cx, cx+L], [cy, cy-0.34], color=BLUE, lw=2.4)
    ax.add_patch(Circle((cx+L+0.10, cy), 0.09, fill=False, edgecolor=BLUE, lw=2.2))
    return cx+L+0.19
def wire(x1, y1, x2, y2, lw=1.9, color=INK):
    ax.plot([x1, x2], [y1, y2], color=color, lw=lw)
def dot(x, y):
    ax.plot([x],[y], "o", color=INK, ms=5)

yA, yB = 5.7, 1.0
yA1 = 5.5   # AND1 门底部 y
yA2 = 2.6   # AND2 底部
yANDin1 = yA1 + 0.7
yANDin2 = yA2 + 0.3

# 输入主干
wire(0.4, yA, 2.3, yA); ax.text(0.15, yA, "A", fontsize=F+1, color=INK, va="center")
wire(0.4, yB, 2.3, yB); ax.text(0.15, yB, "B", fontsize=F+1, color=INK, va="center")

# A 的非门：放在 A 线上方独立高度 yNOT_A=6.15
yNOTA = 6.15
wire(1.6, yA, 1.6, yNOTA); dot(1.6, yA)
oNA = small_not(1.8, yNOTA)
wire(oNA, yNOTA, 2.6, yNOTA)
wire(2.6, yNOTA, 2.6, yANDin1)
wire(2.6, yANDin1, 3.9, yANDin1)
ax.text(1.55, yNOTA+0.42, "Ā", fontsize=F-1, color=GREY)

# B 的非门 yNOTB = 0.35
yNOTB = 0.35
wire(1.9, yB, 1.9, yNOTB); dot(1.9, yB)
oNB = small_not(2.1, yNOTB)
wire(oNB, yNOTB, 2.7, yNOTB)
wire(2.7, yNOTB, 2.7, yANDin2)
wire(2.7, yANDin2, 3.9, yANDin2)
ax.text(2.05, yNOTB-0.35, "B̄", fontsize=F-1, color=GREY)

# 进 AND 的第二个输入：AND1←B（分支），AND2←A（分支）
dot(2.9, yA)                     # A 分支下行进 AND2 第二输入
wire(2.9, yA, 2.9, yANDin2+0.0)
wire(2.9, yANDin2+0.0, 3.9, yANDin2+0.0)
dot(3.05, yB)
wire(3.05, yB, 3.05, yANDin1+0.0)
wire(3.05, yANDin1+0.0, 3.9, yANDin1+0.0)

o1 = small_and(3.9, yA1)
ax.text(o1+0.45, yA1+0.75, "Ā·B", fontsize=F-1, color=GREY)
o2 = small_and(3.9, yA2)
ax.text(o2+0.45, yA2+0.75, "A·B̄", fontsize=F-1, color=GREY)

# 输出汇到 OR
yOR = 3.9
wire(o1, yA1+0.5, 8.3, yA1+0.5)
wire(8.3, yA1+0.5, 8.3, yOR+0.78)
wire(o2, yA2+0.5, 8.3, yA2+0.5)
wire(8.3, yA2+0.5, 8.3, yOR+0.22)
oR = small_or(8.3, yOR)
wire(oR, yOR+0.5, 10.7, yOR+0.5)
ax.text(10.95, yOR+0.5, "A⊕B", fontsize=F+1, color=RED, va="center")

ax.text(6.0, 6.55, "A⊕B = (Ā·B) + (A·B̄)", fontsize=F+1, color=INK, ha="center")
ax.set_title("用与、或、非门搭出异或", fontsize=F+2, color=INK, pad=10)
fig.tight_layout()
fig.savefig(BASE + "logic-xor-impl.png", dpi=170)
plt.close(fig)

print("ok xor impl")
