import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

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


def style(ax):
    ax.spines[["top", "right"]].set_visible(False)
    for s in ax.spines.values():
        s.set_color(GREY)
    ax.tick_params(colors="#555")


def cross(ax, xlim, ylim):
    ax.axhline(0, color=GREY, lw=0.9)
    ax.axvline(0, color=GREY, lw=0.9)
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)


# ============================================================
# 1 两点距离、中点、定比分点
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(12.4, 5.0), dpi=150)
ax = axes[0]
A, B = np.array([0.6, 0.8]), np.array([4.2, 3.0])
M = (A + B) / 2
ax.plot([A[0], B[0]], [A[1], B[1]], color=BLUE, lw=2.2)
ax.plot(*A, "o", color=ORANGE, ms=9, zorder=6)
ax.plot(*B, "o", color=ORANGE, ms=9, zorder=6)
ax.plot(*M, "o", color=GREEN, ms=7, zorder=6)
ax.text(A[0] - 0.35, A[1] - 0.28, "$A(x_1,y_1)$", fontsize=10.5, color=ORANGE)
ax.text(B[0] + 0.10, B[1] + 0.08, "$B(x_2,y_2)$", fontsize=10.5, color=ORANGE)
ax.text(M[0] + 0.06, M[1] - 0.42, "$M$", fontsize=10.5, color=GREEN)
# 直角三角形的两条直角边
ax.plot([A[0], B[0]], [A[1], A[1]], color=GREY, lw=1.2, ls="--")
ax.plot([B[0], B[0]], [A[1], B[1]], color=GREY, lw=1.2, ls="--")
ax.text((A[0] + B[0]) / 2 - 0.35, A[1] - 0.30, "$x_2-x_1$", fontsize=10, color=GREY)
ax.text(B[0] + 0.10, (A[1] + B[1]) / 2, "$y_2-y_1$", fontsize=10, color=GREY)
ax.text(1.15, 0.10, r"$|AB|=\sqrt{\left(x_2-x_1\right)^2+\left(y_2-y_1\right)^2}$",
        fontsize=11.5, color=INK)
ax.set_title("两点距离与中点", fontsize=12, color=INK)
ax.set_aspect("equal"); cross(ax, (-0.4, 5.2), (-0.4, 3.8))
ax.set_xlabel("$x$", fontsize=10, color=INK); ax.set_ylabel("$y$", fontsize=10, color=INK)
style(ax)

ax = axes[1]
A, B = np.array([0.5, 0.7]), np.array([4.5, 3.2])
lam = 2.0
P = (A + lam * B) / (1 + lam)
ax.plot([A[0], B[0]], [A[1], B[1]], color=BLUE, lw=2.2)
for pt, col, lab, dx, dy in [(A, ORANGE, "$A$", -0.35, -0.30), (B, ORANGE, "$B$", 0.10, 0.05),
                             (P, RED, "$P$", -0.10, 0.22)]:
    ax.plot(*pt, "o", color=col, ms=9, zorder=6)
    ax.text(pt[0] + dx, pt[1] + dy, lab, fontsize=11, color=col)
ax.annotate("$AP$", xy=((A[0] + P[0]) / 2, (A[1] + P[1]) / 2 - 0.08),
            xytext=(0.95, 0.25), fontsize=10.5, color=GREEN,
            arrowprops=dict(arrowstyle="->", color=GREEN, lw=0.9))
ax.annotate("$PB$", xy=((P[0] + B[0]) / 2, (P[1] + B[1]) / 2 + 0.08),
            xytext=(3.35, 1.45), fontsize=10.5, color=GREEN,
            arrowprops=dict(arrowstyle="->", color=GREEN, lw=0.9))
ax.plot([A[0], A[0] + 0.18], [A[1], A[1]], color=GREY, lw=1.0)
ax.text(1.30, 3.55, r"$\dfrac{AP}{PB}=\lambda$，$x=\dfrac{x_1+\lambda x_2}{1+\lambda}$",
        fontsize=11.5, color=INK)
ax.set_title("定比分点：$\\lambda>0$ 内分，$\\lambda<0$ 外分", fontsize=12, color=INK)
ax.set_aspect("equal"); cross(ax, (-0.4, 5.4), (-0.3, 4.1))
ax.set_xlabel("$x$", fontsize=10, color=INK); ax.set_ylabel("$y$", fontsize=10, color=INK)
style(ax)
fig.tight_layout()
fig.savefig(BASE + "geo2-distance-basic.png", dpi=150)
plt.close(fig)


# ============================================================
# 2 两直线的位置关系与夹角
# ============================================================
fig, axes = plt.subplots(1, 3, figsize=(12.8, 4.2), dpi=150)

ax = axes[0]
x = np.linspace(-1.2, 3.6, 10)
ax.plot(x, 0.7 * x + 0.4, color=BLUE, lw=2.2)
ax.plot(x, 0.7 * x + 2.2, color=ORANGE, lw=2.2)
ax.text(2.15, 0.7 * 2.15 + 0.55, r"$l_1$", fontsize=11, color=BLUE)
ax.text(2.15, 0.7 * 2.15 + 2.35, r"$l_2$", fontsize=11, color=ORANGE)
ax.set_title("平行：$k_1=k_2$", fontsize=11.5, color=INK)
cross(ax, (-1.0, 3.8), (-0.6, 4.6)); ax.set_aspect("equal")

ax = axes[1]
x = np.linspace(-2.2, 2.6, 10)
ax.plot(x, 0.55 * x + 1.4, color=BLUE, lw=2.2)
ax.plot(x, -1.8 * x + 1.0, color=ORANGE, lw=2.2)
ax.text(-2.05, 0.55 * -2.05 + 1.75, r"$l_1$", fontsize=11, color=BLUE)
ax.text(1.55, -1.8 * 1.55 + 1.35, r"$l_2$", fontsize=11, color=ORANGE)
ax.set_title("垂直：$k_1k_2=-1$", fontsize=11.5, color=INK)
cross(ax, (-2.2, 2.8), (-3.6, 3.2)); ax.set_aspect("equal")

ax = axes[2]
k1, k2 = 0.35, 1.35
x = np.linspace(-1.0, 4.0, 10)
ax.plot(x, k1 * x + 0.5, color=BLUE, lw=2.2)
ax.plot(x, k2 * x - 1.5, color=ORANGE, lw=2.2)
X = (0.5 + 1.5) / (k2 - k1)
Y = k1 * X + 0.5
ax.plot([X], [Y], "o", color=RED, ms=7, zorder=6)
ax.plot([X, 3.6], [Y, Y], color=GREY, lw=1.0, ls="--")
import matplotlib.patches as mpatches
ax.add_patch(mpatches.Arc((X, Y), 2.4, 2.4, theta1=0, theta2=np.degrees(np.arctan(k2)),
                          color=RED, lw=1.4))
ax.text(X + 1.02, Y + 0.42, r"$\theta$", fontsize=12, color=RED)
ax.text(-0.85, -1.95, r"$\tan\theta=\left|\dfrac{k_2-k_1}{1+k_1k_2}\right|$",
        fontsize=11.5, color=INK)
ax.set_title("夹角", fontsize=11.5, color=INK)
cross(ax, (-1.0, 4.2), (-2.6, 3.6)); ax.set_aspect("equal")

for a in axes:
    a.set_xlabel("$x$", fontsize=10, color=INK)
    a.set_ylabel("$y$", fontsize=10, color=INK)
    style(a)
fig.tight_layout()
fig.savefig(BASE + "geo2-lines-relation.png", dpi=150)
plt.close(fig)


# ============================================================
# 3 焦点三角形
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(12.0, 5.0), dpi=150)

# 椭圆
ax = axes[0]
a, b = 2.6, 1.9
c = np.sqrt(a ** 2 - b ** 2)
t = np.linspace(0, 2 * np.pi, 400)
ax.plot(a * np.cos(t), b * np.sin(t), color=BLUE, lw=2.2)
th = np.deg2rad(112)
P = np.array([a * np.cos(th), b * np.sin(th)])
F1, F2 = np.array([-c, 0]), np.array([c, 0])
for F, lab, dx in [(F1, "$F_1$", -0.40), (F2, "$F_2$", 0.12)]:
    ax.plot(*F, "o", color=RED, ms=8, zorder=6)
    ax.text(F[0] + dx, F[1] + 0.14, lab, fontsize=10.5, color=RED)
ax.plot([F1[0], P[0]], [F1[1], P[1]], color=GREEN, lw=1.7)
ax.plot([F2[0], P[0]], [F2[1], P[1]], color=GREEN, lw=1.7)
ax.plot([F1[0], F2[0]], [0, 0], color=ORANGE, lw=1.7)
ax.plot(*P, "o", color=INK, ms=6, zorder=6)
ax.text(P[0] - 0.12, P[1] + 0.20, "$P$", fontsize=11, color=INK)
ax.text((F1[0] + P[0]) / 2 - 0.50, (F1[1] + P[1]) / 2 + 0.05, "$m$", fontsize=11, color=GREEN)
ax.text((F2[0] + P[0]) / 2 + 0.18, (F2[1] + P[1]) / 2 + 0.18, "$n$", fontsize=11, color=GREEN)
ax.text(-0.10, -0.42, "$2c$", fontsize=10.5, color=ORANGE)
ax.text(P[0] + 0.42, P[1] - 0.42, r"$\theta$", fontsize=11, color=RED)
ax.text(-2.95, -2.55, "$m+n=2a$", fontsize=11, color=GREEN, ha="left")
ax.text(-2.95, -3.15, r"$S=\dfrac{1}{2}mn\sin\theta=b^{2}\tan\dfrac{\theta}{2}$",
        fontsize=11, color=INK, ha="left")
ax.set_title("椭圆：焦点三角形的面积", fontsize=11.5, color=INK)
ax.set_aspect("equal"); cross(ax, (-3.2, 3.1), (-3.55, 2.45))
ax.set_xlabel("$x$", fontsize=10, color=INK); ax.set_ylabel("$y$", fontsize=10, color=INK)
style(ax)

# 双曲线（用参数式取点，避免极角取错）
ax = axes[1]
a, b = 1.7, 1.3
c = np.sqrt(a ** 2 + b ** 2)
tt = np.linspace(-1.45, 1.45, 500)
ax.plot(a * np.cosh(tt), b * np.sinh(tt), color=BLUE, lw=2.2)
ax.plot(-a * np.cosh(tt), b * np.sinh(tt), color=BLUE, lw=2.2)
P = np.array([a * np.cosh(0.62), b * np.sinh(0.62)])
F1, F2 = np.array([-c, 0]), np.array([c, 0])
for F, lab, dx in [(F1, "$F_1$", -0.42), (F2, "$F_2$", 0.12)]:
    ax.plot(*F, "o", color=RED, ms=8, zorder=6)
    ax.text(F[0] + dx, F[1] + 0.14, lab, fontsize=10.5, color=RED)
ax.plot([F1[0], P[0]], [F1[1], P[1]], color=GREEN, lw=1.7)
ax.plot([F2[0], P[0]], [F2[1], P[1]], color=GREEN, lw=1.7)
ax.plot([F1[0], F2[0]], [0, 0], color=ORANGE, lw=1.7)
ax.plot(*P, "o", color=INK, ms=6, zorder=6)
ax.text(P[0] + 0.20, P[1] + 0.06, "$P$", fontsize=11, color=INK, ha="left")
ax.text(-0.12, -0.42, "$2c$", fontsize=10.5, color=ORANGE)
ax.text(P[0] - 0.55, P[1] - 0.55, r"$\theta$", fontsize=11, color=RED)
ax.text(-3.15, -2.62, r"$\left|m-n\right|=2a$", fontsize=11, color=GREEN, ha="left")
ax.text(-3.15, -3.20, r"$S=b^{2}\cot\dfrac{\theta}{2}$", fontsize=11, color=INK, ha="left")
ax.set_title("双曲线：焦点三角形的面积", fontsize=11.5, color=INK)
ax.set_aspect("equal"); cross(ax, (-3.5, 3.3), (-3.55, 2.45))
ax.set_xlabel("$x$", fontsize=10, color=INK); ax.set_ylabel("$y$", fontsize=10, color=INK)
style(ax)
fig.tight_layout()
fig.savefig(BASE + "geo2-focus-triangle.png", dpi=150)
plt.close(fig)


# ============================================================
# 4 点差法：弦的中点和斜率
# ============================================================
fig, ax = plt.subplots(figsize=(7.4, 5.4), dpi=150)
a, b = 2.8, 2.0
t = np.linspace(0, 2 * np.pi, 400)
ax.plot(a * np.cos(t), b * np.sin(t), color=BLUE, lw=2.3)
t1, t2 = np.deg2rad(122), np.deg2rad(28)
A = np.array([a * np.cos(t1), b * np.sin(t1)])
B = np.array([a * np.cos(t2), b * np.sin(t2)])
M = (A + B) / 2
ax.plot([A[0], B[0]], [A[1], B[1]], color=RED, lw=1.8)
ax.plot(*A, "o", color=ORANGE, ms=7, zorder=6)
ax.plot(*B, "o", color=ORANGE, ms=7, zorder=6)
ax.plot(*M, "o", color=GREEN, ms=8, zorder=6)
ax.text(A[0] - 0.55, A[1] + 0.10, "$A(x_1,y_1)$", fontsize=10, color=ORANGE)
ax.text(B[0] + 0.12, B[1] + 0.10, "$B(x_2,y_2)$", fontsize=10, color=ORANGE)
ax.text(M[0] + 0.12, M[1] - 0.30, "$M(x_0,y_0)$", fontsize=10, color=GREEN)
ax.annotate("弦的斜率 $k$", xy=(0.62, 1.30), xytext=(1.45, 2.25), fontsize=10.5, color=RED,
            arrowprops=dict(arrowstyle="->", color=RED, lw=0.9))
ax.text(-3.05, -2.72, r"两式相减 $\Longrightarrow\ \dfrac{2x_0}{a^{2}}+\dfrac{2y_0}{b^{2}}k=0"
                       r"\ \Longrightarrow\ k=-\dfrac{b^{2}x_0}{a^{2}y_0}$",
        fontsize=10.5, color=INK)
ax.set_title("点差法：由弦的中点直接读出弦的斜率", fontsize=12, color=INK)
ax.set_aspect("equal"); cross(ax, (-3.2, 3.6), (-3.35, 2.75))
ax.set_xlabel("$x$", fontsize=10, color=INK); ax.set_ylabel("$y$", fontsize=10, color=INK)
style(ax)
fig.tight_layout()
fig.savefig(BASE + "geo2-midpoint-chord.png", dpi=150)
plt.close(fig)


# ============================================================
# 5 空间点到直线的距离（叉积）
# ============================================================
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

fig = plt.figure(figsize=(8.0, 6.6), dpi=150)
ax = fig.add_subplot(111, projection="3d")
M0 = np.array([0.0, 0.0, 0.0])
sv = np.array([2.0, 0.35, 0.25])
M = np.array([0.55, 1.75, 0.55])

ts = np.linspace(-0.12, 1.15, 6)
ax.plot(M0[0] + ts * sv[0], M0[1] + ts * sv[1], M0[2] + ts * sv[2], color=BLUE, lw=2.6)
Mp = M0 + sv
ax.scatter(*M0, color=ORANGE, s=50, depthshade=False)
ax.text(M0[0] - 0.30, M0[1] - 0.55, M0[2] - 0.05, "$M_0$", fontsize=11, color=ORANGE)
ax.text(Mp[0] + 0.08, Mp[1] + 0.02, Mp[2] + 0.06, "$M_0+\\vec{s}$", fontsize=10, color=BLUE)

# 平行四边形 M0, M, M+s, M0+s
poly = [[M0, M, M + sv, M0 + sv]]
ax.add_collection3d(Poly3DCollection(poly, facecolor=CREAM, alpha=0.55, edgecolor="#c9b295"))

ax.scatter(*M, color=RED, s=60, depthshade=False)
ax.text(M[0] + 0.06, M[1] + 0.06, M[2] + 0.10, "$M$", fontsize=11.5, color=RED)
tt = np.dot(M - M0, sv) / np.dot(sv, sv)
Q = M0 + tt * sv
ax.plot([M[0], Q[0]], [M[1], Q[1]], [M[2], Q[2]], color=GREEN, lw=2.6)
ax.scatter(*Q, color=GREEN, s=45, depthshade=False)
ax.text(Q[0] - 0.05, Q[1] - 0.36, Q[2] + 0.02, "$Q$", fontsize=11, color=GREEN)
mid = (M + Q) / 2
ax.text(mid[0] + 0.20, mid[1] + 0.12, mid[2], "$d$", fontsize=12.5, color=GREEN)
ax.plot([M0[0], M[0]], [M0[1], M[1]], [M0[2], M[2]], color=GREY, lw=1.1, ls="--")

ax.text2D(0.03, 0.93, r"平行四边形面积 $=\left\|\overrightarrow{M_0M}\times\vec{s}\right\|$",
          transform=ax.transAxes, fontsize=11, color=INK)
ax.text2D(0.03, 0.84, r"$d=\dfrac{\left\|\overrightarrow{M_0M}\times\vec{s}\right\|}{\left\|\vec{s}\right\|}$",
          transform=ax.transAxes, fontsize=12, color=RED)

ax.set_xlabel("$x$", fontsize=9.5); ax.set_ylabel("$y$", fontsize=9.5); ax.set_zlabel("$z$", fontsize=9.5)
ax.set_xlim(0, 2.6); ax.set_ylim(0, 2.6); ax.set_zlim(0, 1.6)
ax.view_init(elev=20, azim=-72)
ax.set_title("空间点到直线的距离：面积除以底边得高", fontsize=12, color=INK, pad=0)
for pane in (ax.xaxis, ax.yaxis, ax.zaxis):
    pane.pane.set_facecolor("white"); pane.pane.set_edgecolor("#dddddd")
fig.tight_layout()
fig.savefig(BASE + "geo2-point-line-3d.png", dpi=150)
plt.close(fig)


print("batch A done")


# ============================================================
# 6 极坐标系
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(11.8, 5.2), dpi=150)
ax = axes[0]
th = np.linspace(0, 2 * np.pi, 400)
for r in (1, 2, 3):
    ax.plot(r * np.cos(th), r * np.sin(th), color="#d8c9b4", lw=0.9)
for a in np.arange(0, np.pi, np.pi / 6):
    ax.plot([0, 3.4 * np.cos(a)], [0, 3.4 * np.sin(a)], color="#d8c9b4", lw=0.9)
    ax.plot([0, -3.4 * np.cos(a)], [0, -3.4 * np.sin(a)], color="#d8c9b4", lw=0.9)
P = (2.2 * np.cos(np.deg2rad(52)), 2.2 * np.sin(np.deg2rad(52)))
ax.plot(*P, "o", color=RED, ms=9, zorder=6)
ax.plot([0, P[0]], [0, P[1]], color=BLUE, lw=2.2)
import matplotlib.patches as mpatches
ax.add_patch(mpatches.Arc((0, 0), 1.3, 1.3, theta1=0, theta2=52, color=ORANGE, lw=1.6))
ax.text(0.72, 0.28, r"$\theta$", fontsize=12, color=ORANGE)
ax.text(1.02, 1.05, r"$\rho$", fontsize=12, color=BLUE)
ax.text(P[0] + 0.10, P[1] + 0.10, r"$P(\rho,\theta)$", fontsize=11, color=RED)
ax.text(-0.30, -0.42, "$O$", fontsize=11, color=INK)
ax.set_title("极坐标系：同心圆是等 $\\rho$ 线，射线是等 $\\theta$ 线", fontsize=11.5, color=INK)
ax.set_aspect("equal"); ax.axis("off")
ax.set_xlim(-3.3, 3.9); ax.set_ylim(-3.1, 3.4)

ax = axes[1]
th = np.linspace(0, 2 * np.pi, 600)
# r = 2cos(theta)：过极点的圆
r = 2 * np.cos(th)
ax.plot(r * np.cos(th), r * np.sin(th), color=BLUE, lw=2.2)
# 直线 x = 1：r = sec(theta)
tt2 = np.linspace(-1.2, 1.2, 400)
ax.plot(1 / np.cos(tt2) * np.cos(tt2), 1 / np.cos(tt2) * np.sin(tt2), color=RED, lw=2.0)
ax.plot([0], [0], "o", color=INK, ms=6, zorder=6)
ax.text(0.06, -0.28, "$O$", fontsize=11, color=INK)
ax.text(1.05, 1.35, r"$r=\sec\theta$", fontsize=11, color=RED)
ax.text(-0.95, 0.75, r"$r=2\cos\theta$", fontsize=11, color=BLUE)
ax.set_title(r"圆 $r=2\cos\theta$ 与直线 $x=1$ 即 $r=\sec\theta$", fontsize=11.5, color=INK)
ax.set_aspect("equal"); cross(ax, (-1.6, 2.6), (-1.6, 1.9))
ax.set_xlabel("$x$", fontsize=10, color=INK); ax.set_ylabel("$y$", fontsize=10, color=INK)
style(ax)
fig.tight_layout()
fig.savefig(BASE + "geo2-polar-basic.png", dpi=150)
plt.close(fig)


# ============================================================
# 7 常见极坐标曲线
# ============================================================
fig, axes = plt.subplots(2, 3, figsize=(13.0, 8.0), dpi=150)
th = np.linspace(0, 2 * np.pi, 2000)


def polar(ax, r, title, color=BLUE, lim=2.2, extra=None):
    x, y = r * np.cos(th), r * np.sin(th)
    ax.plot(x, y, color=color, lw=2.0)
    if extra:
        extra(ax)
    ax.set_title(title, fontsize=10.5, color=INK, pad=4)
    ax.set_aspect("equal")
    ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_color("#cccccc")


polar(axes[0][0], 1 + np.cos(th), r"心形线 $r=1+\cos\theta$", RED, 2.3)
polar(axes[0][1], np.sin(3 * th), r"三叶玫瑰线 $r=\sin 3\theta$", ORANGE, 1.2)
polar(axes[0][2], 0.45 * th, r"阿基米德螺线 $r=0.45\,\theta$", GREEN, 3.2)

# 双纽线 r^2 = cos 2theta，只在 cos2θ>=0 处有定义
t2 = np.concatenate([np.linspace(-np.pi / 4, np.pi / 4, 800),
                     np.linspace(3 * np.pi / 4, 5 * np.pi / 4, 800)])
r2 = np.sqrt(np.cos(2 * t2))
axes[1][0].plot(r2 * np.cos(t2), r2 * np.sin(t2), color=BLUE, lw=2.0)
axes[1][0].plot([-1.5, 1.5], [0, 0], color="#d8c9b4", lw=0.9)
axes[1][0].set_title(r"双纽线 $r^{2}=\cos 2\theta$", fontsize=10.5, color=INK, pad=4)
axes[1][0].set_aspect("equal"); axes[1][0].set_xlim(-1.4, 1.4); axes[1][0].set_ylim(-1.0, 1.0)
axes[1][0].set_xticks([]); axes[1][0].set_yticks([])

# 对数螺线 r = e^{0.22 theta}
th3 = np.linspace(0, 3 * np.pi, 1200)
r3 = np.exp(0.22 * th3)
axes[1][1].plot(r3 * np.cos(th3), r3 * np.sin(th3), color=GREEN, lw=2.0)
axes[1][1].set_title(r"对数螺线 $r=e^{0.22\theta}$", fontsize=10.5, color=INK, pad=4)
axes[1][1].set_aspect("equal")
_lim = np.exp(0.22 * 3 * np.pi) + 0.6
axes[1][1].set_xlim(-_lim, _lim); axes[1][1].set_ylim(-_lim, _lim)
axes[1][1].set_xticks([]); axes[1][1].set_yticks([])

# r = 1 - cos 的对比：玫瑰线四叶 r = |cos 2theta| 用 cos2θ 直接画四叶
polar(axes[0][0], 1 + np.cos(th), r"心形线 $r=1+\cos\theta$", RED, 2.3)
axes[1][2].plot(np.cos(2 * th) * np.cos(th), np.cos(2 * th) * np.sin(th),
                color=ORANGE, lw=2.0)
axes[1][2].set_title(r"四叶玫瑰线 $r=\cos 2\theta$", fontsize=10.5, color=INK, pad=4)
axes[1][2].set_aspect("equal"); axes[1][2].set_xlim(-1.2, 1.2); axes[1][2].set_ylim(-1.2, 1.2)
axes[1][2].set_xticks([]); axes[1][2].set_yticks([])

for row in axes:
    for a in row:
        for sp in a.spines.values():
            sp.set_color("#d6d6d6")
        a.set_xticks([]); a.set_yticks([])
fig.suptitle("常见的极坐标曲线", fontsize=13, color=INK)
fig.tight_layout()
fig.savefig(BASE + "geo2-polar-curves.png", dpi=150)
plt.close(fig)


# ============================================================
# 8 参数方程：圆与椭圆的参数化
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(11.8, 5.2), dpi=150)

ax = axes[0]
t = np.linspace(0, 2 * np.pi, 400)
ax.plot(np.cos(t), np.sin(t), color=BLUE, lw=2.2)
tt = np.deg2rad(56)
P = (np.cos(tt), np.sin(tt))
ax.plot([0, P[0]], [0, P[1]], color=GREY, lw=1.1, ls="--")
ax.plot([P[0], P[0]], [0, P[1]], color=ORANGE, lw=1.4, ls=":")
ax.plot([0, P[0]], [0, 0], color=GREEN, lw=1.4, ls=":")
ax.plot(*P, "o", color=RED, ms=8, zorder=6)
ax.plot([0, 1], [0, 0], color=GREY, lw=0.9)
import matplotlib.patches as mpatches
ax.add_patch(mpatches.Arc((0, 0), 0.75, 0.75, theta1=0, theta2=56, color=GREY, lw=1.2))
ax.text(0.42, 0.16, "$t$", fontsize=11.5, color=GREY)
ax.text(P[0] + 0.06, P[1] + 0.08, "$P$", fontsize=11, color=RED)
ax.text(P[0] / 2 - 0.04, -0.22, r"$\cos t$", fontsize=10.5, color=GREEN)
ax.text(P[0] + 0.08, P[1] / 2, r"$\sin t$", fontsize=10.5, color=ORANGE)
ax.text(-1.25, 1.28, r"$x=\cos t,\quad y=\sin t$", fontsize=11.5, color=INK)
ax.set_title("单位圆：$t$ 是圆心角", fontsize=11.5, color=INK)
ax.set_aspect("equal"); cross(ax, (-1.45, 1.55), (-1.35, 1.5))
ax.set_xlabel("$x$", fontsize=10, color=INK); ax.set_ylabel("$y$", fontsize=10, color=INK)
style(ax)

ax = axes[1]
a, b = 2.2, 1.35
ax.plot(a * np.cos(t), b * np.sin(t), color=BLUE, lw=2.2)
tt = np.deg2rad(56)
P = (a * np.cos(tt), b * np.sin(tt))
ax.plot([0, P[0]], [P[1], P[1]], color=GREY, lw=1.0, ls="--")
ax.plot([P[0], P[0]], [0, P[1]], color=GREY, lw=1.0, ls="--")
ax.plot([0, P[0]], [0, 0], color=GREEN, lw=1.3, ls=":")
ax.plot(*P, "o", color=RED, ms=8, zorder=6)
ax.plot(*[a * np.cos(tt)], *[0], "o", color=GREEN, ms=5)
ax.text(P[0] + 0.08, P[1] + 0.06, "$P$", fontsize=11, color=RED)
ax.text(a * np.cos(tt) + 0.04, -0.26, "$a\\cos t$", fontsize=10, color=GREEN)
ax.text(P[0] + 0.10, P[1] / 2, "$b\\sin t$", fontsize=10, color=GREY)
ax.text(-2.35, 1.55, r"$x=a\cos t,\quad y=b\sin t$", fontsize=11.5, color=INK)
ax.text(-2.52, -1.30, "椭圆：$t$ 不再等于圆心角", fontsize=10.5, color=RED)
ax.set_title("椭圆：消去 $t$ 得 $\\dfrac{x^{2}}{a^{2}}+\\dfrac{y^{2}}{b^{2}}=1$",
             fontsize=11.5, color=INK)
ax.set_aspect("equal"); cross(ax, (-2.6, 2.7), (-1.75, 1.85))
ax.set_xlabel("$x$", fontsize=10, color=INK); ax.set_ylabel("$y$", fontsize=10, color=INK)
style(ax)
fig.tight_layout()
fig.savefig(BASE + "geo2-param-basic.png", dpi=150)
plt.close(fig)


# ============================================================
# 9 摆线
# ============================================================
fig, ax = plt.subplots(figsize=(9.6, 4.4), dpi=150)
a = 1.0
t = np.linspace(0, 3 * np.pi, 900)
ax.plot(a * (t - np.sin(t)), a * (1 - np.cos(t)), color=BLUE, lw=2.4, label="摆线")
ax.axhline(0, color=GREY, lw=1.2)
ax.axhline(2 * a, color=GREY, lw=0.9, ls="--")
ax.text(0.05, 2 * a + 0.10, "最高 $2a$", fontsize=10, color=GREY)
# 三个位置的滚动圆
for t0, col in [(np.pi / 2, ORANGE), (np.pi, RED), (3 * np.pi / 2, GREEN)]:
    cx, cy = a * t0, a
    th = np.linspace(0, 2 * np.pi, 200)
    ax.plot(cx + a * np.cos(th), cy + a * np.sin(th), color=col, lw=1.2, alpha=0.9)
    # 半径到接触点与到轨迹点
    Px, Py = a * (t0 - np.sin(t0)), a * (1 - np.cos(t0))
    ax.plot([cx, Px], [cy, Py], color=col, lw=1.4)
    ax.plot([cx], [cy], "o", color=col, ms=4)
    ax.plot([cx, cx], [0, cy], color=col, lw=0.9, ls=":")
    ax.plot([Px], [Py], "o", color=col, ms=6)
ax.text(4.75, 2.68, r"$x=a(t-\sin t),\quad y=a(1-\cos t)$", fontsize=12, color=INK)
ax.text(4.75, 2.26, "圆沿直线滚动，圆周上一点的轨迹", fontsize=10.5, color=GREY)
ax.set_title("摆线", fontsize=12.5, color=INK)
ax.set_aspect("equal"); ax.set_xlim(-0.4, 9.6); ax.set_ylim(-0.6, 3.0)
ax.set_xlabel("$x$", fontsize=10, color=INK); ax.set_ylabel("$y$", fontsize=10, color=INK)
style(ax)
fig.tight_layout()
fig.savefig(BASE + "geo2-cycloid.png", dpi=150)
plt.close(fig)


# ============================================================
# 10 星形线与渐开线
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(11.2, 5.0), dpi=150)

ax = axes[0]
t = np.linspace(0, 2 * np.pi, 800)
a = 1.6
ax.plot(a * np.cos(t) ** 3, a * np.sin(t) ** 3, color=BLUE, lw=2.3)
ax.plot(a * np.cos(t), a * np.sin(t), color="#d8c9b4", lw=1.0, ls="--")
for ang in np.arange(0, 2 * np.pi, np.pi / 2):
    ax.plot([0, a * np.cos(ang)], [0, a * np.sin(ang)], color=GREY, lw=0.8, ls=":")
ax.text(-1.85, 1.62, r"$x=a\cos^{3}t,\quad y=a\sin^{3}t$", fontsize=11, color=INK)
ax.text(-1.85, 1.25, r"$x^{2/3}+y^{2/3}=a^{2/3}$", fontsize=11, color=BLUE)
ax.set_title("星形线（内摆线的一种）", fontsize=11.5, color=INK)
ax.set_aspect("equal"); cross(ax, (-2.0, 2.0), (-1.9, 1.9))
ax.set_xlabel("$x$", fontsize=10, color=INK); ax.set_ylabel("$y$", fontsize=10, color=INK)
style(ax)

ax = axes[1]
R = 1.0
t = np.linspace(0, 2.6 * np.pi, 900)
ax.plot(R * (np.cos(t) + t * np.sin(t)), R * (np.sin(t) - t * np.cos(t)),
        color=BLUE, lw=2.2)
th = np.linspace(0, 2 * np.pi, 300)
ax.plot(R * np.cos(th), R * np.sin(th), color=GREY, lw=1.2, ls="--")
t0 = 1.9
P = (R * (np.cos(t0) + t0 * np.sin(t0)), R * (np.sin(t0) - t0 * np.cos(t0)))
T = (R * np.cos(t0), R * np.sin(t0))
ax.plot([T[0], P[0]], [T[1], P[1]], color=RED, lw=1.8)
ax.plot(*T, "o", color=GREEN, ms=6, zorder=6)
ax.plot(*P, "o", color=ORANGE, ms=6, zorder=6)
ax.text(T[0] - 0.55, T[1] + 0.12, "切点", fontsize=9.5, color=GREEN)
ax.text(P[0] + 0.08, P[1] + 0.10, "$P$", fontsize=10.5, color=ORANGE)
ax.text(-3.75, -2.15, r"$x=R(\cos t+t\sin t)$", fontsize=10.5, color=INK)
ax.text(-3.75, -2.62, r"$y=R(\sin t-t\cos t)$", fontsize=10.5, color=INK)
ax.set_title("圆的渐开线：把切线一段段展开", fontsize=11.5, color=INK)
ax.set_aspect("equal"); cross(ax, (-3.8, 4.4), (-3.4, 3.4))
ax.set_xlabel("$x$", fontsize=10, color=INK); ax.set_ylabel("$y$", fontsize=10, color=INK)
style(ax)
fig.tight_layout()
fig.savefig(BASE + "geo2-astroid-involute.png", dpi=150)
plt.close(fig)


# ============================================================
# 11 参数方程求导：切线斜率 = y'(t)/x'(t)
# ============================================================
fig, ax = plt.subplots(figsize=(7.6, 5.4), dpi=150)
t = np.linspace(0, 2 * np.pi, 500)
a, b = 2.6, 1.7
X, Y = a * np.cos(t), b * np.sin(t)
ax.plot(X, Y, color=BLUE, lw=2.3)
t0 = np.deg2rad(52)
P = np.array([a * np.cos(t0), b * np.sin(t0)])
dx, dy = -a * np.sin(t0), b * np.cos(t0)
sc = 0.85
ax.annotate("", xy=(P[0] + sc * dx, P[1] + sc * dy), xytext=(P),
            arrowprops=dict(arrowstyle="->", color=RED, lw=2.0))
ax.plot([P[0], P[0] + sc * dx], [P[1], P[1]], color=GREEN, lw=1.4, ls="--")
ax.plot([P[0] + sc * dx, P[0] + sc * dx], [P[1], P[1] + sc * dy], color=ORANGE, lw=1.4, ls="--")
ax.plot(*P, "o", color=INK, ms=6, zorder=6)
ax.text(P[0] - 0.10, P[1] + 0.16, "$P$", fontsize=11, color=INK)
ax.text(P[0] + sc * dx / 2 - 0.35, P[1] - 0.30, "$x'(t)\\Delta t$", fontsize=10, color=GREEN)
ax.text(P[0] + sc * dx - 0.62, P[1] + sc * dy / 2 - 0.10, "$y'(t)\\Delta t$", fontsize=10, color=ORANGE)
ax.text(1.05, 1.95, "箭头方向 $(x'(t),y'(t))$", fontsize=10.5, color=RED)
ax.text(-2.90, -2.02, r"$\dfrac{\mathrm{d}y}{\mathrm{d}x}=\dfrac{y'(t)}{x'(t)}$",
        fontsize=12, color=INK)
ax.text(-2.90, -2.52, r"$\dfrac{\mathrm{d}^{2}y}{\mathrm{d}x^{2}}"
                       r"=\dfrac{\left(y'(t)/x'(t)\right)'}{x'(t)}$",
        fontsize=12, color=INK)
ax.set_title("参数方程求导：切线斜率由两个导数之比给出", fontsize=12, color=INK)
ax.set_aspect("equal"); cross(ax, (-3.1, 3.4), (-2.85, 2.25))
ax.set_xlabel("$x$", fontsize=10, color=INK); ax.set_ylabel("$y$", fontsize=10, color=INK)
style(ax)
fig.tight_layout()
fig.savefig(BASE + "geo2-param-tangent.png", dpi=150)
plt.close(fig)

print("batch B done")
