"""加法原理 / 乘法原理：路线与班次（教材同一套场景对照）"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle
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

def node(ax, x, y, label, r=0.44):
    ax.add_patch(Circle((x, y), r, facecolor="white", edgecolor=INK, lw=2.4, zorder=8))
    T(ax, x, y, label, size=F-2, color=INK)

def qarc(ax, p0, p1, apex, color, lw=2.6, z=4, alpha=1.0):
    """过 p0、p1、顶点 apex 的二次曲线"""
    p0 = np.array(p0, float); p1 = np.array(p1, float); apex = np.array(apex, float)
    c = 2*apex - (p0+p1)/2
    t = np.linspace(0, 1, 120)
    pts = ((1-t)**2)[:, None]*p0 + (2*(1-t)*t)[:, None]*c + (t**2)[:, None]*p1
    ax.plot(pts[:, 0], pts[:, 1], color=color, lw=lw, zorder=z, alpha=alpha,
            solid_capstyle="round")

def grab(fig, tag):
    fp = os.path.join(SCRATCH, "_%s.png" % tag)
    fig.savefig(fp, dpi=120); plt.close(fig)
    im = Image.open(fp).convert("RGB"); os.remove(fp)
    return im

def save_gif(frames, name, dur=850):
    pal = [f.convert("P", palette=Image.ADAPTIVE) for f in frames]
    pal[0].save(BASE + name, save_all=True, append_images=pal[1:], duration=dur, loop=0, optimize=True)
    print("ok", name, len(frames))

A = (2.2, 5.0)      # 甲
B = (12.6, 5.0)     # 乙

# =====================================================================
# 加法原理：甲到乙，坐火车 3 班 或 坐汽车 2 班（任选其一即可完成）
# =====================================================================
train = ["K101", "K102", "K103"]
bus = ["大巴 1", "大巴 2"]
train_ap = [(7.4, 8.55), (7.4, 7.55), (7.4, 6.60)]
bus_ap = [(7.4, 3.55), (7.4, 2.55)]

frames = []
for step in range(7):
    fig, ax = axes_(7.8, 5.0, (0, 15.0), (0, 10.4))
    node(ax, *A, "甲")
    node(ax, *B, "乙")
    for i, ap in enumerate(train_ap):
        on = step >= i+1
        qarc(ax, A, B, ap, ORANGE if on else GREY, lw=3.4 if on else 2.0, alpha=1 if on else 0.45)
        T(ax, ap[0] + 1.95, ap[1] + 0.16, train[i], size=F-3, color=ORANGE if on else GREY)
    for j, ap in enumerate(bus_ap):
        on = step >= 4 + j
        qarc(ax, A, B, ap, BLUE if on else GREY, lw=3.4 if on else 2.0, alpha=1 if on else 0.45)
        T(ax, ap[0] + 1.55, ap[1] - 0.05, bus[j], size=F-3, color=BLUE if on else GREY)
    T(ax, 7.4, 10.05, "加法原理：从甲到乙，坐火车或坐汽车（二选一）", size=F-2)
    T(ax, 11.9, 8.55, "第 1 类：火车", size=F-4, color=ORANGE, ha="left")
    T(ax, 11.9, 2.55, "第 2 类：汽车", size=F-4, color=BLUE, ha="left")
    T(ax, 7.4, 0.55, "每一班都单独能到乙，互不重叠 → 把两类相加", size=F-3, color=GREY)
    k1 = min(step, 3); k2 = max(0, min(step-3, 2))
    T(ax, 7.4, 9.55, "火车 %d 班 ＋ 汽车 %d 班 ＝ 已数 %d 种" % (k1, k2, k1+k2),
      size=F-2, color=INK)
    if step == 6:
        T(ax, 7.4, 1.45, "$3+2=5$ 班，就是 5 种走法", size=F+2, color=GREEN)
    fig.subplots_adjust(0.01, 0.02, 0.99, 0.98)
    frames.append(grab(fig, "add"))
save_gif(frames, "comb-addition.gif", dur=850)

# =====================================================================
# 乘法原理：甲 → 乙（3 条路），乙 → 丙（2 条路）；两步都做完才算一种走法
# =====================================================================
A2 = (1.8, 5.0); B2 = (7.4, 5.0); C2 = (13.0, 5.0)
r1 = [(4.6, 8.0), (4.6, 7.1), (4.6, 2.5)]      # 甲→乙 三条路的顶点
r2 = [(10.2, 7.1), (10.2, 2.9)]                # 乙→丙 两条路的顶点
pairs = [(i, j) for i in range(3) for j in range(2)]
frames = []
for step in range(len(pairs)+2):
    fig, ax = axes_(8.6, 5.2, (0, 17.8), (0, 10.6))
    node(ax, *A2, "甲")
    node(ax, *B2, "乙")
    node(ax, *C2, "丙")
    for i, ap in enumerate(r1):
        qarc(ax, A2, B2, ap, ORANGE, lw=2.4, alpha=0.9)
        T(ax, ap[0], ap[1] + (0.30 if ap[1] > 5 else -0.34), "路 %s" % "①②③"[i], size=F-4, color=ORANGE)
    for j, ap in enumerate(r2):
        qarc(ax, B2, C2, ap, BLUE, lw=2.4, alpha=0.9)
        T(ax, ap[0], ap[1] + (0.30 if ap[1] > 5 else -0.34), "路 %s" % "ⓐⓑ"[j], size=F-4, color=BLUE)
    T(ax, 7.4, 10.15, "乘法原理：甲→乙有 3 条路，乙→丙有 2 条路，两步都走完才算一种", size=F-2)
    # 已枚举的走法
    for k, (i, j) in enumerate(pairs[:step]):
        last = (k == step-1)
        col = RED if last else GREY
        qarc(ax, A2, B2, r1[i], RED if last else "#dfe3e8", lw=5.0 if last else 2.4, z=6 if last else 3)
        qarc(ax, B2, C2, r2[j], RED if last else "#dfe3e8", lw=5.0 if last else 2.4, z=6 if last else 3)
        T(ax, 14.9, 8.5 - k*0.70, "路 %s ＋ 路 %s" % ("①②③"[i], "ⓐⓑ"[j]),
          size=F-4, color=col, ha="left")
    T(ax, 14.9, 9.25, "已配出的走法", size=F-4, color=GREY, ha="left")
    T(ax, 6.0, 1.35, "每条「甲→乙」和每条「乙→丙」都能配成一种走法", size=F-3, color=GREY)
    if step >= len(pairs):
        T(ax, 6.0, 0.6, "$3\\times2=6$ 种走法", size=F+2, color=GREEN)
    fig.subplots_adjust(0.01, 0.02, 0.99, 0.98)
    frames.append(grab(fig, "mul"))
save_gif(frames, "comb-multiplication.gif", dur=800)
