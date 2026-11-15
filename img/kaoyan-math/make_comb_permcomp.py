"""排列 / 组合 各自独立的动画"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch
from PIL import Image
import itertools, os

plt.rcParams["font.family"] = ["PingFang SC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
INK = "#2b2b2b"
BLUE, GREY, GREEN = "#2f4f6f", "#8a8a8a", "#4a7c59"
PAL = ["#b03a2e", "#d2691e", "#4a7c59", "#2f4f6f", "#6b4c9a"]
BASE = "/Users/fred/Documents/GitHub/cycleuser/blog/output/img/kaoyan-math/"
F = 14.0
SCRATCH = os.path.dirname(os.path.abspath(__file__))
LETTERS = ["A", "B", "C", "D", "E"]

def axes_(w, h, xlim, ylim):
    fig, ax = plt.subplots(figsize=(w, h), dpi=120)
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values(): sp.set_color("none")
    return fig, ax

def T(ax, x, y, s, size=F, color=INK, ha="center", va="center"):
    ax.text(x, y, s, fontsize=size, color=color, ha=ha, va=va, zorder=9)

def grab(fig, tag):
    fp = os.path.join(SCRATCH, "_%s.png" % tag)
    fig.savefig(fp, dpi=120); plt.close(fig)
    im = Image.open(fp).convert("RGB"); os.remove(fp)
    return im

def save_gif(frames, name, dur=800):
    pal = [f.convert("P", palette=Image.ADAPTIVE) for f in frames]
    pal[0].save(BASE + name, save_all=True, append_images=pal[1:], duration=dur, loop=0, optimize=True)
    print("ok", name, len(frames))

def pool(ax, letters=LETTERS, y=8.6, x0=1.2, gap=1.25, hi=None, label="5 个不同的元素"):
    T(ax, x0 + gap*2, 9.65, label, size=F-1, color=GREY)
    for i, L in enumerate(letters):
        x = x0 + i*gap
        on = (hi is None) or (i in hi)
        ax.add_patch(Circle((x, y), 0.44, facecolor=PAL[i], alpha=0.85 if on else 0.18,
                            edgecolor=PAL[i], lw=2.0, zorder=4))
        T(ax, x, y, L, size=F, color="white" if on else PAL[i])

def slots(ax, filled, y=5.6, x0=1.2, gap=2.0):
    for j in range(3):
        x = x0 + j*gap
        ax.add_patch(FancyBboxPatch((x-0.5, y-0.5), 1.0, 1.0, boxstyle="round,pad=0.05",
                                    facecolor="#f6f8fa", edgecolor="#c6ccd3", lw=1.6, zorder=2))
        if j < len(filled):
            idx = LETTERS.index(filled[j])
            ax.add_patch(Circle((x, y), 0.42, facecolor=PAL[idx], alpha=0.9,
                                edgecolor=PAL[idx], lw=2.0, zorder=5))
            T(ax, x, y, filled[j], size=F, color="white")
        T(ax, x, y-0.95, "第 %d 位" % (j+1), size=F-4, color=GREY)

# =====================================================================
# 图 A：排列（有序，逐位填，换个顺序算新方案）
# =====================================================================
seqs = [("A", "C", "E"), ("E", "A", "C")]
frames = []
for si, seq in enumerate(seqs):
    for step in range(4):
        fig, ax = axes_(7.0, 4.8, (0, 8.4), (1.2, 10.2))
        picked = list(seq)[:step]
        pool(ax, hi=[LETTERS.index(p) for p in picked] if picked else [])
        slots(ax, picked)
        cnt = [1, 5, 20, 60][step]
        note = ["从 5 个里取 3 个，按顺序放进三个位置",
                "第 1 位：5 种选法",
                "第 2 位：剩 4 种，前两位共 $5\\times4=20$ 种",
                "第 3 位：剩 3 种，共 $5\\times4\\times3=60$ 种"][step]
        T(ax, 4.2, 3.55, note, size=F-2, color=INK)
        if step == 3:
            T(ax, 4.2, 2.70, "$A_5^3=%d$" % cnt, size=F+4, color=BLUE)
        if si == 1 and step == 3:
            T(ax, 4.2, 1.85, "换成 $E,A,C$：位置上的元素变了，就是另一种排列",
              size=F-2, color=GREEN)
        fig.subplots_adjust(0.01, 0.01, 0.99, 0.99)
        frames.append(grab(fig, "p"))
save_gif(frames, "comb-permutation.gif", dur=900)

# =====================================================================
# 图 B：组合（无序，只挑出来，顺序无效）
# =====================================================================
combos = list(itertools.combinations(LETTERS, 3))     # 10 种
frames = []
# 阶段1：挑出一组，展示 6 种写法都算同一种
first = ("A", "C", "E")
orders = list(itertools.permutations(first))
for k in range(len(orders)+1):
    fig, ax = axes_(7.0, 4.8, (0, 8.4), (1.2, 10.2))
    pool(ax, hi=[LETTERS.index(p) for p in first])
    # 中括号包住一组
    ax.add_patch(Circle((4.2, 5.9), 1.55, fill=False, edgecolor=GREEN, lw=2.2, ls="--", zorder=2))
    for j, L in enumerate(first):
        ang = np.pi/2 + j*2*np.pi/3
        x = 4.2 + 0.85*np.cos(ang); y = 5.9 + 0.85*np.sin(ang)
        idx = LETTERS.index(L)
        ax.add_patch(Circle((x, y), 0.42, facecolor=PAL[idx], alpha=0.9,
                            edgecolor=PAL[idx], lw=2.0, zorder=5))
        T(ax, x, y, L, size=F, color="white")
    T(ax, 4.2, 3.75, "只挑出 3 个，装进一个集合", size=F-2, color=INK)
    if k > 0:
        shown = orders[k-1]
        T(ax, 4.2, 3.05, "写法 %d：{%s}" % (k, ",".join(shown)), size=F-1, color=GREY)
    if k == len(orders):
        T(ax, 4.2, 2.30, "6 种写法，指的是同一堆元素", size=F-2, color=GREEN)
        T(ax, 4.2, 1.55, "组合只算 1 种", size=F+1, color=GREEN)
    fig.subplots_adjust(0.01, 0.01, 0.99, 0.99)
    frames.append(grab(fig, "c"))

# 阶段2：把 10 种组合逐个列出，说明 C(5,3)=10
for k in range(1, len(combos)+1):
    fig, ax = axes_(7.0, 4.9, (0, 8.4), (0.4, 10.4))
    pool(ax, hi=[LETTERS.index(p) for p in combos[k-1]])
    T(ax, 4.2, 7.05, "把所有「选 3 个」的组都列出来", size=F-2, color=INK)
    for i, cb in enumerate(combos[:k]):
        col = i // 5; row = i % 5
        x = 1.6 + row*1.45; y = 5.6 - col*1.5
        xs = "{" + ",".join(cb) + "}"
        T(ax, x, y, xs, size=F-3 if i != k-1 else F-1,
          color=GREEN if i == k-1 else GREY)
    T(ax, 4.2, 2.35, "$C_5^3=\\dfrac{A_5^3}{3!}=\\dfrac{60}{6}=%d$" % k, size=F+2, color=BLUE)
    T(ax, 4.2, 1.25, "同样 3 个元素有 $3!=6$ 种排法，组合里只算 1 种，所以要除掉", size=F-3, color=GREY)
    fig.subplots_adjust(0.01, 0.01, 0.99, 0.99)
    frames.append(grab(fig, "c2"))
save_gif(frames, "comb-combination.gif", dur=700)
