"""Iris + 线性 SVM：最大间隔、支持向量、新样本判别"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import load_iris
from sklearn.svm import SVC
from PIL import Image
import os

plt.rcParams["font.family"] = ["PingFang SC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
INK = "#2b2b2b"
GREY, GREEN = "#8a8a8a", "#4a7c59"
BASE = "/Users/fred/Documents/GitHub/cycleuser/blog/output/img/kaoyan-math/"
F = 13.0
SCRATCH = os.path.dirname(os.path.abspath(__file__))

iris = load_iris()
X = iris.data[:, [2, 3]]              # 花瓣长、花瓣宽
y = iris.target
# 取 setosa(0) 与 versicolor(1) 两类
m = y < 2
Xs, ys = X[m], y[m]
SC = ["#b03a2e", "#d2691e", "#2f4f6f"]

clf = SVC(kernel="linear", C=1e6)
clf.fit(Xs, ys)
w = clf.coef_[0]; b = clf.intercept_[0]
sv = clf.support_vectors_

xmin, xmax = 0.8, 7.2
ymin, ymax = -0.2, 2.9

def line_y(x, w=w, b=b, off=0.0):
    # w0*x + w1*y + b = off  →  y = (off - b - w0*x)/w1
    return (off - b - w[0]*x)/w[1]

def axes_(w_, h_, equal=True):
    fig, ax = plt.subplots(figsize=(w_, h_), dpi=120)
    ax.set_xlim(xmin, xmax); ax.set_ylim(ymin, ymax)
    if equal: ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values(): sp.set_color("#d8dde3")
    return fig, ax

def T(ax, x, y_, s, size=F, color=INK, ha="center", va="center"):
    ax.text(x, y_, s, fontsize=size, color=color, ha=ha, va=va, zorder=10)

def grab(fig, tag):
    fp = os.path.join(SCRATCH, "_%s.png" % tag)
    fig.savefig(fp, dpi=120); plt.close(fig)
    im = Image.open(fp).convert("RGB"); os.remove(fp)
    return im

def save_gif(frames, name, dur=800):
    pal = [f.convert("P", palette=Image.ADAPTIVE) for f in frames]
    pal[0].save(BASE + name, save_all=True, append_images=pal[1:], duration=dur, loop=0, optimize=True)
    print("ok", name, len(frames))

xx = np.linspace(xmin, xmax, 200)
frames = []

# 阶段一：散点
for k in range(2):
    fig, ax = axes_(6.8, 5.2)
    for c in (0, 1):
        idx = np.where(ys == c)[0][: 60 if k == 0 else 200]
        ax.scatter(Xs[idx, 0], Xs[idx, 1], s=52, color=SC[c], alpha=0.9,
                   edgecolor="white", linewidth=0.8, zorder=4)
    T(ax, (xmin+xmax)/2, ymax+0.22, "Iris：setosa 与 versicolor 两类，只用两个特征", size=F-3)
    T(ax, (xmin+xmax)/2, ymin-0.28,
      "任务：找一条线把两类分开" if k == 0 else "两类明显可以分开——线性可分", size=F-4, color=GREY)
    fig.subplots_adjust(0.04, 0.07, 0.98, 0.94)
    frames.append(grab(fig, "svm"))

# 阶段二：多条候选线（间隔大小不同）
angles = [15, 30, 45, 60, 75]
for ang in angles:
    fig, ax = axes_(6.8, 5.2)
    for c in (0, 1):
        ax.scatter(Xs[ys == c, 0], Xs[ys == c, 1], s=52, color=SC[c], alpha=0.9,
                   edgecolor="white", linewidth=0.8, zorder=4)
    k = np.tan(np.deg2rad(ang))
    # 过某点的候选线
    x0, y0 = 2.6, 1.15
    ax.plot(xx, y0 + k*(xx-x0), color=GREY, lw=2.0, ls="-", zorder=5)
    T(ax, (xmin+xmax)/2, ymax+0.22, "很多条线都能把两类分开，哪条更好？", size=F-3)
    T(ax, (xmin+xmax)/2, ymin-0.28, "倾斜角 %d°：这条也能分开，但离样本太近" % ang, size=F-4, color=GREY)
    fig.subplots_adjust(0.04, 0.07, 0.98, 0.94)
    frames.append(grab(fig, "svm2"))

# 阶段三：最大间隔 + 支持向量
for t in np.linspace(0, 1, 3):
    fig, ax = axes_(6.8, 5.2)
    for c in (0, 1):
        ax.scatter(Xs[ys == c, 0], Xs[ys == c, 1], s=52, color=SC[c], alpha=0.9,
                   edgecolor="white", linewidth=0.8, zorder=4)
    yc = line_y(xx, off=0)
    ax.fill_between(xx, line_y(xx, off=-1), line_y(xx, off=1), color=GREEN, alpha=0.10, zorder=2)
    ax.plot(xx, yc, color=GREEN, lw=2.8, zorder=6)
    ax.plot(xx, line_y(xx, off=1), color=GREEN, lw=1.6, ls="--", zorder=5)
    ax.plot(xx, line_y(xx, off=-1), color=GREEN, lw=1.6, ls="--", zorder=5)
    if t > 0.4:
        ax.scatter(sv[:, 0], sv[:, 1], s=210, facecolor="none", edgecolor=INK,
                   linewidth=1.8, zorder=7)
    T(ax, (xmin+xmax)/2, ymax+0.22, "SVM（support vector machine，支持向量机）", size=F-3)
    msg = ("SVM 选「离两类都尽量远」的那条线，两条虚线之间是间隔（margin）" if t <= 0.4
           else "压住虚线的点叫支持向量（support vector）：只有它们决定了边界位置")
    T(ax, (xmin+xmax)/2, ymin-0.28, msg, size=F-4, color=GREY)
    fig.subplots_adjust(0.04, 0.07, 0.98, 0.94)
    frames.append(grab(fig, "svm3"))

# 阶段四：新样本 → 判别
q = np.array([5.9, 1.55])
for step in range(3):
    fig, ax = axes_(6.8, 5.2)
    for c in (0, 1):
        ax.scatter(Xs[ys == c, 0], Xs[ys == c, 1], s=52, color=SC[c], alpha=0.9,
                   edgecolor="white", linewidth=0.8, zorder=4)
    ax.fill_between(xx, line_y(xx, off=-1), line_y(xx, off=1), color=GREEN, alpha=0.10, zorder=2)
    ax.plot(xx, line_y(xx, off=0), color=GREEN, lw=2.8, zorder=6)
    ax.plot(xx, line_y(xx, off=1), color=GREEN, lw=1.6, ls="--", zorder=5)
    ax.plot(xx, line_y(xx, off=-1), color=GREEN, lw=1.6, ls="--", zorder=5)
    ax.scatter(sv[:, 0], sv[:, 1], s=210, facecolor="none", edgecolor=INK,
               linewidth=1.8, zorder=7)
    side = float(np.dot(w, q) + b)
    col = SC[1] if side > 0 else SC[0]
    pos = [q, q + np.array([-0.45, 0.30]), q + np.array([-0.9, 0.55])][step]
    ax.plot([pos[0]], [pos[1]], marker="s", ms=15, mfc="white", mec=col, mew=2.4, zorder=8)
    T(ax, (xmin+xmax)/2, ymax+0.22, "新样本来了，判它属于哪一类", size=F-3)
    if step == 0:
        msg = "新样本（空心方块）：花瓣长 %.1f cm，花瓣宽 %.1f cm，没有标签" % (q[0], q[1])
    elif step == 1:
        msg = "把它放进图里，看它落在边界哪一侧"
    else:
        msg = "落在 versicolor 一侧 → 判为 versicolor（判别结果就是「哪一侧」）"
    T(ax, (xmin+xmax)/2, ymin-0.28, msg, size=F-4, color=col if step == 2 else GREY)
    if step == 2:
        T(ax, pos[0]+0.15, pos[1]+0.30, "判为 versicolor", size=F-4, color=col, ha="left")
    fig.subplots_adjust(0.04, 0.07, 0.98, 0.94)
    frames.append(grab(fig, "svm4"))

save_gif(frames, "iris-svm.gif", dur=900)
