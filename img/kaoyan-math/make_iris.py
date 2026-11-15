"""Iris 数据集上的聚类与降维动画"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_iris
from PIL import Image
import os

plt.rcParams["font.family"] = ["PingFang SC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
INK = "#2b2b2b"
BLUE, GREY, GREEN, ORANGE = "#2f4f6f", "#8a8a8a", "#4a7c59", "#d2691e"
BASE = "/Users/fred/Documents/GitHub/cycleuser/blog/output/img/kaoyan-math/"
F = 13.5
SCRATCH = os.path.dirname(os.path.abspath(__file__))

iris = load_iris()
X4 = iris.data                      # 150 × 4
y = iris.target                     # 0/1/2 = setosa / versicolor / virginica
FEAT = ["花萼长", "花萼宽", "花瓣长", "花瓣宽"]
SPEC = ["setosa", "versicolor", "virginica"]
SC = ["#b03a2e", "#d2691e", "#2f4f6f"]
rng = np.random.default_rng(5)

def axes_(w, h, xlim, ylim, equal=True):
    fig, ax = plt.subplots(figsize=(w, h), dpi=120)
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    if equal: ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values(): sp.set_color("#d8dde3")
    return fig, ax

def T(ax, x, y_, s, size=F, color=INK, ha="center", va="center"):
    ax.text(x, y_, s, fontsize=size, color=color, ha=ha, va=va, zorder=9)

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
# 1) 聚类：花瓣长 × 花瓣宽（2 个特征），k-means，不告诉它种类
# =====================================================================
X = X4[:, [2, 3]]
xmin, xmax = X[:, 0].min()-0.4, X[:, 0].max()+0.6
ymin, ymax = X[:, 1].min()-0.3, X[:, 1].max()+0.4

cent = np.array([[2.0, 0.4], [4.8, 1.3], [6.2, 2.0]])
def assign(X, cent):
    return ((X[:, None, :]-cent[None, :, :])**2).sum(axis=2).argmin(axis=1)

hist = [(cent.copy(), assign(X, cent))]
for _ in range(5):
    lab = assign(X, hist[-1][0])
    hist.append((np.array([X[lab == j].mean(axis=0) for j in range(3)]), None))
    hist[-1] = (hist[-1][0], assign(X, hist[-1][0]))

frames = []
for idx, (c, lab) in enumerate(hist):
    fig, ax = axes_(6.8, 5.2, (xmin, xmax), (ymin, ymax))
    for j in range(3):
        if np.any(lab == j):
            ax.scatter(X[lab == j, 0], X[lab == j, 1], s=56, color=SC[j], alpha=0.9,
                       edgecolor="white", linewidth=0.9, zorder=4)
        ax.plot([c[j, 0]], [c[j, 1]], marker="*", ms=26, color=SC[j],
                markeredgecolor=INK, markeredgewidth=1.0, zorder=6)
    ax.set_xlabel("花瓣长（cm）", fontsize=F-4, color=GREY)
    ax.set_ylabel("花瓣宽（cm）", fontsize=F-4, color=GREY)
    ax.tick_params(colors=GREY, labelsize=F-5)
    names = ["起点：随机放 3 个中心（算法不知道有几类，是我们指定的 $k=3$）",
             "第 1 轮：按最近的中心染色，再把中心移到本组平均位置",
             "第 2 轮：重新染色，中心继续挪",
             "第 3 轮：分组基本稳定",
             "第 4 轮：不再变化，收敛",
             "结果：三簇分得很开；对照真实种类，聚类几乎还原了三个物种"]
    T(ax, (xmin+xmax)/2, ymax+0.42, "Iris 数据集：150 朵鸢尾花，只用两个特征做聚类", size=F-3)
    T(ax, (xmin+xmax)/2, ymin-0.42, names[min(idx, len(names)-1)], size=F-5, color=INK)
    fig.subplots_adjust(0.09, 0.11, 0.98, 0.93)
    frames.append(grab(fig, "km"))

# 末帧：与真实种类对照
fig, ax = axes_(6.8, 5.2, (xmin, xmax), (ymin, ymax))
for j in range(3):
    ax.scatter(X[y == j, 0], X[y == j, 1], s=56, color=SC[j], alpha=0.9,
               edgecolor="white", linewidth=0.9, zorder=4)
    T(ax, xmax-0.1, ymax-0.25-j*0.33, SPEC[j], size=F-5, color=SC[j], ha="right")
ax.set_xlabel("花瓣长（cm）", fontsize=F-4, color=GREY)
ax.set_ylabel("花瓣宽（cm）", fontsize=F-4, color=GREY)
ax.tick_params(colors=GREY, labelsize=F-5)
T(ax, (xmin+xmax)/2, ymax+0.42, "对照：按真实物种上色（聚类时并没有用这个信息）", size=F-3)
T(ax, (xmin+xmax)/2, ymin-0.42, "setosa 完全分离；versicolor 与 virginica 有少量交叠", size=F-5, color=INK)
fig.subplots_adjust(0.09, 0.11, 0.98, 0.93)
frames.append(grab(fig, "km2"))
save_gif(frames, "iris-clustering.gif", dur=900)

# =====================================================================
# 2) 降维：4 个特征 → PCA 降到 2 维
# =====================================================================
Xc = X4 - X4.mean(axis=0)
U, S, Vt = np.linalg.svd(Xc, full_matrices=False)
Z2 = Xc @ Vt[:2].T          # 150 × 2
explained = (S**2)/(S**2).sum()

frames = []
# 阶段1：3 维视角（取前三个特征），旋转
for ang in range(0, 300, 50):
    fig = plt.figure(figsize=(6.8, 5.4), dpi=120)
    ax = fig.add_subplot(111, projection="3d")
    for j in range(3):
        ax.scatter(X4[y == j, 0], X4[y == j, 1], X4[y == j, 2],
                   s=24, color=SC[j], alpha=0.85, depthshade=False)
    ax.view_init(elev=18, azim=ang)
    ax.set_xlabel(FEAT[0], fontsize=F-6, color=GREY)
    ax.set_ylabel(FEAT[1], fontsize=F-6, color=GREY)
    ax.set_zlabel(FEAT[2], fontsize=F-6, color=GREY)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
    ax.set_box_aspect((1, 1, 1))
    ax.set_title("Iris 有 4 个特征；先看其中 3 个", fontsize=F-3, pad=2)
    fig.subplots_adjust(0.02, 0.02, 0.98, 0.94)
    frames.append(grab(fig, "pc"))

# 阶段2：投影到 2 维
for t in np.linspace(0, 1, 5):
    fig, ax = axes_(6.8, 5.2, (Z2[:, 0].min()-0.8, Z2[:, 0].max()+0.8),
                    (Z2[:, 1].min()-0.8, Z2[:, 1].max()+0.8))
    for j in range(3):
        ax.scatter(Z2[y == j, 0], Z2[y == j, 1], s=52, color=SC[j], alpha=0.9,
                   edgecolor="white", linewidth=0.8, zorder=4)
    ax.annotate("", xy=(Z2[:, 0].max()+0.5, 0), xytext=(Z2[:, 0].min()-0.5, 0),
                arrowprops=dict(arrowstyle="->", color=GREY, lw=1.3))
    ax.annotate("", xy=(0, Z2[:, 1].max()+0.5), xytext=(0, Z2[:, 1].min()-0.5),
                arrowprops=dict(arrowstyle="->", color=GREY, lw=1.3))
    T(ax, Z2[:, 0].max()+0.55, -0.55, "第1主成分", size=F-5, color=GREY, ha="right")
    T(ax, 0.35, Z2[:, 1].max()+0.35, "第2主成分", size=F-5, color=GREY, ha="left")
    T(ax, 0, Z2[:, 1].max()+1.35, "把 4 维数据投影到 2 维（PCA）", size=F-2)
    T(ax, 0, Z2[:, 1].min()-1.15,
      "两个主成分保留了 %.0f%% 的信息；三个物种在平面上清楚分开" % ((explained[:2].sum())*100),
      size=F-3, color=GREY)
    fig.subplots_adjust(0.06, 0.12, 0.97, 0.93)
    frames.append(grab(fig, "pc2"))
save_gif(frames, "iris-dimreduce.gif", dur=800)

# 阶段3：解释方差柱状图（单帧，作为 gif 末尾）
fig, ax = axes_(6.2, 4.4, (0, 4), (0, 1), equal=False)
ax.bar([1, 2, 3, 4], explained, color=[ORANGE, ORANGE, "#c9ced4", "#c9ced4"],
       edgecolor="white", width=0.62)
ax.set_xticks([1, 2, 3, 4]); ax.set_xticklabels(["PC1", "PC2", "PC3", "PC4"], color=GREY, fontsize=F-4)
ax.set_yticks([])
for i, v in enumerate(explained):
    T(ax, i+1, v+0.035, "%.0f%%" % (v*100), size=F-4, color=INK)
T(ax, 2, 0.98, "每个主成分解释的方差比例", size=F-2)
T(ax, 2, -0.12, "前两个主成分合起来 %.0f%%，所以压到 2 维几乎不丢信息" % (explained[:2].sum()*100),
  size=F-4, color=GREY)
fig.subplots_adjust(0.04, 0.14, 0.98, 0.94)
fig.savefig(BASE + "iris-pca-variance.png", dpi=170); plt.close(fig)
print("ok iris-pca-variance.png")
