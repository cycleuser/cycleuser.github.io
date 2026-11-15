"""加法原理 / 乘法原理：食堂点餐的两种情形"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch
from PIL import Image
import os

plt.rcParams["font.family"] = ["PingFang SC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
INK = "#2b2b2b"
GREY, GREEN, ORANGE = "#9aa4ae", "#4a7c59", "#d2691e"
RED, BLUE = "#b03a2e", "#2f4f6f"
BASE = "/Users/fred/Documents/GitHub/cycleuser/blog/output/img/kaoyan-math/"
F = 14.0
SCRATCH = os.path.dirname(os.path.abspath(__file__))

def axes_(w, h, xlim, ylim):
    fig, ax = plt.subplots(figsize=(w, h), dpi=120)
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values(): sp.set_color("none")
    return fig, ax

def T(ax, x, y, s, size=F, color=INK, ha="center", va="center"):
    ax.text(x, y, s, fontsize=size, color=color, ha=ha, va=va, zorder=10)

def card(ax, x, y, w, h, text, on, color):
    fc = color if on else "white"
    ec = color if on else "#c9ced4"
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.06",
                                facecolor=fc, edgecolor=ec, lw=2.2, zorder=4))
    T(ax, x+w/2, y+h/2, text, size=F-2, color="white" if on else GREY)

def grab(fig, tag):
    fp = os.path.join(SCRATCH, "_%s.png" % tag)
    fig.savefig(fp, dpi=120); plt.close(fig)
    im = Image.open(fp).convert("RGB"); os.remove(fp)
    return im

def save_gif(frames, name, dur=850):
    pal = [f.convert("P", palette=Image.ADAPTIVE) for f in frames]
    pal[0].save(BASE + name, save_all=True, append_images=pal[1:], duration=dur, loop=0, optimize=True)
    print("ok", name, len(frames))

# =====================================================================
# 加法原理：主食三选一 —— 面 3 种 或 饭 2 种
# =====================================================================
noodle = ["牛肉面", "炸酱面", "酸辣粉"]
rice = ["盖饭", "炒饭"]
frames = []
for step in range(7):
    fig, ax = axes_(7.6, 4.6, (0, 15.2), (0, 9.2))
    T(ax, 7.6, 8.6, "加法原理：主食只能选一样，面或饭", size=F-1)
    T(ax, 2.4, 7.0, "面（3 种）", size=F-3, color=ORANGE)
    T(ax, 2.4, 2.7, "饭（2 种）", size=F-3, color=BLUE)
    for i, s in enumerate(noodle):
        on = step >= i+1
        card(ax, 4.4 + i*2.6, 6.1, 2.2, 1.1, s, on, ORANGE)
    for j, s in enumerate(rice):
        on = step >= 4 + j
        card(ax, 4.4 + j*2.6, 1.8, 2.2, 1.1, s, on, BLUE)
    T(ax, 7.4, 4.6, "两类不能同时选，互不重叠 → 相加", size=F-3, color=GREY)
    k1 = min(step, 3); k2 = max(0, min(step-3, 2))
    T(ax, 7.4, 0.95, "数到第 %d 种：面 %d 种 + 饭 %d 种" % (k1+k2, k1, k2), size=F-2)
    if step == 6:
        T(ax, 7.4, 0.25, "$3+2=5$ 种选法", size=F+2, color=GREEN)
    fig.subplots_adjust(0.01, 0.02, 0.99, 0.98)
    frames.append(grab(fig, "add"))
save_gif(frames, "comb-addition.gif", dur=850)

# =====================================================================
# 乘法原理：套餐 = 主食 3 选 1，再饮料 2 选 1
# =====================================================================
mains = ["牛肉面", "盖饭", "炒饭"]
drinks = ["可乐", "豆浆"]
frames = []
pairs = [(i, j) for i in range(3) for j in range(2)]
for step in range(len(pairs)+3):
    fig, ax = axes_(7.8, 5.0, (0, 15.6), (0, 10.2))
    T(ax, 7.8, 9.6, "乘法原理：一份套餐 = 先选主食，再选饮料", size=F-1)
    # 列标题（饮料）
    for j, d in enumerate(drinks):
        T(ax, 7.6 + j*3.4, 8.3, d, size=F-2, color=BLUE)
    for i, m in enumerate(mains):
        y = 6.4 - i*2.3
        T(ax, 2.6, y+0.55, m, size=F-3, color=ORANGE, ha="right")
        for j in range(2):
            idx = i*2 + j
            on = step >= idx+1
            x = 6.0 + j*3.4
            ax.add_patch(FancyBboxPatch((x, y), 3.0, 1.1, boxstyle="round,pad=0.06",
                                        facecolor=ORANGE if on else "white",
                                        edgecolor=ORANGE if on else "#c9ced4",
                                        lw=2.2, zorder=4, alpha=0.9 if on else 1.0))
            txt = "%s+%s" % (m, drinks[j])
            T(ax, x+1.5, y+0.55, txt, size=F-4, color="white" if on else GREY)
            if on:
                T(ax, x+2.85, y+0.15, str(idx+1), size=F-5, color="white", ha="right")
    T(ax, 11.2, 1.15, "每一格是一种套餐；逐格配出来就是「先 3 再 2」", size=F-3, color=GREY)
    if step >= len(pairs):
        T(ax, 11.2, 0.45, "$3\\times2=6$ 种套餐", size=F+2, color=GREEN)
    fig.subplots_adjust(0.01, 0.02, 0.99, 0.98)
    frames.append(grab(fig, "mul"))
save_gif(frames, "comb-multiplication.gif", dur=800)
