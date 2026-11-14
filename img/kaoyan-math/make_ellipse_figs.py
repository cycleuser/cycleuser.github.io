import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
from matplotlib.patches import Circle

plt.rcParams["font.family"] = ["PingFang SC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

INK, ORANGE, BLUE = "#2b2b2b", "#d2691e", "#2f4f6f"
CREAM, RED, GREEN, GREY, BROWN = "#f3e3ce", "#b03a2e", "#4a7c59", "#8a8a8a", "#7a5230"
BASE = "/Users/fred/Documents/GitHub/cycleuser/blog/output/img/kaoyan-math/"
F, T = 12.5, 13.5


def frame(ax, xlim, ylim, title):
    ax.axhline(0, color="#dcdcdc", lw=0.9, zorder=1)
    ax.axvline(0, color="#dcdcdc", lw=0.9, zorder=1)
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    ax.set_aspect("equal")
    ax.set_xlabel("$x$", fontsize=11, color=INK)
    ax.set_ylabel("$y$", fontsize=11, color=INK)
    ax.tick_params(colors="#666", labelsize=9)
    for sp in ax.spines.values():
        sp.set_color("#bbbbbb")
    ax.set_title(title, fontsize=T, color=INK, pad=10)


# ============ 1 定义（绳线） ============
a, b = 2.7, 1.9
c = np.sqrt(a * a - b * b)
th = np.linspace(0, 2 * np.pi, 600)
fig, ax = plt.subplots(figsize=(6.8, 5.4), dpi=150)
frame(ax, (-3.6, 3.6), (-2.9, 2.9), "定义：到两焦点距离之和为 $2a$")
ax.plot(a * np.cos(th), b * np.sin(th), color=BLUE, lw=2.6, zorder=3)
F1, F2 = np.array([-c, 0]), np.array([c, 0])
for Fp, lab, dx in [(F1, "$F_1$", -0.42), (F2, "$F_2$", 0.10)]:
    ax.plot(*Fp, "o", color=RED, ms=9, zorder=6)
    ax.text(Fp[0] + dx, Fp[1] - 0.34, lab, fontsize=F, color=RED)
for t0, col in [(np.deg2rad(58), GREEN), (np.deg2rad(122), ORANGE), (np.deg2rad(205), BROWN)]:
    P = np.array([a * np.cos(t0), b * np.sin(t0)])
    ax.plot([F1[0], P[0]], [F1[1], P[1]], color=col, lw=1.6, zorder=4)
    ax.plot([F2[0], P[0]], [F2[1], P[1]], color=col, lw=1.6, zorder=4)
    ax.plot(*P, "o", color=col, ms=7, zorder=6)
ax.text(-3.45, 2.45, r"$|PF_1|+|PF_2|=2a$", fontsize=F, color=INK)
ax.text(-3.45, -2.05, "三处取点的两段之和都相等", fontsize=F - 1.5, color=GREY)
ax.text(-3.45, -2.55, "绳长取 $2a$，笔尖绷紧绕一圈", fontsize=F - 1.5, color=GREY)
fig.tight_layout(); fig.savefig(BASE + "ellipse-definition.png", dpi=150); plt.close(fig)


# ============ 2 元素：a,b,c 与顶点焦点 ============
a, b = 3.0, 2.0
c = np.sqrt(a * a - b * b)
fig, ax = plt.subplots(figsize=(6.8, 5.4), dpi=150)
frame(ax, (-4.0, 4.0), (-3.0, 3.0), "元素：顶点、焦点与 $a,b,c$ 三角形")
ax.plot(a * np.cos(th), b * np.sin(th), color=BLUE, lw=2.6, zorder=3)
for pt, lab, ox, oy, col in [((-a, 0), "$A_1$", -0.42, 0.12, GREEN), ((a, 0), "$A_2$", 0.12, 0.12, GREEN),
                             ((0, b), "$B_1$", 0.12, 0.12, GREEN), ((0, -b), "$B_2$", 0.12, -0.40, GREEN),
                             ((-c, 0), "$F_1$", -0.42, -0.36, RED), ((c, 0), "$F_2$", 0.12, -0.36, RED)]:
    ax.plot(*pt, "o", color=col, ms=8, zorder=6)
    ax.text(pt[0] + ox, pt[1] + oy, lab, fontsize=F - 0.5, color=col)
ax.plot([0, 0], [0, b], color=ORANGE, lw=2.0, zorder=4)
ax.plot([0, c], [0, 0], color=ORANGE, lw=2.0, zorder=4)
ax.plot([c, 0], [0, b], color=ORANGE, lw=2.2, zorder=4)
ax.plot([0], [0], "o", color=INK, ms=5, zorder=6)
ax.text(-0.30, -0.36, "$O$", fontsize=F - 0.5, color=INK)
ax.text(-0.26, b / 2, "$b$", fontsize=F, color=ORANGE)
ax.text(c / 2 - 0.02, -0.34, "$c$", fontsize=F, color=ORANGE)
ax.text(c / 2 + 0.16, b / 2 + 0.02, "$a$", fontsize=F, color=ORANGE)
ax.text(1.30, 1.95, "$a^2=b^2+c^2$", fontsize=F + 0.5, color=ORANGE)
ax.text(-3.85, -2.35, r"$|PF_1|+|PF_2|=2a$，$e=\dfrac{c}{a}<1$", fontsize=F - 0.5, color=INK)
ax.text(-3.85, -2.80, "半长轴 $a$、半短轴 $b$、半焦距 $c$", fontsize=F - 1.5, color=GREY)
fig.tight_layout(); fig.savefig(BASE + "ellipse-elements.png", dpi=150); plt.close(fig)


# ============ 3 离心率：e 从小到大 ============
fig, ax = plt.subplots(figsize=(6.8, 5.4), dpi=150)
frame(ax, (-3.4, 4.2), (-3.2, 3.2), "离心率 $e=\\frac{c}{a}$：从圆到扁")
a = 2.6
for e, col, lab in [(0.0, GREEN, "$e=0$（圆）"), (0.45, ORANGE, "$e=0.45$"),
                    (0.75, RED, "$e=0.75$"), (0.93, BROWN, "$e=0.93$")]:
    c = a * e
    bb = a * np.sqrt(1 - e * e)
    ax.plot(a * np.cos(th), bb * np.sin(th), color=col, lw=2.2, zorder=3, label=lab)
    if e > 0:
        ax.plot([c], [0], "o", color=col, ms=6, zorder=6)
ax.legend(loc="upper right", fontsize=F - 2, frameon=False, bbox_to_anchor=(1.02, 1.0))
ax.text(-3.3, 2.95, "四条曲线共用同一个长轴 $2a$", fontsize=F - 1.5, color=INK)
ax.text(-3.3, -2.75, "$e=0$ 时 $c=0$，两个焦点重合于中心，", fontsize=F - 1.5, color=GREEN)
ax.text(-3.3, -3.10, "椭圆就是圆 $x^2+y^2=a^2$", fontsize=F - 1.5, color=GREEN)
fig.tight_layout(); fig.savefig(BASE + "ellipse-eccentricity.png", dpi=150); plt.close(fig)


# ============ 4 准线 ============
a, b = 2.2, 1.6
c = np.sqrt(a * a - b * b)
d_val = a * a / c
fig, ax = plt.subplots(figsize=(6.8, 5.4), dpi=150)
frame(ax, (-4.0, 4.0), (-2.6, 2.6), "准线：$\\frac{|PF|}{d(P,l)}=e$")
ax.plot(a * np.cos(th), b * np.sin(th), color=BLUE, lw=2.6, zorder=3)
for sgn in (-1, 1):
    ax.plot([sgn * d_val] * 2, [-2.2, 2.2], color=GREY, lw=1.6, ls="--", zorder=2)
ax.text(d_val + 0.10, 2.25, r"$x=\frac{a^2}{c}$", fontsize=F - 0.5, color=GREY)
ax.text(-d_val - 0.10, 2.25, r"$x=-\frac{a^2}{c}$", fontsize=F - 0.5, color=GREY, ha="right")
F2 = np.array([c, 0])
ax.plot(*F2, "o", color=RED, ms=9, zorder=6)
ax.text(F2[0] + 0.10, -0.34, "$F_2$", fontsize=F, color=RED)
t0 = np.deg2rad(62)
P = np.array([a * np.cos(t0), b * np.sin(t0)])
ax.plot([F2[0], P[0]], [F2[1], P[1]], color=GREEN, lw=2.0, zorder=5)
ax.plot([P[0], d_val], [P[1], P[1]], color=ORANGE, lw=2.0, zorder=5)
ax.plot(*P, "o", color=INK, ms=7, zorder=6)
ax.text(P[0] + 0.10, P[1] + 0.12, "$P$", fontsize=F, color=INK)
ax.text((F2[0] + P[0]) / 2 - 0.95, (F2[1] + P[1]) / 2 + 0.05, "$|PF_2|$", fontsize=F - 1, color=GREEN)
ax.text((P[0] + d_val) / 2, P[1] + 0.14, "$d$", fontsize=F - 1, color=ORANGE)
ax.text(-3.90, -2.20, r"$e=\frac{c}{a}$，准线到中心的距离是 $\frac{a^2}{c}$", fontsize=F - 1, color=INK)
fig.tight_layout(); fig.savefig(BASE + "ellipse-directrix.png", dpi=150); plt.close(fig)


# ============ 5 通径 ============
a, b = 3.0, 2.0
c = np.sqrt(a * a - b * b)
half = b * b / a
fig, ax = plt.subplots(figsize=(6.8, 5.4), dpi=150)
frame(ax, (-3.9, 3.9), (-2.8, 2.8), "通径：过焦点垂直于长轴的弦")
ax.plot(a * np.cos(th), b * np.sin(th), color=BLUE, lw=2.6, zorder=3)
ax.plot([c, c], [-half, half], color=ORANGE, lw=3.0, zorder=5)
ax.plot([c, c], [-half, half], "o", color=ORANGE, ms=7, zorder=6)
ax.plot([c], [0], "o", color=RED, ms=9, zorder=6)
ax.text(c + 0.12, half + 0.10, "通径 $=\\dfrac{2b^2}{a}$", fontsize=F - 0.5, color=ORANGE)
ax.text(c + 0.10, -0.34, "$F_2$", fontsize=F, color=RED)
ax.plot([0, c], [half, half], color=GREY, lw=1.0, ls=":", zorder=2)
ax.text(-3.75, -2.05, r"把 $x=c$ 代进 $\frac{x^2}{a^2}+\frac{y^2}{b^2}=1$", fontsize=F - 1, color=INK)
ax.text(-3.75, -2.50, r"得 $y=\pm\frac{b^2}{a}$，弦长就是 $\frac{2b^2}{a}$", fontsize=F - 1, color=INK)
fig.tight_layout(); fig.savefig(BASE + "ellipse-latus.png", dpi=150); plt.close(fig)


# ============ 6 焦半径 ============
a, b = 3.0, 2.1
c = np.sqrt(a * a - b * b)
e = c / a
fig, ax = plt.subplots(figsize=(6.8, 5.4), dpi=150)
frame(ax, (-4.0, 4.0), (-3.2, 2.9), "焦半径：$a\\pm ex_0$")
ax.plot(a * np.cos(th), b * np.sin(th), color=BLUE, lw=2.6, zorder=3)
t0 = np.deg2rad(55)
x0, y0 = a * np.cos(t0), b * np.sin(t0)
P = np.array([x0, y0])
F1, F2 = np.array([-c, 0]), np.array([c, 0])
ax.plot([F1[0], x0], [0, y0], color=GREEN, lw=2.0, zorder=5)
ax.plot([F2[0], x0], [0, y0], color=ORANGE, lw=2.0, zorder=5)
ax.plot([x0, x0], [0, y0], color=GREY, lw=1.1, ls="--", zorder=2)
ax.plot([0, x0], [0, 0], color=GREY, lw=1.1, ls=":", zorder=2)
ax.plot(*P, "o", color=INK, ms=7, zorder=6)
for Fp, lab, ox in [(F1, "$F_1$", -0.42), (F2, "$F_2$", 0.10)]:
    ax.plot(*Fp, "o", color=RED, ms=8, zorder=6)
    ax.text(Fp[0] + ox, -0.34, lab, fontsize=F - 0.5, color=RED)
ax.text(x0 + 0.10, y0 + 0.10, "$P(x_0,y_0)$", fontsize=F - 1, color=INK)
ax.text((F1[0] + x0) / 2 - 0.55, (y0) / 2 + 0.18, "$a+ex_0$", fontsize=F - 0.5, color=GREEN)
ax.text((F2[0] + x0) / 2 + 0.18, y0 / 2 + 0.18, "$a-ex_0$", fontsize=F - 0.5, color=ORANGE)
ax.text(x0 / 2 - 0.10, -0.34, "$x_0$", fontsize=F - 0.5, color=GREY)
ax.text(-3.85, -2.45, r"$|PF_1|=a+ex_0$，$|PF_2|=a-ex_0$", fontsize=F - 0.5, color=INK)
ax.text(-3.85, -2.95, "两式相加得 $2a$，与定义吻合", fontsize=F - 1.5, color=GREY)
fig.tight_layout(); fig.savefig(BASE + "ellipse-focal-radius.png", dpi=150); plt.close(fig)


# ============ 7 参数式与辅助圆 ============
a, b = 3.0, 1.8
fig, ax = plt.subplots(figsize=(6.8, 5.4), dpi=150)
frame(ax, (-4.0, 5.4), (-3.7, 3.5), "参数式：借辅助圆读 $t$")
ax.add_patch(Circle((0, 0), a, facecolor="none", edgecolor="#c9b295", lw=1.6, ls="--", zorder=2))
ax.plot(a * np.cos(th), b * np.sin(th), color=BLUE, lw=2.6, zorder=3)
t0 = np.deg2rad(52)
Q = np.array([a * np.cos(t0), a * np.sin(t0)])      # 辅助圆上的点
P = np.array([a * np.cos(t0), b * np.sin(t0)])      # 椭圆上的点
ax.plot([0, Q[0]], [0, Q[1]], color=GREY, lw=1.2, zorder=3)
ax.plot([Q[0], Q[0]], [0, Q[1]], color="#c9b295", lw=1.0, ls=":", zorder=2)
ax.plot([P[0], Q[0]], [P[1], Q[1]], color=ORANGE, lw=1.6, ls="--", zorder=4)
ax.plot([0, P[0]], [P[1], P[1]], color=ORANGE, lw=1.0, ls=":", zorder=2)
ax.plot([P[0], P[0]], [0, P[1]], color=GREEN, lw=1.6, zorder=4)
ax.add_patch(mpatches.Arc((0, 0), 1.1, 1.1, theta1=0, theta2=52, color=GREY, lw=1.3))
ax.plot(*Q, "o", color="#a9814f", ms=7, zorder=6)
ax.plot(*P, "o", color=RED, ms=8, zorder=6)
ax.text(0.60, 0.20, "$t$", fontsize=F + 0.5, color=GREY)
ax.text(Q[0] + 0.15, Q[1] + 0.12, "$(a\\cos t,\\ a\\sin t)$", fontsize=F - 2, color="#a9814f")
ax.text(Q[0] + 0.55, Q[1] / 2 + 0.10, "$a\\sin t$", fontsize=F - 1.5, color="#a9814f", rotation=90)
ax.text(P[0] + 0.12, P[1] - 0.05, "$P$", fontsize=F, color=RED)
ax.text(P[0] / 2 - 0.10, -0.34, "$a\\cos t$", fontsize=F - 1, color=GREY)
ax.text(P[0] + 0.12, P[1] / 2, "$b\\sin t$", fontsize=F - 1, color=GREEN)
ax.text(-3.85, 3.05, r"$x=a\cos t$，$y=b\sin t$", fontsize=F - 0.5, color=INK)
ax.text(-3.85, 2.62, "虚线圆半径 $a$，与椭圆共用同一个 $t$", fontsize=F - 2, color=GREY)
ax.text(-3.85, -3.35, "同一个 $t$：辅助圆上的高度是 $a\\sin t$，椭圆上的高度是 $b\\sin t$", fontsize=F - 2.5, color=INK)
fig.tight_layout(); fig.savefig(BASE + "ellipse-parametric.png", dpi=150); plt.close(fig)

print("ellipse figs done")
