"""帕斯卡恒等式文章配图"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, FancyBboxPatch, FancyArrowPatch
import matplotlib.patches as mp
from math import comb
import os

plt.rcParams["font.family"] = ["PingFang SC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
INK = "#2b2b2b"
GREY, GREEN, ORANGE = "#8a8a8a", "#4a7c59", "#d2691e"
RED, BLUE, PURPLE = "#b03a2e", "#2f4f6f", "#6b4c9a"
BASE = os.path.dirname(os.path.abspath(__file__)) + "/"
F = 14

def T(ax, x, y, s, size=F, color=INK, ha="center", va="center", weight="normal"):
    ax.text(x, y, s, fontsize=size, color=color, ha=ha, va=va, zorder=10, weight=weight)

def axes_(w, h, xlim, ylim, equal=True):
    fig, ax = plt.subplots(figsize=(w, h), dpi=170)
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    if equal: ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values(): sp.set_color("none")
    return fig, ax

# ============ 图1：杨辉三角与加法规则 ============
fig, ax = axes_(8.4, 6.4, (-0.4, 8.4), (-1.3, 7.4))
rows = 8
for n in range(rows):
    vals = [comb(n, k) for k in range(n+1)]
    for k, v in enumerate(vals):
        x = 4.0 + (k - n/2)*0.92
        y = 6.6 - n*0.86
        hl = (n, k) in [(4, 2), (3, 1), (3, 2)]
        col = RED if (n, k) == (4, 2) else (ORANGE if (n, k) in [(3, 1), (3, 2)] else INK)
        if hl:
            ax.add_patch(Circle((x, y), 0.33, facecolor="#fdeee8" if (n, k) == (4, 2) else "#fdf1e6",
                                edgecolor=col, lw=1.6, zorder=4))
        T(ax, x, y, str(v), size=F - (1 if v < 100 else 2), color=col)
# 标注箭头
x42 = 4.0 + (2 - 2)*0.92; y42 = 6.6 - 4*0.86
x31 = 4.0 + (1 - 1.5)*0.92; y31 = 6.6 - 3*0.86
x32 = 4.0 + (2 - 1.5)*0.92; y32 = 6.6 - 3*0.86
for (xs, ys) in [(x31, y31), (x32, y32)]:
    ax.annotate("", xy=(x42, y42 + 0.34), xytext=(xs, ys - 0.34),
                arrowprops=dict(arrowstyle="-|>", color=GREY, lw=1.4,
                                connectionstyle="arc3,rad=0.0"))
T(ax, 4.0, -0.55, "第 $n$ 行第 $k$ 个数是 $C_n^k$；每个数 ＝ 上方两数之和", size=F-4, color=GREY)
T(ax, 7.4, 7.0, "杨辉三角（贾宪三角）", size=F, color=INK)
T(ax, 7.4, 0.2, "$C_4^2=6=3+3=C_3^1+C_3^2$", size=F+1, color=RED)
fig.subplots_adjust(0.01, 0.01, 0.99, 0.99)
fig.savefig(BASE + "pascal-triangle-rule.png", dpi=170); plt.close(fig)
print("ok 1")

# ============ 图2：组合证明（5 选 3，按含不含 a 分两类）============
fig, ax = axes_(9.2, 5.4, (0, 17.2), (0, 10.2))
elems = ["a", "b", "c", "d", "e"]
AX, AY = 1.6, 5.0
for i, e in enumerate(elems):
    x = 0.9 + i*1.5
    ax.add_patch(Circle((x, 8.4), 0.42, facecolor="white" if e != "a" else "#fdeee8",
                        edgecolor=RED if e == "a" else INK, lw=2.0, zorder=5))
    T(ax, x, 8.4, e, size=F, color=RED if e == "a" else INK)
T(ax, 4.4, 9.35, "5 个元素：选中 3 个", size=F-1)

# 左：含 a
T(ax, 4.0, 6.55, "含 $a$：再从 4 个里选 2 个", size=F-3, color=RED)
combos_with = [("a","b","c"), ("a","b","d"), ("a","b","e"), ("a","c","d"), ("a","c","e"), ("a","d","e")]
for i, cb in enumerate(combos_with):
    x = 1.0 + (i % 3)*2.9; y = 5.2 - (i // 3)*1.35
    ax.add_patch(FancyBboxPatch((x-0.62, y-0.34), 2.0, 0.68, boxstyle="round,pad=0.04",
                                facecolor="#fdeee8", edgecolor=RED, lw=1.4, zorder=4))
    T(ax, x+0.38, y, "{" + ",".join(cb) + "}", size=F-4, color=RED)
T(ax, 4.0, 2.35, "共 $C_4^2=6$ 种", size=F-2, color=RED)

# 右：不含 a
T(ax, 12.8, 6.55, "不含 $a$：从其余 4 个里选 3 个", size=F-3, color=BLUE)
combos_wo = [("b","c","d"), ("b","c","e"), ("b","d","e"), ("c","d","e")]
for i, cb in enumerate(combos_wo):
    x = 10.4 + (i % 2)*3.0; y = 5.2 - (i // 2)*1.35
    ax.add_patch(FancyBboxPatch((x-0.62, y-0.34), 2.0, 0.68, boxstyle="round,pad=0.04",
                                facecolor="#eaf0f6", edgecolor=BLUE, lw=1.4, zorder=4))
    T(ax, x+0.38, y, "{" + ",".join(cb) + "}", size=F-4, color=BLUE)
T(ax, 12.8, 2.35, "共 $C_4^3=4$ 种", size=F-2, color=BLUE)
T(ax, 8.6, 1.15, "$6+4=10=C_5^3$，两类不重不漏", size=F+1, color=GREEN)
fig.subplots_adjust(0.01, 0.02, 0.99, 0.98)
fig.savefig(BASE + "pascal-comb-proof.png", dpi=170); plt.close(fig)
print("ok 2")

# ============ 图3：历史时间线 ============
fig, ax = axes_(10.4, 4.2, (0, 20.8), (0, 8.4), equal=False)
events = [
    ("公元前 2—3 世纪", "印度《韵律经》\n（平伽拉）", "数诗律组合\n相当于三角形", 1.4),
    ("约 1000 年", "波斯 凯拉吉\n（al-Karaji）", "已明确写出\n三角形数表", 5.0),
    ("约 1050 年", "北宋 贾宪\n《释锁算书》", "中国最早记载\n（今称贾宪三角）", 8.6),
    ("约 1070 年", "波斯 奥马尔·海亚姆", "用于开高次方\n伊朗称海亚姆三角", 12.2),
    ("1261 年", "南宋 杨辉\n《详解九章算法》", "引贾宪之法\n中国称杨辉三角", 15.8),
    ("1654 年", "法国 帕斯卡", "《算术三角形论》\n给出归纳证明", 19.4),
]
ax.plot([0.6, 20.2], [4.4, 4.4], color="#cfd6dd", lw=3.0, zorder=2)
for label, who, what, x in events:
    col = ORANGE if ("贾宪" in who or "杨辉" in who) else (RED if "帕斯卡" in who else BLUE)
    ax.plot([x], [4.4], "o", ms=13, mfc="white", mec=col, mew=2.6, zorder=5)
    T(ax, x, 5.35, label, size=F-4, color=GREY)
    T(ax, x, 6.25, who, size=F-4, color=col)
    T(ax, x, 2.95, what, size=F-4.5, color=INK)
T(ax, 10.4, 7.7, "同一个三角形的五百年流传", size=F+1)
T(ax, 10.4, 1.35, "帕斯卡不是发明者，是第一个把它写成\"证明\"的人", size=F-3, color=GREY)
fig.subplots_adjust(0.01, 0.02, 0.99, 0.98)
fig.savefig(BASE + "pascal-history.png", dpi=170); plt.close(fig)
print("ok 3")

# ============ 图4：曲棍球棒恒等式 ============
fig, ax = axes_(7.6, 6.4, (-0.5, 8.0), (-2.0, 7.2))
rows = 8
hl_cells = []
for n in range(rows):
    for k in range(0, n+1):
        x = 3.8 + (k - n/2)*0.90
        y = 6.5 - n*0.86
        v = comb(n, k)
        on = (k == 2) and n >= 2          # 第 2 列
        T(ax, x, y, str(v), size=F-2.5, color=ORANGE if on else INK)
        if on:
            ax.add_patch(Circle((x, y), 0.30, facecolor="none", edgecolor=ORANGE, lw=1.8, zorder=4))
        if n == 5 and k == 3:
            ax.add_patch(Circle((x, y), 0.32, facecolor="none", edgecolor=RED, lw=2.2, zorder=5))
T(ax, 6.9, 6.9, "曲棍球棒恒等式", size=F-1)
T(ax, 3.6, -1.05, "$C_2^2+C_3^2+C_4^2=1+3+6=10=C_5^3$", size=F-2.5, color=RED)
T(ax, 3.6, -1.75, "沿一列加到头，等于拐角那个数（形状像曲棍球棒）", size=F-4, color=GREY)
fig.subplots_adjust(0.01, 0.02, 0.99, 0.98)
fig.savefig(BASE + "pascal-hockey-stick.png", dpi=170); plt.close(fig)
print("ok 4")
