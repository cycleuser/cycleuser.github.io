import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Rectangle, FancyArrowPatch, Polygon

plt.rcParams["font.family"] = ["PingFang SC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

INK    = "#2b2b2b"
ORANGE = "#d2691e"
BLUE   = "#2f4f6f"
CREAM  = "#f3e3ce"
RED    = "#b03a2e"
GREEN  = "#4a7c59"
GREY   = "#8a8a8a"

BASE = "/Users/fred/Documents/GitHub/cycleuser/blog/output/img/kaoyan-math/"


def clean(ax, xlim=(-2.4, 2.4), ylim=(-1.6, 1.6)):
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)


# ============================================================
# 1 四个逻辑联结词的区域图
# ============================================================
fig, axes = plt.subplots(2, 2, figsize=(10.6, 7.6), dpi=150)
c1, c2, r = (-0.55, 0.0), (0.55, 0.0), 1.05
FILL = ORANGE


def circles(ax):
    ax.add_patch(Rectangle((-2.3, -1.5), 4.6, 3.0, facecolor="#fbf7f2",
                           edgecolor="#dddddd", lw=1.0, zorder=0))
    for c, lab, col in [(c1, "p", BLUE), (c2, "q", GREEN)]:
        ax.add_patch(Circle(c, r, facecolor="white", edgecolor=col, lw=1.8, zorder=2))
        ax.text(c[0] - 0.05, c[1] + r - 0.34, lab, fontsize=12, color=col, zorder=6)


# (1) p 且 q
ax = axes[0][0]
circles(ax)
pat = Circle(c1, r, facecolor=FILL, alpha=0.50, edgecolor="none", zorder=3)
ax.add_patch(pat)
pat.set_clip_path(Circle(c2, r, transform=ax.transData))
ax.set_title(r"$p\wedge q$：两个条件同时成立", fontsize=11.5, color=INK)
clean(ax)

# (2) p 或 q
ax = axes[0][1]
circles(ax)
for c in (c1, c2):
    ax.add_patch(Circle(c, r, facecolor=FILL, alpha=0.50, edgecolor="none", zorder=3))
ax.set_title(r"$p\vee q$：至少一个成立", fontsize=11.5, color=INK)
clean(ax)

# (3) 非 p
ax = axes[1][0]
ax.add_patch(Rectangle((-2.3, -1.5), 4.6, 3.0, facecolor="#fbf7f2",
                       edgecolor="#dddddd", lw=1.0, zorder=0))
ax.add_patch(Rectangle((-2.3, -1.5), 4.6, 3.0, facecolor=FILL, alpha=0.50,
                       edgecolor="none", zorder=1))
ax.add_patch(Circle(c1, r, facecolor="white", edgecolor=BLUE, lw=1.8, zorder=2))
ax.add_patch(Circle(c2, r, facecolor="none", edgecolor=GREEN, lw=1.8, zorder=3))
ax.text(c1[0] - 0.05, c1[1] + r - 0.34, "p", fontsize=12, color=BLUE, zorder=6)
ax.text(c2[0] - 0.05, c2[1] + r - 0.34, "q", fontsize=12, color=GREEN, zorder=6)
ax.set_title(r"$\neg p$：阴影是 $p$ 之外的部分", fontsize=11.5, color=INK)
clean(ax)

# (4) p 推出 q
ax = axes[1][1]
circles(ax)
ax.add_patch(Rectangle((-2.3, -1.5), 4.6, 3.0, facecolor=FILL, alpha=0.50,
                       edgecolor="none", zorder=1))
ax.add_patch(Circle(c1, r, facecolor="white", edgecolor="none", zorder=2))
ax.add_patch(Circle(c2, r, facecolor=FILL, alpha=0.50, edgecolor="none", zorder=3))
ax.add_patch(Circle(c1, r, facecolor="none", edgecolor=BLUE, lw=1.8, zorder=4))
ax.add_patch(Circle(c2, r, facecolor="none", edgecolor=GREEN, lw=1.8, zorder=4))
ax.text(c1[0] - 0.05, c1[1] + r - 0.34, "p", fontsize=12, color=BLUE, zorder=6)
ax.text(c2[0] - 0.05, c2[1] + r - 0.34, "q", fontsize=12, color=GREEN, zorder=6)
ax.annotate("只有这块是白的：\np 成立而 q 不成立",
            xy=(-1.05, 0.25), xytext=(-2.15, 1.15), fontsize=9.5, color=RED,
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.0))
ax.set_title(r"$p\Rightarrow q$：阴影是可以的，白块是不允许的", fontsize=11.5, color=INK)
clean(ax)

fig.suptitle("四个逻辑联结词看区域：$p$ 与 $q$ 是两个条件成立的范围", fontsize=12.5, color=INK)
fig.tight_layout()
fig.savefig(BASE + "logic-connectives.png", dpi=150)
plt.close(fig)


# ============================================================
# 2 充分、必要、充要
# ============================================================
fig, axes = plt.subplots(1, 3, figsize=(12.6, 4.4), dpi=150)
for ax, (mode, title) in zip(axes, [
        ("need", r"$p\Rightarrow q$ 且 $q\not\Rightarrow p$：$p$ 充分不必要"),
        ("suff", r"$q\Rightarrow p$ 且 $p\not\Rightarrow q$：$p$ 必要不充分"),
        ("eq", r"$p\Leftrightarrow q$：充要条件")]):
    ax.add_patch(Rectangle((-2.2, -1.55), 4.4, 3.1, facecolor="#fbf7f2",
                           edgecolor="#eeeeee", lw=1.0, zorder=0))
    if mode == "need":
        big = Circle((0, 0), 1.35, facecolor="none", edgecolor=GREEN, lw=1.8)
        small = Circle((-0.1, -0.05), 0.62, facecolor=ORANGE, alpha=0.45,
                       edgecolor=ORANGE, lw=1.6)
        ax.add_patch(big); ax.add_patch(small)
        ax.text(0.0, 1.10, "q", fontsize=12, color=GREEN)
        ax.text(-0.62, -0.12, "p", fontsize=12, color="#8a4b16")
    elif mode == "suff":
        big = Circle((0, 0), 1.35, facecolor="none", edgecolor=BLUE, lw=1.8)
        small = Circle((0.1, 0.05), 0.62, facecolor=ORANGE, alpha=0.45,
                       edgecolor=ORANGE, lw=1.6)
        ax.add_patch(big); ax.add_patch(small)
        ax.text(0.0, 1.10, "p", fontsize=12, color=BLUE)
        ax.text(-0.42, -0.12, "q", fontsize=12, color="#8a4b16")
    else:
        ax.add_patch(Circle((0, 0), 1.15, facecolor=ORANGE, alpha=0.45,
                            edgecolor=ORANGE, lw=1.8))
        ax.text(-0.35, 0.05, "p = q", fontsize=12, color="#8a4b16")
    ax.set_title(title, fontsize=10.5, color=INK)
    clean(ax, (-2.2, 2.2), (-1.6, 1.6))

fig.suptitle("充分、必要看包含：小范围推得出大范围，反过来推不出",
             fontsize=12.5, color=INK, y=0.98)
fig.tight_layout(rect=(0, 0, 1, 0.93))
fig.savefig(BASE + "logic-conditions.png", dpi=150)
plt.close(fig)


# ============================================================
# 3 四种命题的关系
# ============================================================
fig, ax = plt.subplots(figsize=(8.6, 5.4), dpi=150)
ax.set_xlim(0, 10); ax.set_ylim(0, 6)
ax.axis("off")


def box(x, y, text, col):
    ax.add_patch(Rectangle((x - 1.55, y - 0.52), 3.1, 1.04, facecolor="white",
                           edgecolor=col, lw=1.8, zorder=3))
    ax.text(x, y, text, fontsize=11.5, color=col, ha="center", va="center", zorder=4)


box(2.4, 4.9, r"原命题：$p\Rightarrow q$", BLUE)
box(7.6, 4.9, r"逆命题：$q\Rightarrow p$", GREY)
box(2.4, 1.1, r"否命题：$\neg p\Rightarrow\neg q$", GREY)
box(7.6, 1.1, r"逆否命题：$\neg q\Rightarrow\neg p$", GREEN)

arrow_kw = dict(arrowstyle="<->", color=GREY, lw=1.3, linestyle="--")
ax.annotate("", xy=(7.6 - 1.6, 4.9), xytext=(2.4 + 1.6, 4.9),
            arrowprops=dict(arrowstyle="<->", color=GREY, lw=1.2, linestyle="--"))
ax.annotate("", xy=(7.6 - 1.6, 1.1), xytext=(2.4 + 1.6, 1.1),
            arrowprops=dict(arrowstyle="<->", color=GREY, lw=1.2, linestyle="--"))
ax.annotate("", xy=(2.4, 4.9 - 0.55), xytext=(2.4, 1.1 + 0.55),
            arrowprops=dict(arrowstyle="<->", color=GREY, lw=1.2, linestyle="--"))
ax.annotate("", xy=(7.6, 4.9 - 0.55), xytext=(7.6, 1.1 + 0.55),
            arrowprops=dict(arrowstyle="<->", color=GREY, lw=1.2, linestyle="--"))

ax.annotate("", xy=(6.72, 1.66), xytext=(3.28, 4.38),
            arrowprops=dict(arrowstyle="<->", color=GREEN, lw=2.2,
                            connectionstyle="arc3,rad=-0.22"))
ax.text(4.28, 4.02, "互为逆否，同真同假", fontsize=10.5, color=GREEN, rotation=-38,
        ha="center", va="center")

ax.text(5.0, 5.72, "互逆", fontsize=10, color=GREY, ha="center")
ax.text(5.0, 0.28, "互否", fontsize=10, color=GREY, ha="center")
ax.text(1.30, 3.0, "互否", fontsize=10, color=GREY, rotation=90, va="center", ha="center")
ax.text(8.70, 3.0, "互逆", fontsize=10, color=GREY, rotation=90, va="center", ha="center")

fig.suptitle("四种命题：只有原命题与逆否命题一定同真同假", fontsize=12.5, color=INK)
fig.tight_layout()
fig.savefig(BASE + "logic-four.png", dpi=150)
plt.close(fig)


# ============================================================
# 4 数学归纳法：多米诺骨牌
# ============================================================
fig, ax = plt.subplots(figsize=(10.4, 4.0), dpi=150)
n = 8
for i in range(n):
    x = 0.9 + i * 1.05
    lean = 0.32 if i == 0 else 0.06
    ax.add_patch(Polygon([[x, 0.0], [x + 0.30, 0.0],
                          [x + 0.30 + lean, 1.75], [x + lean, 1.75]],
                         facecolor=CREAM if i else "#e8cdb0",
                         edgecolor=ORANGE if i else BLUE, lw=1.8))
ax.annotate("", xy=(0.55, 1.35), xytext=(-0.45, 1.75),
            arrowprops=dict(arrowstyle="->", color=RED, lw=2.2))
ax.text(-0.55, 1.95, "推倒第一块", fontsize=10.5, color=RED, ha="left")
ax.annotate("", xy=(2.35, 1.05), xytext=(1.65, 1.05),
            arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.6))
ax.text(1.30, 2.45, "第一块（$n_0$）成立", fontsize=10.5, color=GREEN, ha="center")
ax.annotate("", xy=(5.6, 1.05), xytext=(4.9, 1.05),
            arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.6))
ax.text(4.55, 2.45, "前一块成立则后一块也成立（$k\\to k+1$）", fontsize=10.5,
        color=GREEN, ha="center")
ax.axhline(0, color=GREY, lw=1.2)
ax.set_xlim(-0.8, 9.4); ax.set_ylim(-0.3, 2.9)
ax.set_aspect("equal"); ax.axis("off")
ax.set_title("数学归纳法：第一步不倒，后面的每一块都会跟着倒",
             fontsize=12.5, color=INK)
fig.tight_layout()
fig.savefig(BASE + "logic-induction.png", dpi=150)
plt.close(fig)

print("logic done")


# ============================================================
# 5 乘法原理：树状图
# ============================================================
fig, ax = plt.subplots(figsize=(9.2, 5.0), dpi=150)
tops = [("甲", 1.0), ("乙", 3.5), ("丙", 6.0)]
leaf_y, top_y, root_y = 0.6, 2.4, 3.6
n = 0
for name, tx in tops:
    ax.plot([tx], [top_y], "o", color=BLUE, ms=9)
    ax.text(tx, top_y + 0.22, name, fontsize=12, color=BLUE, ha="center")
    ax.plot([-0.55, tx], [root_y, top_y], color="#c9b295", lw=1.2)
    for dx, lab in [(-0.62, "长裤"), (0.62, "短裤")]:
        n += 1
        lx = tx + dx
        ax.plot([tx, lx], [top_y, leaf_y], color=GREEN, lw=1.3)
        ax.plot([lx], [leaf_y], "o", color=GREEN, ms=8)
        ax.text(lx, leaf_y - 0.30, lab, fontsize=9.5, color=GREEN, ha="center")
        ax.text(lx, leaf_y - 0.62, str(n), fontsize=9.5, color=ORANGE, ha="center")
ax.plot([-0.55], [root_y], "o", color=INK, ms=8)
ax.text(-0.75, root_y + 0.16, "开始", fontsize=10.5, color=INK, ha="right")
ax.text(3.5, 4.05, "先选上衣 3 种，每种上衣再配裤子 2 种：$3\\times2=6$ 套",
        fontsize=11.5, color=INK, ha="center")
ax.set_xlim(-1.6, 7.6); ax.set_ylim(0.0, 4.4)
ax.axis("off")
ax.set_title("乘法原理：一步接一步地选，各步的种数相乘", fontsize=12.5, color=INK)
fig.tight_layout()
fig.savefig(BASE + "comb-tree.png", dpi=150)
plt.close(fig)


# ============================================================
# 6 杨辉三角与帕斯卡公式
# ============================================================
fig, ax = plt.subplots(figsize=(9.4, 5.6), dpi=150)
rows = 7
vals = [[1]]
for n in range(1, rows):
    prev = vals[-1]
    vals.append([1] + [prev[i] + prev[i + 1] for i in range(len(prev) - 1)] + [1])
for n, row in enumerate(vals):
    for k, v in enumerate(row):
        x = k - n / 2.0
        y = rows - n
        ax.text(x, y, str(v), fontsize=11, color=INK, ha="center", va="center")
# 高亮 C(4,2)=C(3,1)+C(3,2)
hl = [(3, 1, BLUE), (3, 2, BLUE), (4, 2, RED)]
for n, k, col in hl:
    x = k - n / 2.0
    ax.add_patch(Circle((x, rows - n), 0.28, facecolor=col, alpha=0.22, edgecolor=col, lw=1.4))
for sx, tx in [(-0.5, -0.14), (0.5, 0.14)]:
    ax.annotate("", xy=(tx, rows - 4 + 0.22), xytext=(sx, rows - 3 - 0.22),
                arrowprops=dict(arrowstyle="->", color=RED, lw=1.2))
ax.text(1.05, rows - 4.15, r"$C_4^2=C_3^1+C_3^2$", fontsize=12, color=RED, ha="left")
ax.text(-4.1, rows - 0 - 0.55, "第 0 行", fontsize=9.5, color=GREY)
ax.text(-4.1, rows - 6 - 0.55, "第 6 行", fontsize=9.5, color=GREY)
ax.set_xlim(-4.4, 4.4); ax.set_ylim(0.2, rows + 1.0)
ax.axis("off")
ax.set_title("杨辉三角：每个数是上方两数之和", fontsize=12.5, color=INK)
fig.tight_layout()
fig.savefig(BASE + "comb-pascal.png", dpi=150)
plt.close(fig)


# ============================================================
# 7 二项式定理的系数来源
# ============================================================
fig, ax = plt.subplots(figsize=(10.0, 4.8), dpi=150)
labels = ["(a+b)", "(a+b)", "(a+b)"]
xs = [1.0, 3.2, 5.4]
for x, lab in zip(xs, labels):
    ax.add_patch(Rectangle((x - 0.75, 1.4), 1.5, 1.1, facecolor=CREAM,
                           edgecolor=ORANGE, lw=1.6))
    ax.text(x, 1.95, lab, fontsize=12, color=INK, ha="center", va="center")
ax.text(-1.55, 1.95, "三个因式", fontsize=11, color=GREY, ha="left", va="center")
# 一种取法：第1、3 个取 b，第2 个取 a
picks = [(1.0, "b"), (3.2, "a"), (5.4, "b")]
for x, ch in picks:
    ax.text(x, 2.75, ch, fontsize=13, color=RED if ch == "b" else BLUE, ha="center")
    ax.annotate("", xy=(x, 2.55), xytext=(x, 2.20),
                arrowprops=dict(arrowstyle="->", color=RED if ch == "b" else BLUE, lw=1.3))
ax.text(3.2, 3.15, "每次从每个因式里取一个字母", fontsize=10.5, color=INK, ha="center")
ax.text(3.2, 0.75, r"这一种取法给出 $a^{1}b^{2}$；$b$ 取在哪两个因式里有 $C_3^2$ 种，"
                   r"所以 $a b^{2}$ 的系数是 $C_3^2=3$", fontsize=11, color=INK, ha="center")
ax.text(3.2, 0.25, r"$(a+b)^{3}=a^{3}+3a^{2}b+3ab^{2}+b^{3}$", fontsize=12.5, color=BLUE,
        ha="center")
ax.set_xlim(-1.7, 6.8); ax.set_ylim(0.0, 3.5)
ax.axis("off")
ax.set_title("二项式系数从哪来：选哪几个因式出 $b$", fontsize=12.5, color=INK)
fig.tight_layout()
fig.savefig(BASE + "comb-binomial.png", dpi=150)
plt.close(fig)


# ============================================================
# 8 平均分组为什么要除以 k!
# ============================================================
fig, ax = plt.subplots(figsize=(11.0, 4.4), dpi=150)
groups = [("AB", "CD", "EF"), ("AB", "EF", "CD"), ("CD", "AB", "EF"),
          ("CD", "EF", "AB"), ("EF", "AB", "CD"), ("EF", "CD", "AB")]
for i, g in enumerate(groups):
    y = 3.0 - i * 0.52
    ax.text(0.15, y, f"{i + 1}", fontsize=10, color=GREY, ha="center", va="center")
    for j, blk in enumerate(g):
        ax.add_patch(Rectangle((0.7 + j * 1.5, y - 0.20), 1.25, 0.4,
                               facecolor=CREAM, edgecolor=ORANGE, lw=1.2))
        ax.text(0.7 + j * 1.5 + 0.62, y, blk, fontsize=10.5, color=INK,
                ha="center", va="center")
ax.text(5.9, 3.0, "这 6 行是同一分组，只是三块的顺序不同", fontsize=11, color=RED,
        ha="left", va="center")
ax.text(5.9, 2.45, r"所以 $\dfrac{C_6^2C_4^2C_2^2}{3!}$ 才是分法数", fontsize=11.5,
        color=BLUE, ha="left", va="center")
ax.set_xlim(0.0, 12.2); ax.set_ylim(-0.15, 3.4)
ax.axis("off")
ax.set_title("平均分组：同一结果被数了 $3!$ 次，要除回去", fontsize=12.5, color=INK)
fig.tight_layout()
fig.savefig(BASE + "comb-grouping.png", dpi=150)
plt.close(fig)


# ============================================================
# 9 隔板法
# ============================================================
fig, ax = plt.subplots(figsize=(9.6, 3.4), dpi=150)
n_star, k_bar = 7, 2
pos = 0.6
for i in range(n_star):
    ax.text(pos, 1.0, "★", fontsize=17, color=ORANGE, ha="center", va="center")
    pos += 0.75
    if i in (1, 4):
        ax.text(pos - 0.05, 1.0, "|", fontsize=20, color=BLUE, ha="center", va="center")
        pos += 0.45
ax.text(0.6, 1.75, r"7 个相同球放进 3 个不同的盒子 $\Leftrightarrow$ 插 2 块板", fontsize=11,
        color=INK, ha="left")
ax.text(0.6, 0.30, r"允许空盒：$C_{7+3-1}^{3-1}=C_9^2=36$；每盒至少一个：$C_{7-1}^{3-1}=C_6^2=15$",
        fontsize=11.5, color=BLUE, ha="left")
ax.set_xlim(0.3, 8.6); ax.set_ylim(0.05, 2.1)
ax.axis("off")
ax.set_title("隔板法：球相同、盒不同，只看两块板插在哪", fontsize=12.5, color=INK)
fig.tight_layout()
fig.savefig(BASE + "comb-stars.png", dpi=150)
plt.close(fig)


# ============================================================
# 10 容斥原理
# ============================================================
fig, ax = plt.subplots(figsize=(6.4, 5.0), dpi=150)
A = Circle((-0.75, 0.35), 1.15, facecolor=BLUE, alpha=0.30, edgecolor=BLUE, lw=1.8)
B = Circle((0.75, 0.35), 1.15, facecolor=GREEN, alpha=0.30, edgecolor=GREEN, lw=1.8)
C = Circle((0.0, -0.75), 1.15, facecolor=ORANGE, alpha=0.28, edgecolor=ORANGE, lw=1.8)
for p in (A, B, C):
    ax.add_patch(p)
ax.text(-1.55, 1.15, "$A$", fontsize=13, color=BLUE)
ax.text(1.45, 1.15, "$B$", fontsize=13, color=GREEN)
ax.text(0.0, -1.75, "$C$", fontsize=13, color=ORANGE)
ax.text(D if False else 0, 0, "", fontsize=1)
ax.text(-1.35, 0.35, "只 A", fontsize=9.5, color=INK)
ax.text(1.05, 0.35, "只 B", fontsize=9.5, color=INK)
ax.text(-0.55, -1.15, "只 C", fontsize=9.5, color=INK)
ax.text(0.0, 0.55, "$AB$", fontsize=9, color=INK)
ax.text(-0.62, -0.42, "$AC$", fontsize=9, color=INK)
ax.text(0.62, -0.42, "$BC$", fontsize=9, color=INK)
ax.text(0.0, -0.18, "$ABC$", fontsize=8.5, color=RED)
ax.text(0.0, 2.35, "$|A\\cup B\\cup C|=|A|+|B|+|C|-|AB|-|AC|-|BC|+|ABC|$",
        fontsize=10.5, color=INK, ha="center")
ax.set_xlim(-2.2, 2.2); ax.set_ylim(-2.1, 2.6)
ax.set_aspect("equal"); ax.axis("off")
ax.set_title("容斥原理：加回来、再减回去", fontsize=12, color=INK)
fig.tight_layout()
fig.savefig(BASE + "comb-inclusion.png", dpi=150)
plt.close(fig)

print("comb done")
