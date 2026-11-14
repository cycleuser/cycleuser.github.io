"""附录7 门电路与加法器动画：信号通断用亮红/浅灰表示"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Circle, Polygon, FancyBboxPatch, PathPatch
from matplotlib.path import Path
from PIL import Image
import os

plt.rcParams["font.family"] = ["PingFang SC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False
INK = "#2b2b2b"
BLUE, GREY = "#4a5a6a", "#9aa4ae"
HOT, COLD = "#c0392b", "#c9ced4"
BASE = "/Users/fred/Documents/GitHub/cycleuser/blog/output/img/kaoyan-math/"
F = 15.0
SCRATCH = os.path.dirname(os.path.abspath(__file__))

def gate_and(ax, x, y, w, h, col, lw=3.2):
    """D 形与门：左边竖线、上下平边、右侧半圆"""
    t = np.linspace(-np.pi/2, np.pi/2, 240)
    xs = [x, x + w*0.55] + list(x + w*0.55 + (w*0.45)*np.cos(t)) + [x + w*0.55, x]
    ys = [y, y] + list(y + h/2 + (h/2)*np.sin(t)) + [y + h, y + h]
    pts = []
    for a, b in zip(xs, ys):
        if not pts or abs(a - pts[-1][0]) > 1e-9 or abs(b - pts[-1][1]) > 1e-9:
            pts.append((a, b))
    ax.add_patch(Polygon(pts, closed=True, fill=True, facecolor="white",
                         edgecolor=col, lw=lw, joinstyle="round", zorder=6))
    return x + w, y + h/2

def gate_or(ax, x, y, w, h, col, lw=3.2, xor=False):
    """或门：输入侧内凹弧 + 上下弧收尖；返回 (尖端x, 中线y, 输入侧x函数)"""
    t = np.linspace(-1, 1, 240)
    back_x = x + 0.45*(t**2)                 # 中间内凹到 x，两端到 x+0.45
    back_y = y + h/2 + (h/2)*t
    ax.plot(back_x, back_y, color=col, lw=lw, zorder=7, solid_capstyle="round")
    if xor:
        ax.plot(back_x - 0.30, back_y, color=col, lw=lw, zorder=7, solid_capstyle="round")
    s_ = np.linspace(0, 1, 240)
    xt = x + 0.45 + (w - 0.45)*s_
    ax.plot(xt, y + h - (h/2)*(s_**1.8), color=col, lw=lw, zorder=5, solid_capstyle="round")
    ax.plot(xt, y + (h/2)*(s_**1.8), color=col, lw=lw, zorder=5, solid_capstyle="round")
    def inx(yin):
        t = (yin - (y + h/2))/(h/2)
        return x + 0.45*(t**2) - (0.30 if xor else 0.0)
    return x + w, y + h/2, inx

def gate_not(ax, x, y, w, h, col, lw=3.2):
    ax.add_patch(Polygon([(x, y+h/2+h/2*0.55), (x, y+h/2-h/2*0.55), (x+w, y+h/2)],
                         closed=True, fill=True, facecolor="white", edgecolor=col,
                         lw=lw, joinstyle="miter", zorder=6))
    ax.add_patch(Circle((x+w+0.15, y+h/2), 0.15, facecolor="white",
                        edgecolor=col, lw=lw-0.4, zorder=7))
    return x + w + 0.30, y + h/2

def wire(ax, pts, on, lw=3.0):
    col = HOT if on else COLD
    xs = [p[0] for p in pts]; ys = [p[1] for p in pts]
    ax.plot(xs, ys, color=col, lw=lw + (1.0 if on else 0), solid_capstyle="round",
            solid_joinstyle="round", zorder=4)

def dot(ax, x, y, on):
    ax.add_patch(Circle((x, y), 0.11, facecolor=HOT if on else COLD,
                        edgecolor="white", lw=1.2, zorder=8))

def T(ax, x, y, s, size=F, color=INK, ha="center", va="center"):
    ax.text(x, y, s, fontsize=size, color=color, ha=ha, va=va, zorder=9)

def axes_(w, h, xlim, ylim):
    fig, ax = plt.subplots(figsize=(w, h), dpi=120)
    ax.set_xlim(*xlim); ax.set_ylim(*ylim); ax.set_aspect("equal")
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values(): sp.set_color("none")
    return fig, ax

def grab(fig, tag):
    fp = os.path.join(SCRATCH, "_%s.png" % tag)
    fig.savefig(fp, dpi=120); plt.close(fig)
    im = Image.open(fp).convert("RGB"); os.remove(fp)
    return im

def save_gif(frames, name, dur=650):
    pal = [f.convert("P", palette=Image.ADAPTIVE) for f in frames]
    pal[0].save(BASE + name, save_all=True, append_images=pal[1:], duration=dur, loop=0, optimize=True)
    print("ok", name, len(frames))

# =====================================================================
# 1) 四种门：各自动画（真值表逐行，导线亮/暗）
# =====================================================================
def gate_anim(kind, fname):
    rows = [(0, 0), (0, 1), (1, 0), (1, 1)]
    frames = []
    for a, b in rows:
        if kind == "AND": out = a & b
        elif kind == "OR": out = a | b
        elif kind == "NOT": out = 1 - a
        else: out = a ^ b
        fig, ax = axes_(6.2, 4.9, (0, 10.2), (0, 8.0))
        yA, yB = 5.85, 3.35
        T(ax, 0.30, yA, "$A=%d$" % a, size=F, color=HOT if a else GREY, ha="left")
        T(ax, 0.30, yB, "$B=%d$" % b, size=F, color=HOT if b else GREY, ha="left")
        if kind == "NOT":
            wire(ax, [(1.85, yA), (4.3, yA)], on=bool(a))
            xo, yo = gate_not(ax, 4.3, yA-1.1, 1.9, 2.2, HOT if out else BLUE)
            # B 不参与
            T(ax, 1.85, yB, "（非门只有一个输入）", size=F-4, color=GREY, ha="left")
        elif kind == "AND":
            wire(ax, [(1.85, yA), (4.3, yA)], on=bool(a))
            wire(ax, [(1.85, yB), (4.3, yB)], on=bool(b))
            xo, yo = gate_and(ax, 4.3, 2.6, 3.0, 4.0, HOT if out else BLUE)
            T(ax, 5.6, 4.6, "&", size=F+8, color=HOT if out else BLUE)
        else:
            xo, yo, inx = gate_or(ax, 4.3, 2.6, 3.2, 4.0, HOT if out else BLUE, xor=(kind == "XOR"))
            wire(ax, [(1.85, yA), (inx(yA), yA)], on=bool(a))
            wire(ax, [(1.85, yB), (inx(yB), yB)], on=bool(b))
            T(ax, 6.05, 4.6, "$\\geq$1", size=F+1, color=HOT if out else BLUE)
        wire(ax, [(xo, yo), (8.7, yo)], on=bool(out))
        T(ax, 8.85, yo, "$%d$" % out, size=F+3, color=HOT if out else GREY, ha="left")
        name = {"AND": "与门 $A\\cdot B$：两个都 1 才出 1",
                "OR": "或门 $A+B$：有一个 1 就出 1",
                "NOT": "非门 $\\overline{A}$：输入取反",
                "XOR": "异或门 $A\\oplus B$：不同才出 1"}[kind]
        T(ax, 5.1, 7.55, name, size=F+1)
        T(ax, 5.1, 1.35, "$%d,%d\\ \\to\\ %d$" % (a, b, out), size=F+3, color=INK)
        T(ax, 5.1, 0.55, "红色＝高电平 1（通），灰色＝低电平 0（断）", size=F-3, color=GREY)
        fig.subplots_adjust(0.01, 0.01, 0.99, 0.99)
        frames.append(grab(fig, "g"))
    save_gif(frames, fname, dur=800)

gate_anim("AND", "logic-gate-and.gif")
gate_anim("OR", "logic-gate-or.gif")
gate_anim("NOT", "logic-gate-not.gif")
gate_anim("XOR", "logic-gate-xor.gif")

# =====================================================================
# 2) 半加器动画
# =====================================================================
frames = []
for a, b in [(0,0),(0,1),(1,0),(1,1)]:
    S = a ^ b; C = a & b
    fig, ax = axes_(7.0, 5.8, (0, 14.4), (0.6, 11.4))
    yA, yB = 8.70, 4.60
    T(ax, 0.30, yA, "$A=%d$" % a, size=F, color=HOT if a else GREY, ha="left")
    T(ax, 0.30, yB, "$B=%d$" % b, size=F, color=HOT if b else GREY, ha="left")

    # 异或门：A 直入上输入，B 抬升入下输入
    xo, yo, inx = gate_or(ax, 5.4, 6.60, 3.4, 2.40, HOT if S else BLUE, xor=True)
    wire(ax, [(1.90, yA), (inx(8.70), 8.70)], on=bool(a))
    wire(ax, [(3.40, yB), (3.40, 7.00), (inx(7.00), 7.00)], on=bool(b))
    dot(ax, 3.40, yB, bool(b))
    wire(ax, [(xo, yo), (12.4, yo)], on=bool(S))
    T(ax, 12.55, yo, "$S=%d$" % S, size=F+2, color=HOT if S else GREY, ha="left")
    T(ax, 7.05, 9.55, "异或门（给和）", size=F-3, color=GREY)

    # 与门：A 下拉入下输入，B 下拉入上输入
    xa, ya = gate_and(ax, 5.4, 1.60, 3.0, 2.60, HOT if C else BLUE)
    wire(ax, [(1.60, yA), (1.60, 2.25), (5.4, 2.25)], on=bool(a))
    dot(ax, 1.60, yA, bool(a))
    wire(ax, [(1.90, yB), (4.80, yB)], on=bool(b))
    wire(ax, [(4.80, yB), (4.80, 3.65), (5.4, 3.65)], on=bool(b))
    dot(ax, 4.80, yB, bool(b))
    T(ax, 6.30, 3.10, "&", size=F+5, color=HOT if C else BLUE)
    wire(ax, [(xa, ya), (12.4, ya)], on=bool(C))
    T(ax, 12.55, ya, "$C=%d$" % C, size=F+2, color=HOT if C else GREY, ha="left")
    T(ax, 7.05, 0.95, "与门（给进位）", size=F-3, color=GREY)

    T(ax, 7.2, 10.95, "半加器：$%d+%d$ → 和 $%d$、进位 $%d$" % (a, b, S, C), size=F+1)
    T(ax, 7.2, 0.28, "红＝高电平 1（通），灰＝低电平 0（断）" if False else
          "红＝高电平 1（通），灰＝低电平 0（断）", size=F-4, color=GREY)
    fig.subplots_adjust(0.01, 0.01, 0.99, 0.99)
    frames.append(grab(fig, "ha"))
save_gif(frames, "logic-halfadder.gif", dur=800)

# =====================================================================
# 3) 全加器动画（框图 + 标注式连线）
# =====================================================================
frames = []
for a in (0,1):
    for b in (0,1):
        for cin in (0,1):
            s1 = a ^ b; c1 = a & b
            S = s1 ^ cin; c2 = s1 & cin
            Cout = c1 | c2
            fig, ax = axes_(8.2, 4.4, (0, 23.4), (0, 12.0))

            def box(x, y, w, h, tag, hot):
                ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=0.12",
                                            facecolor="#fdeee8" if hot else "#f4f6f9",
                                            edgecolor=HOT if hot else BLUE, lw=2.8, zorder=5))
                T(ax, x+w/2, y+h/2, tag, size=F-2, color=HOT if hot else BLUE)

            box(2.2, 7.8, 5.0, 2.8, "半加器 1", bool(a or b))
            box(13.6, 7.8, 5.0, 2.8, "半加器 2", bool(s1 or cin))

            def stub(x, y, label, val, side="right", ln=1.0):
                on = bool(val)
                dx = ln if side == "right" else -ln
                wire(ax, [(x, y), (x+dx, y)], on=on)
                T(ax, x+dx + (0.14 if side == "right" else -0.14), y, label,
                  size=F-3, color=HOT if on else GREY,
                  ha="left" if side == "right" else "right")

            stub(2.2, 9.95, "$A=%d$" % a, a, side="left")
            stub(2.2, 8.75, "$B=%d$" % b, b, side="left")
            stub(7.2, 9.95, "$S_1=%d$" % s1, s1)
            stub(7.2, 8.75, "$C_1=%d$" % c1, c1)
            stub(13.6, 9.95, "$S_1$", s1, side="left")
            stub(13.6, 8.75, "$C_{in}=%d$" % cin, cin, side="left")
            stub(18.6, 9.95, "$S=%d$" % S, S)
            stub(18.6, 8.75, "$C_2=%d$" % c2, c2)

            xo, yo, inx = gate_or(ax, 16.6, 3.1, 2.4, 2.1, HOT if Cout else BLUE)
            stub(16.6, 4.75, "$C_1$", c1, side="left", ln=1.1)
            stub(16.6, 3.55, "$C_2$", c2, side="left", ln=1.1)
            wire(ax, [(xo, yo), (20.6, yo)], on=bool(Cout))
            T(ax, 20.75, yo, "$C_{out}=%d$" % Cout, size=F-2,
              color=HOT if Cout else GREY, ha="left")
            T(ax, 17.7, 2.35, "或门", size=F-4, color=GREY)

            T(ax, 11.7, 11.55, "全加器：$%d+%d+%d$ → 和 $%d$、进位 $%d$" % (a, b, cin, S, Cout), size=F+1)
            fig.subplots_adjust(0.01, 0.01, 0.99, 0.99)
            frames.append(grab(fig, "fa"))
save_gif(frames, "logic-fulladder.gif", dur=900)
