import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches

plt.rcParams["font.family"] = ["PingFang SC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False


BASE = "/Users/fred/Documents/GitHub/cycleuser/blog/output/img/kaoyan-math/"
F = 11.5
T = 12.0
PI = np.pi
INK, ORANGE, BLUE, RED, GREEN, GREY = ("#2b2b2b", "#d2691e", "#2f4f6f", "#b03a2e", "#4a7c59", "#8a8a8a")


def frame(ax, xlim, ylim, title):
    ax.axhline(0, color="#dcdcdc", lw=0.9)
    ax.axvline(0, color="#dcdcdc", lw=0.9)
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_color("#cccccc")
    ax.set_title(title, fontsize=12, color=INK, pad=7)


# ============ 1 过极点的圆与直线 ============
BOX = dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#dddddd")
F2, T2 = 11.0, 12.0
a = 1.6
tt = np.linspace(-np.pi / 2, np.pi / 2, 400)
tt2 = np.linspace(-1.2, 1.2, 300)


def one_polar_panel(fname, lim, title, plot, note=""):
    fig, ax = plt.subplots(figsize=(6.4, 5.8), dpi=150)
    th0 = np.linspace(0, 2 * np.pi, 400)
    for rr in np.arange(0.5, lim + 0.01, 0.5):
        ax.plot(rr * np.cos(th0), rr * np.sin(th0), color="#ececec", lw=0.8, zorder=0)
    for aa in np.arange(0, np.pi, np.pi / 6):
        for sg in (1, -1):
            ax.plot([0, lim * np.cos(aa) * sg], [0, lim * np.sin(aa) * sg],
                    color="#ececec", lw=0.8, zorder=0)
    ax.axhline(0, color="#c8c8c8", lw=1.0, zorder=1)
    ax.axvline(0, color="#c8c8c8", lw=1.0, zorder=1)
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_color("#cccccc")
    ax.set_title(title + "\n极坐标平面", fontsize=T2, color=INK, pad=6)
    plot(ax)
    if note:
        ax.text(0.02, 0.96, note, transform=ax.transAxes, fontsize=F2 - 2.5,
            color=INK, va="top")
    fig.tight_layout(); fig.savefig(BASE + fname, dpi=150); plt.close(fig)


def one_cart_panel(fname, lim, title, plot, eq=None, eqfont=None):
    fig, ax = plt.subplots(figsize=(6.2, 5.8), dpi=150)
    ax.set_xlim(*lim); ax.set_ylim(*lim)
    ax.set_aspect("equal")
    ax.grid(True, color="#ececec", lw=0.8)
    ax.axhline(0, color="#c8c8c8", lw=1.1, zorder=1)
    ax.axvline(0, color="#c8c8c8", lw=1.1, zorder=1)
    tk = [t for t in (-2, -1, 0, 1, 2, 3) if lim[0] < t < lim[1]]
    if len(tk) > 6:
        tk = [t for t in (-4, -2, 0, 2, 4) if lim[0] < t < lim[1]]
    ax.set_xticks(tk); ax.set_yticks(tk)
    ax.set_xticklabels([str(t) for t in tk], fontsize=F2 - 3.5, color="#999999")
    ax.set_yticklabels([str(t) for t in tk], fontsize=F2 - 3.5, color="#999999")
    ax.tick_params(length=2, colors="#cccccc")
    for sp in ax.spines.values():
        sp.set_color("#cccccc")
    ax.set_xlabel("$x$", fontsize=F2 - 1, color=INK, labelpad=0)
    ax.set_ylabel("$y$", fontsize=F2 - 1, color=INK, labelpad=0)
    ax.set_title(title + "\n直角坐标：代入后的方程单独画", fontsize=T2, color=INK, pad=6)
    plot(ax)
    if eq:
        ax.text(0.5, 0.03, eq, transform=ax.transAxes, fontsize=(eqfont or F2 - 2),
                color=INK, ha="center", va="bottom", bbox=BOX)
    fig.tight_layout(); fig.savefig(BASE + fname, dpi=150); plt.close(fig)


def circle_p(ax):
    th0 = np.linspace(0, 2 * np.pi, 400)
    ax.plot(2 * a * np.cos(tt) ** 2, 2 * a * np.cos(tt) * np.sin(tt), color=BLUE, lw=2.6, zorder=3)
    ax.plot([0], [0], "o", color=INK, ms=7, zorder=6)
    ax.plot([2 * a], [0], "o", color=RED, ms=7, zorder=6)
    ax.text(-0.16, -0.30, "$O$", fontsize=F2, color=INK, ha="right")
    ax.text(1.50, 0.30, "$\\theta=0$：$r=2a$", fontsize=F2 - 2, color=RED)


def circle_c(ax):
    ax.plot(2 * a * np.cos(tt) ** 2, 2 * a * np.cos(tt) * np.sin(tt), color=BLUE, lw=2.6, zorder=3)
    ax.plot([0], [0], "o", color=INK, ms=7, zorder=6)
    ax.plot([2 * a], [0], "o", color=RED, ms=7, zorder=6)
    ax.text(a - 0.02, -0.48, "圆心 $(a,0)$", fontsize=F2 - 2.5, color=GREY, ha="center")


one_polar_panel("pc-circle-step1.png", 2.5, "过极点的圆 $r=2a\\cos\\theta$", circle_p,
                note="$\\theta\\in\\left[-\\frac{\\pi}{2},\\frac{\\pi}{2}\\right]$")
one_cart_panel("pc-circle-step2.png", (-2.5, 2.5), "过极点的圆", circle_c,
               eq="$y=\\pm\\sqrt{a^{2}-\\left(x-a\\right)^{2}}$", eqfont=F2 - 2)


def line_p(ax):
    ax.plot(np.ones_like(tt2), np.tan(tt2), color=ORANGE, lw=2.6, zorder=3)
    ax.plot([0], [0], "o", color=INK, ms=7, zorder=6)
    ax.text(-0.16, -0.30, "$O$", fontsize=F2, color=INK, ha="right")
    ax.text(1.08, 1.85, "$x=1$", fontsize=F2 - 1, color=ORANGE)


def line_c(ax):
    ax.plot([1, 1], [-2.2, 2.2], color=ORANGE, lw=2.6, zorder=3)
    ax.plot([0], [0], "o", color=INK, ms=7, zorder=6)
    ax.text(1.15, 1.90, "$x=1$", fontsize=F2 - 1, color=ORANGE)


one_polar_panel("pc-line-step1.png", 2.5, "不过极点的直线 $r=\\sec\\theta$", line_p,
                note="直线不过极点，$r$ 随 $\\theta$ 变化")
one_cart_panel("pc-line-step2.png", (-2.5, 2.5), "不过极点的直线", line_c)

# ============ 2 面积微元与弧长微元 ============
BOX = dict(boxstyle="round,pad=0.3", facecolor="white", edgecolor="#dddddd")
rfun = lambda t: 1 + np.sin(t)
th_all = np.linspace(0, 2 * PI, 600)
rr_all = rfun(th_all)

RED, BROWN = "#b03a2e", "#7a5230"

# --- 子图 1：面积切分 ---
fig, axes = plt.subplots(1, 1, figsize=(7.2, 6.2), dpi=170)
ORANGE_L = "#e8a15c"

# 左：面积——切分+扇形
ax = axes
ax.set_xlim(-1.8, 1.8); ax.set_ylim(-1.3, 2.1)
ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
for sp_ in ax.spines.values():
    sp_.set_color("#cccccc")
ax.plot(rr_all * np.cos(th_all), rr_all * np.sin(th_all), color=BLUE, lw=1.4, alpha=0.5, zorder=3)
ax.plot([0], [0], "o", color=INK, ms=5, zorder=6)
# 一条射线方向，切若干射线把区域分块
for ang in np.linspace(-0.3, 2.2, 9):
    rr = rfun(ang)
    ax.plot([0, rr * np.cos(ang)], [0, rr * np.sin(ang)], color="#c9a887", lw=0.9, zorder=2)
# 一份扇形染色
t1, t2 = 0.6, 0.94
tt = np.linspace(t1, t2, 40)
rr = rfun(tt)
ax.fill(np.concatenate([[0], rr * np.cos(tt), [0]]),
        np.concatenate([[0], rr * np.sin(tt), [0]]),
        color=ORANGE_L, alpha=0.55, edgecolor=ORANGE, lw=1.4, zorder=4)
# θ 标记
ax.text(rfun(0.77) * np.cos(np.deg2rad(38)) * 0.42, rfun(0.77) * np.sin(np.deg2rad(38)) * 0.42,
        "$\\Delta\\theta$", fontsize=F - 1, color=ORANGE, ha="center", va="center")
ax.annotate("$r(\\theta)$", xy=(rfun(1.0) * np.cos(1.0), rfun(1.0) * np.sin(1.0)),
            xytext=(-1.7, 1.75), fontsize=F - 1, color=BLUE,
            arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.0))
ax.text(0.03, 0.03, "$\\Delta S\\approx\\frac{1}{2}r^{2}\\,\\Delta\\theta$（扇形）",
        transform=ax.transAxes, fontsize=F - 1.5, color=INK, va="bottom")
ax.set_title("面积：把角度切成小份，\n每一份近似成扇形", fontsize=T - 0.5, color=INK, pad=8)

fig.subplots_adjust(left=0.02, right=0.98, top=0.87, bottom=0.03)
fig.savefig(BASE + "pc-area-slicing.png", dpi=170)
plt.close(fig)

# --- 子图 2：弧长三角形 ---
fig, ax = plt.subplots(1, 1, figsize=(7.2, 5.6), dpi=170)
ax.set_xlim(-0.55, 1.45); ax.set_ylim(-0.50, 1.15)
ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
for sp_ in ax.spines.values():
    sp_.set_color("#cccccc")
th_p = 0.0            # 放大点放在 θ=0 处
u = np.array([1.0, 0.0])          # θ=0 径向
drr = 0.36                        # 径向长度（放大了的 dr）
dth = 0.42                        # 角宽度（放大了的 dθ）
rf0 = 0.62                        # 基准半径
def pt(t, rr):
    return rr * np.array([np.cos(t), np.sin(t)])
A = pt(0.0, rf0)                  # 起点在 θ=0 的圆上
B = pt(dth, rf0)                  # θ=dθ、r 固定的圆弧末端
C = pt(dth, rf0 + drr)            # r 也增加后的真终点
arc = np.array([pt(t, rf0) for t in np.linspace(0, dth, 40)])
# 极点与两条射线
ax.plot([0], [0], "o", color=INK, ms=5, zorder=6)
for ang, lbl in [(0.0, "$\\theta$"), (dth, "$\\theta+\\mathrm{d}\\theta$")]:
    rr_end = rf0 + drr + 0.30
    ax.plot([0, rr_end * np.cos(ang)], [0, rr_end * np.sin(ang)],
            color="#c9a887", lw=0.9, zorder=2)
    ax.text(rr_end * np.cos(ang) * np.array([1, -1])[1] * 0, rr_end * np.sin(ang) + 0.05,
            lbl, fontsize=F - 2, color=GREY,
            ha="left" if lbl.startswith("$\\theta+") else "center")
# 灰色曲线段（真实曲线穿过 A、C 附近，仅示意）
tc = np.linspace(-0.9, 0.9, 120)
curve_hint = np.array([pt(t, rf0 + 0.9 * t) for t in tc])
ax.plot(curve_hint[:, 0], curve_hint[:, 1], color="#b9c4d0", lw=1.2, alpha=0.85, zorder=2)
ax.text(curve_hint[-1][0] + 0.04, curve_hint[-1][1] + 0.04, "曲线",
        fontsize=F - 2.5, color=GREY)
# 弧（横向边 r dθ）
ax.plot(arc[:, 0], arc[:, 1], color=GREEN, lw=3.0, zorder=5)
mid = arc[len(arc) // 2]
ax.text(mid[0] - 0.30, mid[1] - 0.04, "$r\\,\\mathrm{d}\\theta$", fontsize=F, color=GREEN)
# 径向边 dr
ax.plot([B[0], C[0]], [B[1], C[1]], color=ORANGE, lw=3.0, zorder=5)
ax.text(C[0] + 0.04, (B[1] + C[1]) / 2, "$\\mathrm{d}r$", fontsize=F, color=ORANGE)
# 斜边 ds
ax.plot([A[0], C[0]], [A[1], C[1]], color=RED, lw=3.0, zorder=6)
ax.annotate("", xy=((A[0] + C[0]) / 2 - 0.03, (A[1] + C[1]) / 2 - 0.03), xytext=(A[0] - 0.36, (A[1] + C[1]) / 2 + 0.26),
            arrowprops=dict(arrowstyle="->", color=RED, lw=1.0))
ax.text(A[0] - 0.44, (A[1] + C[1]) / 2 + 0.30, "$\\mathrm{d}s$",
        fontsize=F + 2, color=RED)
ax.plot([A[0]], [A[1]], "o", color=INK, ms=6, zorder=7)
ax.text(0.02, 0.96, "$\\mathrm{d}s$ 是斜边，两直角边是 $\\mathrm{d}r$ 与 $r\\,\\mathrm{d}\\theta$",
        transform=ax.transAxes, fontsize=F - 1.5, color=INK, va="top")
ax.text(0.02, 0.03, "$\\mathrm{d}s=\\sqrt{\\left(\\mathrm{d}r\\right)^{2}+\\left(r\\,\\mathrm{d}\\theta\\right)^{2}}$（勾股定理）",
        transform=ax.transAxes, fontsize=F - 1.5, color=INK, va="bottom")
ax.set_title("弧长：一小段近似成直角三角形，\n径向 $\\mathrm{d}r$、横向 $r\\,\\mathrm{d}\\theta$，斜边 $\\mathrm{d}s$",
             fontsize=T - 0.5, color=INK, pad=8)

fig.subplots_adjust(left=0.02, right=0.98, top=0.87, bottom=0.03)
fig.savefig(BASE + "pc-arclen-triangle.png", dpi=170)
plt.close(fig)


# ============================================
# 圆的渐开线（单图）
fig, ax = plt.subplots(figsize=(7.0, 6.4), dpi=170)
R = 1.0
t = np.linspace(0, 4 * np.pi, 900)
x = R * (np.cos(t) + t * np.sin(t))
y = R * (np.sin(t) - t * np.cos(t))
th_all = np.linspace(0, 2 * np.pi, 400)
ax.plot(R * np.cos(th_all), R * np.sin(th_all), color="#d8c9b4", lw=1.6, ls="--")
ax.plot(x, y, color=RED, lw=2.4)
tp = 3.2
u0 = np.array([np.cos(tp), np.sin(tp)])
Tvec = np.array([np.sin(tp), -np.cos(tp)])
P0 = R * u0
P1 = P0 + tp * R * Tvec
ax.plot([P0[0], P1[0]], [P0[1], P1[1]], color=BROWN, lw=1.6)
ax.text((P0[0]+P1[0])/2 - 0.75, (P0[1]+P1[1])/2 - 0.30, "线，长 $Rt$",
        fontsize=F - 1, color=BROWN)
ax.plot([P0[0]], [P0[1]], "o", color=BROWN, ms=5)
ax.plot([0], [0], "o", color=INK, ms=5)
ax.annotate("切点", xy=(P0[0], P0[1]), xytext=(P0[0]*0.4, P0[1]*0.55),
            fontsize=F - 1.5, color=GREY, arrowprops=dict(arrowstyle="->", color=GREY, lw=0.9))
# 弧长标记（基圆上从 (R,0) 到 P0 的弧）
arc_t = np.linspace(0, tp, 60)
arc_r = 0.86
ax.plot(arc_r * R * np.cos(arc_t), arc_r * R * np.sin(arc_t), color=GREEN, lw=1.8, ls=":")
ax.text(arc_r * R * np.cos(tp / 2) - 0.42, arc_r * R * np.sin(tp / 2) - 0.28,
        "弧长 $Rt$", fontsize=F - 1, color=GREEN)
ax.text(0.15, -0.36, "$O$", fontsize=F, color=INK)
ax.text(-0.55, 1.02, "基圆", fontsize=F - 1, color=GREY)
ax.text(-3.5, -3.3, "$x=R(\\cos t+t\\sin t)$", fontsize=F, color=INK)
ax.text(-3.5, -3.95, "$y=R(\\sin t-t\\cos t)$", fontsize=F, color=INK)
ax.set_xlim(-3.6, 3.6); ax.set_ylim(-4.3, 3.5)
ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
for sp_ in ax.spines.values():
    sp_.set_color("none")
ax.set_title("圆的渐开线：细线绷紧拉开，线端点轨迹（红线）",
             fontsize=T - 0.5, color=INK, pad=10)
fig.tight_layout()
fig.savefig(BASE + "geo2-involute.png", dpi=170)
plt.close(fig)


# ============================================
# 渐开线齿形（示意）
fig, axes = plt.subplots(1, 2, figsize=(12.6, 6.4), dpi=170)

def involute_curve(rb, t0, t1, n=200):
    t = np.linspace(t0, t1, n)
    x = rb * (np.cos(t) + t * np.sin(t))
    y = rb * (np.sin(t) - t * np.cos(t))
    return x, y

def rot(x, y, ang):
    c, s = np.cos(ang), np.sin(ang)
    return c*x - s*y, s*x + c*y

# 左：一个齿
ax = axes[0]
rb = 1.0
pitch = 2 * np.pi / 20
t0, t1 = 0.28, 0.80
x1, y1 = involute_curve(rb, t0, t1)
x2, y2 = x1[::-1], -y1[::-1]      # 关于 x 轴镜像
th_all = np.linspace(0, 2*np.pi, 400)
for rr, lbl in [(0.88, "齿根圆"), (1.35, "齿顶圆"), (rb, "基圆")]:
    style_ls = ":" if rr == 1.35 else "--"
    ax.plot(rr*np.cos(th_all), rr*np.sin(th_all), color="#d8c9b4", lw=1.4, ls=style_ls)
    ax.text(rr*0.68, rr*1.03, lbl, fontsize=F-2, color=GREY)
ax.plot(x1, y1, color=RED, lw=2.8)
ax.plot(x2, y2, color=RED, lw=2.8)
tt = np.linspace(-t0 + pitch/2, t0 - pitch/2 + pitch * 0, 30)
tt = np.linspace(-t0, t0, 40)
ax.plot(0.88*np.cos(tt + np.pi/2 + t0 - (t0)), 0.88*np.sin(tt + np.pi/2), color=ORANGE, lw=2.4)
ax.set_xlim(-2.4, 2.4); ax.set_ylim(-2.05, 2.1)
ax.text(-1.35, -1.55, "两条红色齿廓线是同一渐开线的镜像，\n根部用橙色圆弧封底", fontsize=F-1, color=INK)
ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
for sp_ in ax.spines.values():
    sp_.set_color("none")
ax.set_title("一个齿：两侧齿廓互为镜像的渐开线", fontsize=T-0.5, color=INK, pad=8)

# 右：整齿轮
ax = axes[1]
N = 20
for k in range(N):
    ang = k * pitch + pitch / 2 - t0   # 齿槽中心对齐
    xx1, yy1 = rot(x1, y1, ang + t0)
    xx2, yy2 = rot(x2, y2, ang + t0)
    ax.plot(xx1, yy1, color=RED, lw=1.6)
    ax.plot(xx2, yy2, color=RED, lw=1.6)
ax.plot(rb*np.cos(th_all), rb*np.sin(th_all), color="#d8c9b4", lw=1.2, ls="--")
ax.text(-2.3, -2.25, "20 个齿，每条齿廓都是\n同一基圆的渐开线（镜像后旋转）", fontsize=F-1, color=INK)
ax.set_xlim(-2.4, 2.4); ax.set_ylim(-2.55, 2.25)
ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
for sp_ in ax.spines.values():
    sp_.set_color("none")
ax.set_title("渐开线齿轮：20 个齿", fontsize=T-0.5, color=INK, pad=8)

fig.tight_layout()
fig.subplots_adjust(top=0.90)
fig.savefig(BASE + "geo2-involute-gear.png", dpi=170)
plt.close(fig)

print("done-more")
