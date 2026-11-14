"""附录8 开头概念动画：排列/组合、抽样、随机、回归、分类"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, Rectangle
from PIL import Image
import os

plt.rcParams["font.family"] = ["PingFang SC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
INK = "#2b2b2b"
BLUE, GREY, ORANGE = "#2f4f6f", "#8a8a8a", "#d2691e"
RED, GREEN, PURPLE = "#b03a2e", "#4a7c59", "#6b4c9a"
PAL = ["#b03a2e", "#d2691e", "#4a7c59", "#2f4f6f", "#6b4c9a"]
BASE = "/Users/fred/Documents/GitHub/cycleuser/blog/output/img/kaoyan-math/"
F = 13.0
SCRATCH = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(7)

def axes_(w, h, xlim, ylim):
    fig, ax = plt.subplots(figsize=(w, h), dpi=120)
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values(): sp.set_color("none")
    return fig, ax

def T(ax, x, y, s, size=F, color=INK, ha="center", va="center", weight="normal"):
    ax.text(x, y, s, fontsize=size, color=color, ha=ha, va=va, weight=weight, zorder=9)

def grab(fig, tag):
    fp = os.path.join(SCRATCH, "_%s.png" % tag)
    fig.savefig(fp, dpi=120); plt.close(fig)
    im = Image.open(fp).convert("RGB"); os.remove(fp)
    return im

def save_gif(frames, name, dur=600):
    pal = [f.convert("P", palette=Image.ADAPTIVE) for f in frames]
    pal[0].save(BASE + name, save_all=True, append_images=pal[1:], duration=dur, loop=0, optimize=True)
    print("ok", name, len(frames))

# =====================================================================
# 1) 排列 vs 组合
# =====================================================================
letters = ["A", "B", "C", "D", "E"]
frames = []
picks_orders = [("A","B","C"), ("B","D","E"), ("C","A","E")]
for phase, (p1, p2, p3) in enumerate(picks_orders):
    for step in range(4):
        fig, ax = axes_(7.8, 4.6, (0, 19.0), (2.6, 11.4))
        # 球池
        T(ax, 3.2, 10.6, "5 个元素", size=F)
        for i, L in enumerate(letters):
            x = 1.0 + i*1.15
            ax.add_patch(Circle((x, 9.1), 0.42, facecolor=PAL[i], alpha=0.30,
                                edgecolor=PAL[i], lw=2.0, zorder=4))
            T(ax, x, 9.1, L, size=F, color=PAL[i])
        # 三个位置（有序）
        picked = [p1, p2, p3][:step]
        T(ax, 3.6, 7.95, "排成一列（顺序不同算不同）", size=F-2, color=GREY)
        for j in range(3):
            x = 1.9 + j*1.7
            ax.add_patch(FancyBboxPatch((x-0.62, 6.0), 1.24, 1.24, boxstyle="round,pad=0.05",
                                        facecolor="#f4f6f9", edgecolor=GREY, lw=1.6, zorder=3))
            if j < len(picked):
                L = picked[j]
                idx = letters.index(L)
                ax.add_patch(Circle((x, 6.62), 0.44, facecolor=PAL[idx], alpha=0.55,
                                    edgecolor=PAL[idx], lw=2.0, zorder=5))
                T(ax, x, 6.62, L, size=F, color="white")
        step_txt = ["还没开始", "第 1 位：5 种选法", "第 2 位：剩 4 种", "第 3 位：剩 3 种"][step]
        T(ax, 3.6, 4.95, step_txt, size=F-1, color=INK)
        n = [1, 5, 20, 60][step]
        T(ax, 3.6, 3.85, "$A_5^3=5\\times4\\times3=%d$" % n, size=F+2, color=BLUE)

        # 右侧：组合（无序）
        T(ax, 12.6, 10.6, "只问选出哪 3 个（顺序无关）", size=F-2, color=GREY)
        ax.add_patch(Circle((12.6, 8.0), 1.5, fill=False, edgecolor=GREEN, lw=2.0, ls="--", zorder=3))
        if step > 0:
            trio = sorted([p1, p2, p3])
            for k, L in enumerate(trio):
                ang = np.pi/2 + k*2*np.pi/3
                x = 12.6 + 0.85*np.cos(ang); y = 8.0 + 0.85*np.sin(ang)
                idx = letters.index(L)
                ax.add_patch(Circle((x, y), 0.40, facecolor=PAL[idx], alpha=0.55,
                                    edgecolor=PAL[idx], lw=2.0, zorder=5))
                T(ax, x, y, L, size=F-1, color="white")
        T(ax, 12.6, 5.55, "选出的同一堆元素，换个顺序仍是同一种", size=F-3, color=INK)
        if step == 3:
            T(ax, 12.6, 4.55, "同样 3 个元素有 $3!=6$ 种排法，组合里只算 1 种", size=F-3, color=GREY)
            T(ax, 12.6, 3.55, "$C_5^3=\\dfrac{60}{6}=10$", size=F+2, color=GREEN)
        fig.subplots_adjust(0.01, 0.01, 0.99, 0.99)
        frames.append(grab(fig, "pc"))
save_gif(frames, "comb-perm-comp.gif", dur=900)

# =====================================================================
# 2) 抽样
# =====================================================================
pts = rng.uniform(0.5, 7.5, size=(120, 2))
groups = np.where(pts[:, 0] < 3.0, 0, np.where(pts[:, 0] < 5.4, 1, 2))
gcol = ["#b03a2e", "#d2691e", "#2f4f6f"]
frames = []
simple_idx = rng.choice(len(pts), 12, replace=False)
for step in range(13):
    fig, ax = axes_(6.6, 4.6, (0, 17.0), (0, 10.0))
    T(ax, 4.2, 9.4, "总体：一堆个体", size=F)
    ax.add_patch(Rectangle((0.3, 0.6), 7.6, 8.0, fill=False, edgecolor=GREY, lw=1.4, ls="--"))
    selset = set(simple_idx[:step].tolist())
    for i, (x, y) in enumerate(pts):
        sel = i in selset
        ax.add_patch(Circle((x, y), 0.21 if sel else 0.16, facecolor=gcol[groups[i]],
                            alpha=1.0 if sel else 0.32,
                            edgecolor=INK if sel else "none", lw=1.4 if sel else 0, zorder=3))
    T(ax, 4.2, 0.2, "简单随机抽样：随手抓 %d 个（抓过的不放回）" % step, size=F-3, color=GREY)
    # 右：抽到的样本单独列出
    T(ax, 12.6, 9.4, "样本：抽出来的 %d 个" % step, size=F)
    for k in range(step):
        cx = 10.3 + (k % 5)*1.15; cy = 7.6 - (k // 5)*1.25
        gi = groups[simple_idx[k]]
        ax.add_patch(Circle((cx, cy), 0.30, facecolor=gcol[gi], alpha=0.95,
                            edgecolor=INK, lw=1.2, zorder=4))
    if step >= 12:
        T(ax, 12.6, 3.4, "样本的统计量（均值、比例等）", size=F-3, color=GREY)
        T(ax, 12.6, 2.6, "用来估计总体的参数", size=F-3, color=GREY)
    fig.subplots_adjust(0.01, 0.01, 0.99, 0.99)
    frames.append(grab(fig, "samp"))
save_gif(frames, "comb-sampling.gif", dur=500)

# 分层抽样
frames = []
per = 4
chosen = []
for g in range(3):
    idx = np.where(groups == g)[0]
    chosen.append(set(rng.choice(idx, per, replace=False)))
allch = chosen[0] | chosen[1] | chosen[2]
order = sorted(allch)
for step in range(0, 13):
    fig, ax = axes_(6.6, 4.6, (0, 17.0), (0, 10.0))
    T(ax, 4.2, 9.4, "总体：三类人（颜色不同）", size=F)
    ax.add_patch(Rectangle((0.3, 0.6), 7.6, 8.0, fill=False, edgecolor=GREY, lw=1.4, ls="--"))
    sel = set(order[:step])
    for i, (x, y) in enumerate(pts):
        on = i in sel
        ax.add_patch(Circle((x, y), 0.24 if on else 0.16, facecolor=gcol[groups[i]],
                            alpha=0.95 if on else 0.30, edgecolor="none", zorder=3))
    T(ax, 4.2, 0.2, "分层抽样：每一类各抽 %d 个" % per, size=F-3, color=GREY)
    T(ax, 12.6, 9.4, "每层都抽到", size=F)
    for g in range(3):
        got = len([i for i in order[:step] if groups[i] == g])
        T(ax, 11.0, 7.6 - g*1.5, "第 %d 类：%d/%d" % (g+1, got, per), size=F-2, color=gcol[g], ha="left")
    fig.subplots_adjust(0.01, 0.01, 0.99, 0.99)
    frames.append(grab(fig, "strat"))
save_gif(frames, "comb-stratified.gif", dur=450)

# =====================================================================
# 3) 随机：频率稳定
# =====================================================================
flips = rng.integers(0, 2, size=400)
frames = []
for step in [1, 2, 3, 5, 10, 20, 40, 80, 160, 240, 320, 400]:
    fig, ax = axes_(7.2, 4.4, (0, 14.0), (0, 9.0))
    ax.set_aspect("auto")
    xs = np.arange(1, step+1)
    p = np.cumsum(flips[:step])/xs
    ax.plot(xs, p, color=BLUE, lw=2.4)
    ax.axhline(0.5, color=RED, lw=1.6, ls="--")
    ax.set_ylim(0, 1); ax.set_xlim(0, 400)
    ax.set_yticks([0, 0.25, 0.5, 0.75, 1.0])
    for sp in ax.spines.values(): sp.set_color("#d8dde3")
    ax.tick_params(colors=GREY, labelsize=F-3)
    ax.text(0.5, 1.08, "抛硬币 %d 次：正面出现的频率" % step, transform=ax.transAxes,
            fontsize=F, color=INK, ha="center", va="center")
    ax.text(0.06, 0.55, "理论值 0.5", transform=ax.transAxes, fontsize=F-3, color=RED)
    ax.text(0.62, min(0.92, p[-1]+0.12), "当前 %.3f" % p[-1], transform=ax.transAxes,
            fontsize=F-3, color=BLUE)
    ax.text(0.5, -0.14, "次数越多，频率越贴近 0.5：单次结果不可预测，长期却有稳定规律",
            transform=ax.transAxes, fontsize=F-4, color=GREY, ha="center")
    fig.subplots_adjust(0.09, 0.16, 0.98, 0.86)
    frames.append(grab(fig, "rnd"))
save_gif(frames, "comb-random.gif", dur=700)

# =====================================================================
# 4) 回归
# =====================================================================
x = rng.uniform(0, 10, 40)
y = 0.8*x + 2 + rng.normal(0, 1.6, 40)
k_ls, b_ls = np.polyfit(x, y, 1)
frames = []
for t in np.linspace(0, 1, 12):
    k = k_ls + (1 - t)*2.4
    b = b_ls + (1 - t)*(-4.5)
    fig, ax = axes_(7.0, 4.6, (0, 15.0), (0, 10.4))
    ax.set_aspect("auto")
    ax.scatter(x, y, s=42, color=BLUE, alpha=0.75, edgecolor="white", linewidth=0.8, zorder=4)
    xs = np.linspace(0, 10, 50)
    ax.plot(xs, k*xs + b, color=RED, lw=2.6, zorder=5)
    if t > 0.9:
        for xi, yi in zip(x, y):
            ax.plot([xi, xi], [yi, k_ls*xi + b_ls], color=ORANGE, lw=1.4, alpha=0.85, zorder=3)
        T(ax, 5.0, -0.6, "橙色竖线＝残差，最小二乘法让残差平方和最小", size=F-4, color=GREY)
    ax.set_xlim(0, 10); ax.set_ylim(-1.6, 11)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values(): sp.set_color("#d8dde3")
    T(ax, 5.0, 10.15, "回归：用一条直线概括「$x$ 变大时 $y$ 大概怎么变」", size=F-2)
    fig.subplots_adjust(0.01, 0.06, 0.99, 0.98)
    frames.append(grab(fig, "reg"))
save_gif(frames, "comb-regression.gif", dur=650)

# =====================================================================
# 5) 分类
# =====================================================================
c1 = rng.normal([3.0, 3.0], 0.85, size=(24, 2))
c2 = rng.normal([6.5, 7.0], 0.85, size=(24, 2))
frames = []
for t in np.linspace(0, 1, 10):
    fig, ax = axes_(6.8, 4.6, (0, 14.4), (0, 10.2))
    ax.scatter(c1[:, 0], c1[:, 1], s=46, color=RED, alpha=0.8, edgecolor="white", linewidth=0.8, zorder=4)
    ax.scatter(c2[:, 0], c2[:, 1], s=46, color=BLUE, alpha=0.8, edgecolor="white", linewidth=0.8, zorder=4)
    ang = np.deg2rad(38)
    mid = np.array([4.75, 5.0])
    d = np.array([np.cos(ang), np.sin(ang)])
    n = np.array([-d[1], d[0]])
    p0 = mid - 7*d; p1 = mid + 7*d
    if t > 0.05:
        ax.plot([p0[0], p1[0]], [p0[1], p1[1]], color=GREEN, lw=2.6, zorder=5)
        T(ax, 5.5, 1.1, "决策边界：线一侧判为一类，另一侧判为另一类", size=F-4, color=GREEN)
    if t > 0.9:
        q = np.array([8.4, 8.8])
        ax.plot([q[0]], [q[1]], "o", ms=12, mfc="white", mec=INK, mew=2.0, zorder=6)
        T(ax, q[0]-0.5, q[1]+0.45, "新样本 → 蓝类", size=F-3, color=INK, ha="center")
    ax.set_xlim(0, 10.5); ax.set_ylim(0, 10)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values(): sp.set_color("#d8dde3")
    T(ax, 5.25, 9.8, "分类：看它落在哪一类，输出的是类别", size=F-2)
    fig.subplots_adjust(0.01, 0.06, 0.99, 0.98)
    frames.append(grab(fig, "cls"))
save_gif(frames, "comb-classification.gif", dur=700)
