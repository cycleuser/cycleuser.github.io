"""四位加法器逐位进位动画"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import FancyBboxPatch, Circle, Rectangle
from PIL import Image
import os

plt.rcParams["font.family"] = ["PingFang SC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
INK, BLUE, RED, GREEN, GREY, ORANGE = "#2b2b2b", "#2f4f6f", "#b03a2e", "#4a7c59", "#8a8a8a", "#d2691e"
BASE = "/Users/fred/Documents/GitHub/cycleuser/blog/output/img/kaoyan-math/"
F = 13.0
SCRATCH = os.path.dirname(os.path.abspath(__file__))

A = [1, 0, 1, 0]   # 0101 = 5  (LSD 先)
B = [1, 1, 0, 0]   # 0011 = 3
Cin0 = 0

# 逐位计算
S = []
C = []
cin = Cin0
for i in range(4):
    t = A[i] + B[i] + cin
    S.append(t % 2); C.append(t // 2)
    cin = t // 2
Cout = cin

def frame(step):
    fig, ax = plt.subplots(figsize=(11.4, 4.9), dpi=120)
    ax.set_xlim(-1.7, 13.4); ax.set_ylim(-0.45, 5.55)
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values(): sp.set_color("none")

    def bitbox(x, y, v, active, w=1.05, h=0.85):
        fc = "#f6e2cf" if active else "#f4f6f8"
        ec = ORANGE if active else "#b9c2cc"
        ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.05",
                                    facecolor=fc, edgecolor=ec, lw=2.0, zorder=4))
        ax.text(x + w/2, y + h/2, str(v), fontsize=F+4, color=INK,
                ha="center", va="center", zorder=5)

    x0 = 2.6; dx = 2.55
    xpos = lambda i: x0 + (3 - i)*dx      # i=0 在右（最低位）

    ax.text(0.55, 4.42, "$A$", fontsize=F+2, color=INK, va="center")
    ax.text(0.55, 3.32, "$B$", fontsize=F+2, color=INK, va="center")
    for i in range(4):
        x = xpos(i)
        act = (i < step)
        bitbox(x, 4.0, A[i], act)
        bitbox(x, 2.9, B[i], act)
        if act:
            ax.text(x + 0.52, 3.56, "+", fontsize=F+2, color=GREY, ha="center", va="center")

    # 全加器
    for i in range(4):
        x = xpos(i) - 0.35
        act = (i < step)
        ax.add_patch(FancyBboxPatch((x, 1.05), 1.75, 1.05, boxstyle="round,pad=0.06",
                                    facecolor="#e6eef7" if act else "#eef1f5",
                                    edgecolor=BLUE, lw=2.0, zorder=3))
        ax.text(x + 0.875, 1.575, "FA", fontsize=F-2, color=BLUE, ha="center", va="center", zorder=4)

    # 和位
    ax.text(0.55, 0.58, "$S$", fontsize=F+2, color=INK, va="center")
    for i in range(4):
        if i < step:
            bitbox(xpos(i), 0.15, S[i], True)

    # 进位链：位 i 的进位 → 位 i+1（向左）
    for i in range(3):
        x_from = xpos(i) - 0.35           # 本位左边缘（进位输出）
        x_to = xpos(i+1) + 1.40           # 高位右边缘（进位输入）
        act = (i < step - 1)
        ax.annotate("", xy=(x_to, 1.575), xytext=(x_from, 1.575),
                    arrowprops=dict(arrowstyle="-|>", color=ORANGE if act else "#d3d9df",
                                    lw=2.6 if act else 1.6, shrinkA=1, shrinkB=1))
        if act:
            ax.text((x_from + x_to)/2, 1.86, str(C[i]), fontsize=F, color=ORANGE,
                    ha="center", va="center")

    # C_in 进最低位（右侧）
    ax.annotate("", xy=(xpos(0) + 0.52, 1.575), xytext=(xpos(0) + 1.55, 1.575),
                arrowprops=dict(arrowstyle="-|>", color="#d3d9df", lw=1.6,
                                shrinkA=0, shrinkB=0))
    ax.text(xpos(0) + 1.62, 1.575, "$C_{in}=0$", fontsize=F-3, color=GREY,
            ha="left", va="center")

    # Cout（最高位左侧）
    if step >= 4:
        bx = xpos(3) - 1.55
        bitbox(bx, 0.15, Cout, True)
        ax.annotate("", xy=(bx + 1.05, 1.575), xytext=(xpos(3) - 0.35, 1.575),
                    arrowprops=dict(arrowstyle="-|>", color=ORANGE, lw=2.6,
                                    shrinkA=0, shrinkB=0))
        ax.text(bx + 0.52, 1.86, str(C[3]), fontsize=F, color=ORANGE,
                ha="center", va="center")
        ax.text(bx + 0.52, -0.12, "$C_{out}$", fontsize=F-3, color=RED,
                ha="center", va="top")

    # 进度文字
    if step == 0:
        msg = "起点：两个四位二进制数 $0101$ 与 $0011$，最低位的进位输入为 $0$"
    else:
        parts = []
        for i in range(step):
            cin_i = Cin0 if i == 0 else C[i-1]
            parts.append("%d+%d+%d → 进位 %d、和 %d" % (A[i], B[i], cin_i, C[i], S[i]))
        msg = "算第 %d 位（从最右往左）：%s" % (step, "；".join(parts))
    ax.set_title("四位加法器算 $0101+0011$（即 $5+3=8$）", fontsize=F+3, color=INK, pad=30)
    ax.text((xpos(0)+x0)/2 - 0.5, 5.35, msg, fontsize=F-3, color=GREY, ha="center", va="center")
    fig.subplots_adjust(0.01, 0.03, 0.99, 0.99)
    return fig

frames = []
for step in range(5):
    fig = frame(step)
    fp = os.path.join(SCRATCH, "_ad_%d.png" % step)
    fig.savefig(fp, dpi=120); plt.close(fig)
    frames.append(Image.open(fp).convert("RGB"))

# 每步停留更久：重复帧
seq = []
for i, fr in enumerate(frames):
    rep = 6 if i < 4 else 10
    seq.extend([fr]*rep)
pal = [f.convert("P", palette=Image.ADAPTIVE) for f in seq]
pal[0].save(BASE + "logic-4bit-adder.gif", save_all=True, append_images=pal[1:],
            duration=260, loop=0, optimize=True)
for step in range(5):
    os.remove(os.path.join(SCRATCH, "_ad_%d.png" % step))
print("ok 4bit adder gif")
