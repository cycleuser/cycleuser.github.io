"""Iris 花瓣长的密度估计：直方图 → KDE"""
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
petal = iris.data[:, 2]          # 花瓣长 cm
species = iris.target
SC = ["#b03a2e", "#d2691e", "#2f4f6f"]

def axes_(w, h):
    fig, ax = plt.subplots(figsize=(w, h), dpi=120)
    ax.set_xlim(0.6, 7.4); ax.set_ylim(-0.09, 1.30)
    ax.set_xticks([1, 2, 3, 4, 5, 6, 7])
    ax.set_yticks([])
    ax.tick_params(colors=GREY, labelsize=F-4)
    for sp in ax.spines.values(): sp.set_color("#d8dde3")
    ax.set_xlabel("花瓣长（cm）", fontsize=F-4, color=GREY)
    return fig, ax

def T(ax, x, y, s, size=F, color=INK, ha="center", va="center"):
    ax.text(x, y, s, fontsize=size, color=color, ha=ha, va=va, zorder=10,
            transform=ax.transData)

def grab(fig, tag):
    fp = os.path.join(SCRATCH, "_%s.png" % tag)
    fig.savefig(fp, dpi=120); plt.close(fig)
    im = Image.open(fp).convert("RGB"); os.remove(fp)
    return im

def save_gif(frames, name, dur=900):
    pal = [f.convert("P", palette=Image.ADAPTIVE) for f in frames]
    pal[0].save(BASE + name, save_all=True, append_images=pal[1:], duration=dur, loop=0, optimize=True)
    print("ok", name, len(frames))

frames = []
# 1) 直方图，区间数递增
for nb in [4, 8, 14, 24]:
    fig, ax = axes_(7.2, 4.4)
    h, edges = np.histogram(petal, bins=nb, density=True)
    ax.bar((edges[:-1]+edges[1:])/2, h, width=(edges[1]-edges[0])*0.9,
           color=BLUE, alpha=0.32, edgecolor=BLUE, lw=1.2, zorder=3)
    ax.scatter(petal, np.full_like(petal, -0.045), s=15, color=ORANGE, alpha=0.8, zorder=4)
    T(ax, 4.0, 1.24, "Iris：150 朵花的花瓣长（cm）", size=F-1)
    T(ax, 4.0, 1.14, "直方图 %d 个区间：越细越贴合样本，也越抖" % nb, size=F-3, color=GREY)
    T(ax, 4.0, -0.075, "橙色小点：150 个样本值", size=F-4, color=ORANGE)
    fig.subplots_adjust(0.05, 0.14, 0.98, 0.95)
    frames.append(grab(fig, "de"))

# 2) KDE，两个带宽
xs = np.linspace(0.6, 7.4, 500)
for bw, note in [(0.45, "带宽 0.45：两个峰清楚地分开"),
                 (0.22, "带宽 0.22：太细，出现毛刺（过拟合）"),
                 (0.30, "带宽 0.30：折中")]:
    dens = np.exp(-0.5*((xs[:, None]-petal[None, :])/bw)**2).sum(axis=1)
    dens = dens/(len(petal)*bw*np.sqrt(2*np.pi))
    fig, ax = axes_(7.2, 4.4)
    ax.scatter(petal, np.full_like(petal, -0.045), s=15, color=ORANGE, alpha=0.8, zorder=4)
    ax.plot(xs, dens, color=GREEN, lw=2.6, zorder=6)
    ax.fill_between(xs, 0, dens, color=GREEN, alpha=0.12, zorder=2)
    T(ax, 4.0, 1.24, "核密度估计（kernel density estimation，KDE）", size=F-1)
    T(ax, 4.0, 1.14, note, size=F-3, color=GREY)
    T(ax, 4.0, -0.075, "每个样本换成一个高斯小鼓包，全部叠起来再归一化", size=F-4, color=GREEN)
    fig.subplots_adjust(0.05, 0.14, 0.98, 0.95)
    frames.append(grab(fig, "de2"))

# 3) 按物种上色，解释双峰来源
fig, ax = axes_(7.2, 4.4)
dens = np.exp(-0.5*((xs[:, None]-petal[None, :])/0.45)**2).sum(axis=1)
dens = dens/(len(petal)*0.45*np.sqrt(2*np.pi))
ax.plot(xs, dens, color=GREEN, lw=2.6, zorder=6)
ax.fill_between(xs, 0, dens, color=GREEN, alpha=0.12, zorder=2)
for c in range(3):
    ax.scatter(petal[species == c], np.full((species == c).sum(), -0.05 - c*0.012),
               s=16, color=SC[c], alpha=0.9, zorder=5)
    ax.text(6.55, -0.05 - c*0.012, ["setosa", "versicolor", "virginica"][c],
            fontsize=F-5, color=SC[c], ha="right", va="center")
T(ax, 4.0, 1.24, "双峰来自物种差异", size=F-1)
T(ax, 4.0, 1.14, "setosa 花瓣短（左峰），另两类的花瓣长（右峰）", size=F-3, color=GREY)
T(ax, 2.0, 0.30, "左峰：setosa", size=F-4, color=SC[0])
T(ax, 5.2, 0.55, "右峰：versicolor + virginica", size=F-4, color=SC[2])
fig.subplots_adjust(0.05, 0.14, 0.98, 0.95)
frames.append(grab(fig, "de3"))

save_gif(frames, "iris-density.gif", dur=1000)
