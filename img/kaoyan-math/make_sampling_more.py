"""抽样策略与随机的进一步动画：配额/分层/整群、伪随机 vs 真随机"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Rectangle, FancyBboxPatch
from PIL import Image
import os

plt.rcParams["font.family"] = ["PingFang SC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
INK = "#2b2b2b"
BLUE, GREY, GREEN, ORANGE = "#2f4f6f", "#8a8a8a", "#4a7c59", "#d2691e"
RED = "#b03a2e"
BASE = "/Users/fred/Documents/GitHub/cycleuser/blog/output/img/kaoyan-math/"
F = 13.0
SCRATCH = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(23)

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

def save_gif(frames, name, dur=600):
    pal = [f.convert("P", palette=Image.ADAPTIVE) for f in frames]
    pal[0].save(BASE + name, save_all=True, append_images=pal[1:], duration=dur, loop=0, optimize=True)
    print("ok", name, len(frames))

# 总体：三个格子（三个"群"），颜色表示类别比例不同
# 群 1、2、3 各在左中右
pts = []
groups = []
for g, (cx, cy) in enumerate([(2.0, 5.0), (6.0, 5.0), (10.0, 5.0)]):
    for _ in range(36):
        x = cx + rng.uniform(-1.5, 1.5); y = cy + rng.uniform(-2.4, 2.4)
        pts.append((x, y)); groups.append(g)
pts = np.array(pts); groups = np.array(groups)
# 每个个体再有一个"层"（颜色），三层比例在各群不同
strat = rng.choice([0, 1, 2], size=len(pts))
gcol = ["#b03a2e", "#d2691e", "#2f4f6f"]

def draw_pop(ax, sel, alpha_off=0.28, r=0.16):
    for i, (x, y) in enumerate(pts):
        on = i in sel
        ax.add_patch(Circle((x, y), r*1.45 if on else r, facecolor=gcol[strat[i]],
                            alpha=1.0 if on else alpha_off,
                            edgecolor=INK if on else "none", lw=1.3 if on else 0, zorder=3))
    for cx in [2.0, 6.0, 10.0]:
        ax.add_patch(Rectangle((cx-1.75, 2.3), 3.5, 5.4, fill=False,
                               edgecolor="#cfd6dd", lw=1.4, ls="--", zorder=1))

# =====================================================================
# 1) 整群抽样（cluster）：整块整块地抽
# =====================================================================
clusters = {0: list(np.where(groups == 0)[0]), 1: list(np.where(groups == 1)[0]),
            2: list(np.where(groups == 2)[0])}
chosen_cluster = 1
frames = []
for step in range(4):
    fig, ax = axes_(7.4, 4.4, (0, 15.6), (0, 9.6))
    sel = set()
    if step >= 1:
        sel |= set(clusters[0][:len(clusters[0])//3])
    if step >= 2:
        sel |= set(clusters[chosen_cluster])
    draw_pop(ax, sel)
    T(ax, 7.8, 9.0, "整群抽样：先分组，再整块抽", size=F)
    msg = ["总体分成 3 个群（每块一个群）",
           "不理想：只抽到群 1 的一小部分，群 2、3 没有代表",
           "抽中整个群 2：群 2 的全部个体都进样本",
           "整群抽样的优点：实施方便（跑一趟就能采一整块）"][step]
    T(ax, 7.8, 1.35, msg, size=F-2, color=INK)
    T(ax, 7.8, 0.65, "缺点：同一群内个体相似，样本代表性弱于分层抽样", size=F-3, color=GREY)
    fig.subplots_adjust(0.01, 0.02, 0.99, 0.98)
    frames.append(grab(fig, "clu"))
save_gif(frames, "comb-cluster.gif", dur=900)

# =====================================================================
# 2) 分层抽样：按比例分配 vs 等额分配
# =====================================================================
n_all = 120
pop = rng.uniform(0.6, 9.4, size=(n_all, 2))
strata = np.array([0]*60 + [1]*36 + [2]*24)       # 三层人数 60:36:24
rng.shuffle(strata)
scol = ["#b03a2e", "#d2691e", "#2f4f6f"]

def pop_frame(ax, sel):
    for i, (x, y) in enumerate(pop):
        on = i in sel
        ax.add_patch(Circle((x, y), 0.24 if on else 0.17, facecolor=scol[strata[i]],
                            alpha=1.0 if on else 0.25,
                            edgecolor=INK if on else "none", lw=1.3 if on else 0, zorder=3))
    ax.add_patch(Rectangle((0.3, 0.3), 9.4, 9.4, fill=False, edgecolor="#cfd6dd", lw=1.4, ls="--"))

frames = []
schemes = [("按比例分配", np.array([7, 4, 2])),
           ("等额分配", np.array([4, 4, 4]))]
for title, need in schemes:
    for step in range(need.sum()+1):
        fig, ax = axes_(6.8, 5.0, (0, 13.6), (0, 10.4))
        pools = [list(np.where(strata == k)[0]) for k in range(3)]
        for k in range(3):
            rng.shuffle(pools[k])
        taken = np.zeros(3, dtype=int); order = []
        while len(order) < step:
            for k in range(3):
                if taken[k] < need[k] and pools[k] and len(order) < step:
                    order.append(pools[k].pop()); taken[k] += 1
        pop_frame(ax, set(order))
        T(ax, 5.0, 10.0, "分层抽样：" + title, size=F)
        T(ax, 11.4, 8.4, "总体三层人数", size=F-2, color=GREY, ha="left")
        for k in range(3):
            T(ax, 11.4, 7.6 - k*0.85, "第 %d 层 %d 人" % (k+1, int(np.sum(strata == k))),
              size=F-3, color=scol[k], ha="left")
        T(ax, 11.4, 5.0, "本层抽 %d 个" % need[0], size=F-3, color=scol[0], ha="left")
        T(ax, 11.4, 4.3, "本层抽 %d 个" % need[1], size=F-3, color=scol[1], ha="left")
        T(ax, 11.4, 3.6, "本层抽 %d 个" % need[2], size=F-3, color=scol[2], ha="left")
        T(ax, 5.0, 1.15, "已抽：第1层 %d/%d，第2层 %d/%d，第3层 %d/%d"
          % (taken[0], need[0], taken[1], need[1], taken[2], need[2]), size=F-3, color=INK)
        note = ("按比例：人数多的层多抽，样本结构与总体一致（60:36:24 ≈ 7:4:2）"
                if title == "按比例分配" else
                "等额：每层抽一样多，适合关心「少数类」的情形（如罕见病）")
        T(ax, 5.0, 0.4, note, size=F-4, color=GREY)
        fig.subplots_adjust(0.01, 0.02, 0.99, 0.98)
        frames.append(grab(fig, "st3"))
save_gif(frames, "comb-stratified-alloc.gif", dur=420)

# =====================================================================
# 3) 随机：伪随机序列 vs 真随机
# =====================================================================
frames = []
for step in range(1, 13):
    fig, ax = axes_(7.6, 4.2, (0, 16.0), (0, 9.0))
    n = 24
    # 左：伪随机（线性同余），右：真随机
    x = 12345; seq_p = []
    for _ in range(n):
        x = (1103515245*x + 12345) % (2**31)
        seq_p.append(1 if x/(2**31) > 0.5 else 0)
    seq_t = list(rng.integers(0, 2, n))
    for row, (seq, lab, col) in enumerate([(seq_p, "伪随机（算法生成）", ORANGE),
                                           (seq_t, "真随机（物理过程）", GREEN)]):
        yy = 6.3 - row*3.0
        T(ax, 0.3, yy + 0.95, lab, size=F-3, color=col, ha="left")
        for i in range(min(step, n)):
            cx = 0.9 + i*0.62
            fc = col if seq[i] == 1 else "#f2f4f7"
            ax.add_patch(Circle((cx, yy), 0.24, facecolor=fc, edgecolor=col, lw=1.4, zorder=4))
            T(ax, cx, yy, str(seq[i]), size=F-4, color="white" if seq[i] == 1 else col)
    T(ax, 8.0, 8.55, "两种「随机数」的区别", size=F)
    T(ax, 8.0, 1.55, "伪随机：给定初值（种子）就能复现整串；规律藏在算法里，看着乱但是确定的",
      size=F-3, color=GREY)
    T(ax, 8.0, 0.95, "真随机：来自物理噪声（热噪声、放射性衰变），无法复现", size=F-3, color=GREY)
    T(ax, 8.0, 0.35, "日常程序里的随机数几乎都是伪随机：够用，且可复现便于调试", size=F-3, color=GREY)
    fig.subplots_adjust(0.01, 0.02, 0.99, 0.98)
    frames.append(grab(fig, "pr"))
save_gif(frames, "comb-random-types.gif", dur=380)
