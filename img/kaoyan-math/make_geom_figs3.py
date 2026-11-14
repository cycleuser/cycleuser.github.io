import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import matplotlib.patches as mpatches
from matplotlib.patches import Circle, Polygon, Rectangle

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
# 1 点到直线的距离：几何意义 + 数值计算
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(13.4, 5.6), dpi=150)
A, B, C = 3.0, 4.0, -12.0
P = np.array([6.0, 4.0])
t = -(A * P[0] + B * P[1] + C) / (A * A + B * B)
Q = P + t * np.array([A, B])
w = np.array([A, B]) / np.hypot(A, B)
xs = np.linspace(0.0, 7.2, 10)

for ax, mode in zip(axes, ["geo", "num"]):
    ax.plot(xs, (A * xs + C) / (-B), color=BLUE, lw=2.4)
    ax.plot([P[0], Q[0]], [P[1], Q[1]], color=RED, lw=2.4)
    ax.plot(*P, "o", color=ORANGE, ms=10, zorder=6)
    ax.plot(*Q, "o", color=GREEN, ms=8, zorder=6)
    # 直角标记
    u = (Q - P) / np.linalg.norm(Q - P)
    s0 = 0.34
    p1 = Q + s0 * u
    p2 = p1 + s0 * w
    p3 = Q + s0 * w
    ax.plot([p1[0], p2[0], p3[0]], [p1[1], p2[1], p3[1]], color=RED, lw=1.2)
    # 法向量：从直线上另取一点画出
    R = np.array([2.1, (A * 2.1 + C) / (-B)])
    ax.annotate("", xy=R + 1.25 * w, xytext=R,
                arrowprops=dict(arrowstyle="->", color="#7a5230", lw=1.9))
    ax.set_aspect("equal")
    ax.axhline(0, color=GREY, lw=0.9)
    ax.set_xlim(-2.6, 7.4); ax.set_ylim(-2.2, 5.6)
    ax.set_xlabel("$x$", fontsize=10, color=INK)
    ax.set_ylabel("$y$", fontsize=10, color=INK)
    style(ax)

ax = axes[0]
ax.text(P[0] + 0.15, P[1] + 0.14, r"$P(x_0,y_0)$", fontsize=11, color=ORANGE)
ax.text(Q[0] - 1.55, Q[1] - 0.85, r"垂足 $Q$", fontsize=10.5, color=GREEN)
ax.text((P[0] + Q[0]) / 2 + 0.15, (P[1] + Q[1]) / 2 - 0.05, r"$d$", fontsize=13, color=RED)
ax.text(2.1 + 1.30 * w[0], (A * 2.1 + C) / (-B) + 1.30 * w[1] + 0.10,
        r"$\vec{n}=(A,B)$", fontsize=10.5, color="#7a5230")
ax.text(-2.45, 5.25, r"$Ax+By+C=0$", fontsize=11.5, color=BLUE)
ax.text(-2.45, 4.30, r"$d=\frac{|Ax_0+By_0+C|}{\sqrt{A^2+B^2}}$", fontsize=14, color=RED)
ax.text(-2.45, 3.10, "距离沿法向量量取：", fontsize=10, color=GREY)
ax.text(-2.45, 2.70, "把点代进方程，再除", fontsize=10, color=GREY)
ax.text(-2.45, 2.30, "以法向量的长度", fontsize=10, color=GREY)
ax.set_title("几何意义：垂足与法向量", fontsize=12, color=INK)

ax = axes[1]
ax.text(P[0] + 0.15, P[1] + 0.14, r"$P(6,4)$", fontsize=11, color=ORANGE)
ax.text(Q[0] - 1.90, Q[1] - 0.85, r"$Q(3.36,0.48)$", fontsize=10, color=GREEN)
ax.text((P[0] + Q[0]) / 2 + 0.15, (P[1] + Q[1]) / 2 - 0.10, r"$d=4.4$", fontsize=12.5, color=RED)
ax.text(2.1 + 1.30 * w[0], (A * 2.1 + C) / (-B) + 1.30 * w[1] + 0.10,
        r"$\vec{n}=(3,4)$，$|\vec{n}|=5$", fontsize=10, color="#7a5230")
ax.text(-2.45, 5.25, r"直线 $3x+4y-12=0$，点 $P(6,4)$", fontsize=10.5, color=INK)
ax.text(-2.45, 4.35, r"$d=\frac{|3\cdot6+4\cdot4-12|}{\sqrt{3^2+4^2}}$", fontsize=13, color=RED)
ax.text(-2.45, 3.15, r"$=\frac{|18+16-12|}{5}=\frac{22}{5}=4.4$", fontsize=13, color=RED)
ax.text(-2.45, 2.10, "分子：把点代进方程后的数", fontsize=10, color=GREY)
ax.text(-2.45, 1.68, "分母：法向量的长度", fontsize=10, color=GREY)
ax.set_title("数值：代进去、除以法向量长度", fontsize=12, color=INK)

fig.tight_layout()
fig.savefig(BASE + "geo3-point-line-dist.png", dpi=150)
plt.close(fig)


# ============================================================
# 2 椭圆：绳线构造 + 几何元素
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(12.8, 5.2), dpi=150)

a, b = 3.0, 2.0
c = np.sqrt(a * a - b * b)
tt = np.linspace(0, 2 * np.pi, 500)

# 左：绳线构造
ax = axes[0]
ax.plot(a * np.cos(tt), b * np.sin(tt), color=BLUE, lw=2.4)
F1, F2 = np.array([-c, 0]), np.array([c, 0])
for F, lab, dx in [(F1, "$F_1$", -0.55), (F2, "$F_2$", 0.15)]:
    ax.plot(*F, "o", color=RED, ms=9, zorder=6)
    ax.text(F[0] + dx, F[1] + 0.14, lab, fontsize=11, color=RED)
cols = [GREEN, ORANGE, "#7a5230"]
for th, col in zip([np.deg2rad(62), np.deg2rad(118), np.deg2rad(200)], cols):
    P = np.array([a * np.cos(th), b * np.sin(th)])
    ax.plot([F1[0], P[0]], [F1[1], P[1]], color=col, lw=1.4, alpha=0.9)
    ax.plot([F2[0], P[0]], [F2[1], P[1]], color=col, lw=1.4, alpha=0.9)
    ax.plot(*P, "o", color=col, ms=6, zorder=6)
    ax.text(P[0] + 0.10, P[1] + 0.10, "$P$", fontsize=10, color=col)
ax.text(-1.55, -1.45, "三处之和都等于 $2a=6$", fontsize=11, color=INK)
ax.text(-4.15, -2.55, "把绳子的两端固定在 $F_1,F_2$，绳长 $2a$，", fontsize=10, color=INK)
ax.text(-4.15, -2.95, "笔尖绷紧划过一圈，画出的就是椭圆", fontsize=10, color=INK)
ax.set_title("定义：到两焦点距离之和为 $2a$", fontsize=12, color=INK)
ax.set_aspect("equal"); cross(ax, (-4.4, 4.4), (-3.3, 3.2))
ax.set_xlabel("$x$", fontsize=10, color=INK); ax.set_ylabel("$y$", fontsize=10, color=INK)
style(ax)

# 右：几何元素
ax = axes[1]
ax.plot(a * np.cos(tt), b * np.sin(tt), color=BLUE, lw=2.4)
for F, lab, dx in [(F1, "$F_1$", -0.52), (F2, "$F_2$", 0.14)]:
    ax.plot(*F, "o", color=RED, ms=8, zorder=6)
    ax.text(F[0] + dx, F[1] - 0.34, lab, fontsize=10.5, color=RED)
for A_, lab, dx in [(-a, "$A_1$", -0.40), (a, "$A_2$", 0.14)]:
    ax.plot([A_], [0], "o", color=GREEN, ms=6, zorder=6)
    ax.text(A_ + dx, 0.14, lab, fontsize=10.5, color=GREEN)
ax.plot([0, 0], [0, b], color=ORANGE, lw=1.5, ls="--")
ax.plot([0, c], [b, 0], color=ORANGE, lw=1.8)
ax.plot([0, c], [0, 0], color=ORANGE, lw=1.5)
ax.text(-0.30, b / 2, "$b$", fontsize=11, color=ORANGE)
ax.text(c / 2, -0.34, "$c$", fontsize=11, color=ORANGE)
ax.text(c / 2 + 0.16, b / 2 - 0.06, "$a$", fontsize=11, color=ORANGE)
ax.text(1.20, 1.58, "$a^2=b^2+c^2$", fontsize=11, color=ORANGE)
# 准线
for sgn in (-1, 1):
    ax.plot([sgn * a * a / c] * 2, [-2.3, 2.3], color=GREY, lw=1.2, ls="--")
ax.text(a * a / c - 0.15, 2.45, r"$x=\frac{a^2}{c}$", fontsize=10, color=GREY, ha="right")
ax.text(-a * a / c + 0.15, 2.45, r"$x=-\frac{a^2}{c}$", fontsize=10, color=GREY, ha="left")
# 通径
ax.plot([c, c], [-b * b / a, b * b / a], color="#7a5230", lw=1.8)
ax.text(c + 0.30, -b * b / a - 0.60, "通径 $\\frac{2b^2}{a}$", fontsize=9.5, color="#7a5230")
ax.text(-4.15, -2.55, r"$e=\frac{c}{a}<1$，准线 $x=\pm\frac{a^2}{c}$", fontsize=11, color=INK)
ax.set_title("元素：焦点、顶点、准线、通径", fontsize=12, color=INK)
ax.set_aspect("equal"); cross(ax, (-4.6, 4.6), (-3.3, 3.2))
ax.set_xlabel("$x$", fontsize=10, color=INK); ax.set_ylabel("$y$", fontsize=10, color=INK)
style(ax)

fig.tight_layout()
fig.savefig(BASE + "geo3-ellipse.png", dpi=150)
plt.close(fig)


# ============================================================
# 3 双曲线：定义（差为常数）+ 几何元素
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(12.8, 5.2), dpi=150)
a, b = 1.8, 1.4
c = np.sqrt(a * a + b * b)
s = np.linspace(-1.6, 1.6, 400)
xr, yr = a * np.cosh(s), b * np.sinh(s)

# 左：定义
ax = axes[0]
ax.plot(xr, yr, color=BLUE, lw=2.2)
ax.plot(xr, -yr, color=BLUE, lw=2.2)
ax.plot(-xr, yr, color=BLUE, lw=2.2)
ax.plot(-xr, -yr, color=BLUE, lw=2.2)
F1, F2 = np.array([-c, 0]), np.array([c, 0])
for F, lab, dx in [(F1, "$F_1$", -0.55), (F2, "$F_2$", 0.14)]:
    ax.plot(*F, "o", color=RED, ms=9, zorder=6)
    ax.text(F[0] + dx, F[1] + 0.14, lab, fontsize=11, color=RED)
P = np.array([a * np.cosh(0.75), b * np.sinh(0.75)])
Q = np.array([-a * np.cosh(0.75), b * np.sinh(0.75)])
for X, col in [(P, GREEN), (Q, ORANGE)]:
    ax.plot([F1[0], X[0]], [F1[1], X[1]], color=col, lw=1.4)
    ax.plot([F2[0], X[0]], [F2[1], X[1]], color=col, lw=1.4)
    ax.plot(*X, "o", color=col, ms=7, zorder=6)
ax.text(P[0] + 0.12, P[1] + 0.10, "$P$", fontsize=11, color=GREEN)
ax.text(Q[0] - 0.45, Q[1] + 0.10, "$Q$", fontsize=11, color=ORANGE)
ax.text(-1.30, -2.35, r"$|PF_1|-|PF_2|=2a$", fontsize=11, color=GREEN)
ax.text(-1.30, -2.95, r"$|QF_2|-|QF_1|=2a$", fontsize=11, color=ORANGE)
ax.set_title("定义：到两焦点距离之差的绝对值为 $2a$", fontsize=12, color=INK)
ax.set_aspect("equal"); cross(ax, (-4.6, 4.6), (-3.2, 3.4))
ax.set_xlabel("$x$", fontsize=10, color=INK); ax.set_ylabel("$y$", fontsize=10, color=INK)
style(ax)

# 右：元素
ax = axes[1]
ax.plot(xr, yr, color=BLUE, lw=2.2)
ax.plot(xr, -yr, color=BLUE, lw=2.2)
ax.plot(-xr, yr, color=BLUE, lw=2.2)
ax.plot(-xr, -yr, color=BLUE, lw=2.2)
xx = np.linspace(-4.2, 4.2, 10)
ax.plot(xx, b / a * xx, color=GREY, lw=1.2, ls="--")
ax.plot(xx, -b / a * xx, color=GREY, lw=1.2, ls="--")
ax.annotate(r"$y=\frac{b}{a}x$", xy=(3.6, b / a * 3.6), xytext=(3.15, 3.20),
            fontsize=10, color=GREY,
            arrowprops=dict(arrowstyle="->", color=GREY, lw=0.9))
ax.plot([0, a], [0, 0], color=ORANGE, lw=1.6)
ax.plot([a, a], [0, b], color=ORANGE, lw=1.6)
ax.plot([0, a], [0, b], color=ORANGE, lw=1.6)
ax.text(a / 2, -0.34, "$a$", fontsize=11, color=ORANGE)
ax.text(a + 0.10, b / 2, "$b$", fontsize=11, color=ORANGE)
ax.text(a / 2 - 0.32, b / 2 + 0.16, "$c$", fontsize=11, color=ORANGE)
ax.text(0.35, 1.85, "$c^2=a^2+b^2$", fontsize=11, color=ORANGE)
for F, lab, dx in [(F1, "$F_1$", -0.55), (F2, "$F_2$", 0.14)]:
    ax.plot(*F, "o", color=RED, ms=8, zorder=6)
    ax.text(F[0] + dx, F[1] - 0.36, lab, fontsize=10.5, color=RED)
ax.plot([a + 0.3], [0.0], "o", color=GREEN, ms=6)
ax.text(a - 0.55, 0.16, "$A_2$", fontsize=10.5, color=GREEN)
ax.text(-1.15, -2.80, r"$e=\frac{c}{a}>1$", fontsize=11, color=INK)
ax.set_title("元素：两支、渐近线、$a,b,c$ 三角形", fontsize=12, color=INK)
ax.set_aspect("equal"); cross(ax, (-4.7, 4.7), (-3.2, 3.2))
ax.set_xlabel("$x$", fontsize=10, color=INK); ax.set_ylabel("$y$", fontsize=10, color=INK)
style(ax)

fig.tight_layout()
fig.savefig(BASE + "geo3-hyperbola.png", dpi=150)
plt.close(fig)


# ============================================================
# 4 抛物线：定义（到焦点 = 到准线）+ 元素
# ============================================================
fig, axes = plt.subplots(1, 2, figsize=(12.8, 5.2), dpi=150)
p = 2.0
yy = np.linspace(-3.4, 3.4, 500)
xx = yy * yy / (2 * p)

# 左：定义
ax = axes[0]
ax.plot(xx, yy, color=BLUE, lw=2.4)
ax.plot([p / 2], [0], "o", color=RED, ms=9, zorder=6)
ax.text(p / 2 + 0.10, 0.22, r"$F\left(\frac{p}{2},0\right)$", fontsize=10.5, color=RED)
ax.axvline(-p / 2, color=GREY, lw=1.4, ls="--")
ax.text(-p / 2 - 0.10, 3.0, r"$x=-\frac{p}{2}$", fontsize=10, color=GREY, ha="right")
for yv, col in [(2.4, GREEN), (-2.0, ORANGE)]:
    P = np.array([yv * yv / (2 * p), yv])
    ax.plot([P[0], p / 2], [P[1], 0], color=col, lw=1.5)
    ax.plot([P[0], -p / 2], [P[1], P[1]], color=col, lw=1.5)
    ax.plot(*P, "o", color=col, ms=7, zorder=6)
    ax.text(P[0] + 0.12, P[1] + 0.12, "$P$", fontsize=10, color=col)
ax.text(-1.90, -2.75, "绿色、橙色两组线段各自等长", fontsize=10.5, color=INK)
ax.set_title("定义：到定点与定直线等距", fontsize=12, color=INK)
ax.set_aspect("equal"); cross(ax, (-2.0, 6.2), (-3.7, 3.7))
ax.set_xlabel("$x$", fontsize=10, color=INK); ax.set_ylabel("$y$", fontsize=10, color=INK)
style(ax)

# 右：元素
ax = axes[1]
ax.plot(xx, yy, color=BLUE, lw=2.4)
ax.plot([p / 2], [0], "o", color=RED, ms=9, zorder=6)
ax.text(p / 2 + 0.10, 0.22, r"$F\left(\frac{p}{2},0\right)$", fontsize=10.5, color=RED)
ax.axvline(-p / 2, color=GREY, lw=1.4, ls="--")
ax.text(-p / 2 - 0.10, 3.0, r"$x=-\frac{p}{2}$", fontsize=10, color=GREY, ha="right")
ax.plot([p / 2, p / 2], [-p, p], color="#7a5230", lw=2.0)
ax.text(2.10, -2.70, "通径 $=2p$", fontsize=10, color="#7a5230", ha="left")
ax.text(-1.90, -2.55, r"$|PF|=x_0+\frac{p}{2}$", fontsize=10.5, color=INK)
ax.text(-1.90, -3.15, r"$e=1$，$y^2=2px$", fontsize=11, color=INK)
ax.set_title("元素：焦点、准线、通径、焦半径", fontsize=12, color=INK)
ax.set_aspect("equal"); cross(ax, (-2.0, 6.2), (-3.7, 3.7))
ax.set_xlabel("$x$", fontsize=10, color=INK); ax.set_ylabel("$y$", fontsize=10, color=INK)
style(ax)

fig.tight_layout()
fig.savefig(BASE + "geo3-parabola.png", dpi=150)
plt.close(fig)

print("part 1 done")


# ============================================================
# 5 平面截圆锥：上排圆锥与截面，下排截面上的真实形状
# ============================================================
fig = plt.figure(figsize=(13.6, 8.4), dpi=150)
cases = [(0.42, 1.00, (-1.55, 1.55), "椭圆"),
         (1.00, 0.75, (-1.95, 1.95), "抛物线"),
         (1.85, 0.55, (-2.20, 2.20), "双曲线")]


def wire_cone(ax, H=2.2):
    th = np.linspace(0, 2 * np.pi, 200)
    for z in (H, -H):
        ax.plot(H * np.cos(th), H * np.sin(th), z, color=BLUE, lw=1.0, alpha=0.85)
    for a in np.linspace(0, 2 * np.pi, 16, endpoint=False):
        ax.plot([0, H * np.cos(a)], [0, H * np.sin(a)], [0, H], color=BLUE, lw=0.7, alpha=0.55)
        ax.plot([0, H * np.cos(a)], [0, H * np.sin(a)], [0, -H], color=BLUE, lw=0.7, alpha=0.55)
    ax.plot([0, 0], [0, 0], [-H, H], color=GREY, lw=0.9, ls="--")


def section_curves(m, c, vrange):
    vs = np.linspace(vrange[0], vrange[1], 700)
    if abs(m - 1) < 1e-9:
        return [((vs ** 2 - c ** 2) / (np.sqrt(2) * c), vs)]
    A = (1 - m ** 2) / (1 + m ** 2)
    B = -2 * c * m / np.hypot(1, m)
    disc = B ** 2 - 4 * A * (vs ** 2 - c ** 2)
    ok = disc >= 0
    vs, disc = vs[ok], disc[ok]
    up = (-B + np.sqrt(disc)) / (2 * A)
    um = (-B - np.sqrt(disc)) / (2 * A)
    if A > 0:
        return [(np.concatenate([up, um[::-1], up[:1]]),
                 np.concatenate([vs, vs[::-1], vs[:1]]))]
    return [(up, vs), (um, vs)]


for k, (m, c, vr, name) in enumerate(cases):
    e1 = np.array([1, 0, m]) / np.hypot(1, m)
    e2 = np.array([0, 1, 0])
    P0 = np.array([0, 0, c])

    # 上排：3D
    ax = fig.add_subplot(2, 3, k + 1, projection="3d")
    wire_cone(ax)
    corners = [(-2.6, vr[0]), (2.6, vr[0]), (2.6, vr[1]), (-2.6, vr[1]), (-2.6, vr[0])]
    for j in range(len(corners) - 1):
        u0, v0 = corners[j]; u1, v1 = corners[j + 1]
        ax.plot([P0[0] + u0 * e1[0], P0[0] + u1 * e1[0]],
                [P0[1] + u0 * e1[1], P0[1] + u1 * e1[1]],
                [P0[2] + u0 * e1[2], P0[2] + u1 * e1[2]], color=BLUE, lw=1.0, alpha=0.5)
    for u, v in section_curves(m, c, vr):
        ax.plot(P0[0] + u * e1[0] + v * e2[0],
                P0[1] + u * e1[1] + v * e2[1],
                P0[2] + u * e1[2] + v * e2[2], color=RED, lw=2.8, zorder=10)
    ax.set_box_aspect((1, 1, 1.2))
    ax.set_xlim(-2.8, 2.8); ax.set_ylim(-2.8, 2.8); ax.set_zlim(-2.8, 2.8)
    nrm = np.array([-m, 0.0, 1.0]); nrm = nrm / np.linalg.norm(nrm)
    ax.view_init(elev=np.degrees(np.arcsin(nrm[2])) - 6,
                 azim=np.degrees(np.arctan2(nrm[1], nrm[0])) + 12)
    ax.set_axis_off()
    ax.set_title("用平面去截：得到%s" % name, fontsize=10.5, color=INK, pad=0)

    # 下排：截面上的真实形状
    ax2 = fig.add_subplot(2, 3, k + 4)
    for u, v in section_curves(m, c, vr):
        ax2.plot(u, v, color=RED, lw=2.6)
    ax2.axhline(0, color="#e0e0e0", lw=0.9)
    ax2.axvline(0, color="#e0e0e0", lw=0.9)
    ax2.set_aspect("equal")
    ax2.set_xlim(-4.0, 3.2); ax2.set_ylim(vr[0] - 0.4, vr[1] + 0.4)
    ax2.set_title("%s（截面内的真实形状）" % name, fontsize=10.5, color=INK, pad=6)
    ax2.set_xlabel("截面内水平方向", fontsize=8.5, color=GREY)
    ax2.set_ylabel("截面内竖直方向", fontsize=8.5, color=GREY)
    ax2.tick_params(colors="#777", labelsize=7)
    for sp in ax2.spines.values():
        sp.set_color("#cccccc")

fig.suptitle("圆锥曲线：截出来的形状与截面内的真实形状", fontsize=13, color=INK)
fig.tight_layout(rect=(0, 0, 1, 0.95))
fig.savefig(BASE + "geo3-conic-cut.png", dpi=150)
plt.close(fig)

print("part 2 done")
