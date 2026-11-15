"""无监督三个任务：聚类、降维、密度估计"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Ellipse
from PIL import Image
import os

plt.rcParams["font.family"] = ["PingFang SC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
INK = "#2b2b2b"
BLUE, GREY, GREEN, ORANGE = "#2f4f6f", "#8a8a8a", "#4a7c59", "#d2691e"
RED, PURPLE = "#b03a2e", "#6b4c9a"
BASE = "/Users/fred/Documents/GitHub/cycleuser/blog/output/img/kaoyan-math/"
F = 13.5
SCRATCH = os.path.dirname(os.path.abspath(__file__))
rng = np.random.default_rng(31)

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

def save_gif(frames, name, dur=700):
    pal = [f.convert("P", palette=Image.ADAPTIVE) for f in frames]
    pal[0].save(BASE + name, save_all=True, append_images=pal[1:], duration=dur, loop=0, optimize=True)
    print("ok", name, len(frames))

# =====================================================================
# 1) 聚类（k-means）
# =====================================================================
centers_true = np.array([[2.6, 6.6], [6.6, 3.0], [9.6, 7.2]])
X = np.vstack([rng.normal(c, 0.75, size=(26, 2)) for c in centers_true])
k = 3
cent = np.array([[3.4, 2.6], [8.6, 2.9], [7.4, 7.6]])
CC = ["#b03a2e", "#d2691e", "#2f4f6f"]

def assign(X, cent):
    d = ((X[:, None, :] - cent[None, :, :])**2).sum(axis=2)
    return d.argmin(axis=1)

frames = []
hist = [(cent.copy(), assign(X, cent))]
for it in range(4):
    lab = assign(X, hist[-1][0])
    newc = np.array([X[lab == j].mean(axis=0) for j in range(k)])
    hist.append((newc.copy(), assign(X, newc)))

for idx, (c, lab) in enumerate(hist):
    fig, ax = axes_(6.8, 5.0, (0, 13.6), (0, 10.6))
    for j in range(k):
        ax.scatter(X[lab == j, 0], X[lab == j, 1], s=52, color=CC[j], alpha=0.85,
                   edgecolor="white", linewidth=0.9, zorder=4)
        ax.plot([c[j, 0]], [c[j, 1]], marker="*", ms=24, color=CC[j],
                markeredgecolor=INK, markeredgewidth=1.0, zorder=6)
    T(ax, 6.8, 10.1, "聚类（clustering）：没有标签，让数据自己分组", size=F-1)
    T(ax, 6.8, 1.3, ["第 %d 步：随机放 3 个中心，按最近中心把点染成三色" % 0,
                     "第 1 步：把每个中心移到本组点的平均位置",
                     "第 2 步：重新分组，中心再移动",
                     "第 3 步：分组不再变化，收敛",
                     "结束：得到 3 个簇，但「谁是谁」仍需人来解释"][idx], size=F-2, color=INK)
    T(ax, 6.8, 0.6, "★ ＝簇中心（centroid）", size=F-3, color=GREY)
    fig.subplots_adjust(0.01, 0.02, 0.99, 0.98)
    frames.append(grab(fig, "km"))
save_gif(frames, "comb-clustering.gif", dur=950)

# =====================================================================
# 2) 降维（3D → 2D 投影）
# =====================================================================
base = rng.normal(0, 1, size=(90, 2))
Amat = np.array([[1.0, 0.35], [0.2, 0.9], [0.55, -0.3]])
P3 = base @ Amat.T
P3 = P3 + rng.normal(0, 0.10, size=P3.shape)

mean = P3.mean(axis=0)
Pc = P3 - mean
U, S, Vt = np.linalg.svd(Pc, full_matrices=False)
e1, e2 = Vt[0], Vt[1]

frames = []
for ang in range(0, 300, 50):
    fig = plt.figure(figsize=(6.8, 5.4), dpi=120)
    ax = fig.add_subplot(111, projection="3d")
    # 数据所在的平面
    g = np.linspace(-3.2, 3.2, 12)
    G1, G2 = np.meshgrid(g, g)
    Xp = mean[0] + G1*e1[0] + G2*e2[0]
    Yp = mean[1] + G1*e1[1] + G2*e2[1]
    Zp = mean[2] + G1*e1[2] + G2*e2[2]
    ax.plot_surface(Xp, Yp, Zp, color=GREEN, alpha=0.12, linewidth=0)
    ax.scatter(P3[:, 0], P3[:, 1], P3[:, 2], s=24, color=BLUE, alpha=0.85, depthshade=False)
    ax.view_init(elev=20, azim=ang)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
    ax.set_box_aspect((1, 1, 1))
    ax.set_title("三维数据其实躺在一张薄面（绿面）上", fontsize=F-2.5, pad=2)
    fig.subplots_adjust(0.02, 0.02, 0.98, 0.94)
    frames.append(grab(fig, "dr"))

proj = Pc @ Vt[:2].T
for t in np.linspace(0, 1, 5):
    fig, ax = axes_(6.8, 5.0, (-7, 7), (-5.5, 5.5))
    # 平面内坐标 → 屏幕
    scr = np.column_stack([proj[:, 0], proj[:, 1]])
    ax.scatter(scr[:, 0], scr[:, 1], s=30, color=BLUE, alpha=0.85, edgecolor="none", zorder=4)
    ax.annotate("", xy=(5.6, 0), xytext=(-5.6, 0),
                arrowprops=dict(arrowstyle="->", color=GREY, lw=1.4))
    ax.annotate("", xy=(0, 4.4), xytext=(0, -4.4),
                arrowprops=dict(arrowstyle="->", color=GREY, lw=1.4))
    T(ax, 5.9, 0.35, "第一主成分", size=F-3, color=GREY, ha="left")
    T(ax, 0.35, 4.6, "第二主成分", size=F-3, color=GREY, ha="left")
    T(ax, 0, 5.15, "把点投影到绿面上，只剩两个坐标", size=F-2)
    T(ax, 0, -5.2, "降维（dimensionality reduction）：用更少的坐标描述同一批数据；PCA 让投影后点尽量散开",
      size=F-4, color=GREY)
    fig.subplots_adjust(0.02, 0.03, 0.98, 0.98)
    frames.append(grab(fig, "dr2"))
save_gif(frames, "comb-dimreduce.gif", dur=800)

# =====================================================================
# 3) 密度估计（直方图 → 平滑曲线）
# =====================================================================
samp = np.concatenate([rng.normal(3.2, 0.9, 120), rng.normal(7.0, 1.2, 80)])
xs = np.linspace(-1, 11, 400)
frames = []
bins_list = [4, 8, 14, 22]
for nb in bins_list:
    fig, ax = axes_(7.2, 4.4, (-1, 11), (-0.06, 0.62))
    ax.set_aspect("auto")
    h, edges = np.histogram(samp, bins=nb, density=True)
    ax.bar((edges[:-1]+edges[1:])/2, h, width=(edges[1]-edges[0])*0.92,
           color=BLUE, alpha=0.35, edgecolor=BLUE, lw=1.2)
    ax.scatter(samp, np.full_like(samp, -0.012), s=16, color=ORANGE, alpha=0.75, zorder=5)
    ax.set_yticks([]); ax.set_xticks([])
    for sp in ax.spines.values(): sp.set_color("#d8dde3")
    T(ax, 5.0, 0.56, "密度估计：估计数据本身的分布", size=F-1)
    T(ax, 5.0, 0.49, "直方图 %d 个区间：区间越多越细，但越抖" % nb, size=F-3, color=GREY)
    T(ax, 5.0, -0.045, "橙色小点是样本（一维数据）", size=F-4, color=ORANGE)
    fig.subplots_adjust(0.02, 0.06, 0.98, 0.96)
    frames.append(grab(fig, "de"))

# 平滑核密度估计
for bw in [0.55, 0.35]:
    dens = np.exp(-0.5*((xs[:, None]-samp[None, :])/bw)**2).sum(axis=1)
    dens = dens/(len(samp)*bw*np.sqrt(2*np.pi))
    fig, ax = axes_(7.2, 4.4, (-1, 11), (-0.06, 0.62))
    ax.set_aspect("auto")
    ax.scatter(samp, np.full_like(samp, -0.012), s=16, color=ORANGE, alpha=0.75, zorder=5)
    ax.plot(xs, dens, color=GREEN, lw=2.6, zorder=6)
    ax.fill_between(xs, 0, dens, color=GREEN, alpha=0.12)
    ax.set_yticks([]); ax.set_xticks([])
    for sp in ax.spines.values(): sp.set_color("#d8dde3")
    T(ax, 5.0, 0.56, "核密度估计（kernel density estimation, KDE）", size=F-2)
    T(ax, 5.0, 0.49, "把每个样本换成一个「小鼓包」，全部叠起来再归一化", size=F-3, color=GREY)
    T(ax, 5.0, -0.045, "带宽（bandwidth）越大越平滑，越小越贴着样本", size=F-4, color=GREEN)
    fig.subplots_adjust(0.02, 0.06, 0.98, 0.96)
    frames.append(grab(fig, "de2"))
save_gif(frames, "comb-density.gif", dur=900)
