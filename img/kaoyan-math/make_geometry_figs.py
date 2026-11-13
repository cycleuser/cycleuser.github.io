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
GREY   = "#888888"

BASE = "/Users/fred/Documents/GitHub/cycleuser/blog/output/img/kaoyan-math/"


def style(ax):
    ax.spines[["top", "right"]].set_visible(False)
    for s in ax.spines.values():
        s.set_color(GREY)
    ax.tick_params(colors="#555")


def axes_cross(ax, xlim, ylim):
    ax.axhline(0, color=GREY, lw=0.9)
    ax.axvline(0, color=GREY, lw=0.9)
    ax.set_xlim(*xlim)
    ax.set_ylim(*ylim)


# ============================================================
# 图1 直线的倾斜角与斜率、点斜式
# ============================================================
fig, ax = plt.subplots(figsize=(7.4, 5.4), dpi=150)
k = 0.75
x = np.linspace(-0.6, 5.0, 10)
ax.plot(x, k * x + 1.0, color=BLUE, lw=2.4)
P = (2.0, k * 2.0 + 1.0)
ax.plot(*P, "o", color=ORANGE, ms=8, zorder=6)
ax.annotate("$P(x_0,y_0)$", xy=P, xytext=(P[0] + 0.12, P[1] - 0.55), fontsize=11, color=ORANGE)

# 倾斜角
import matplotlib.patches as mpatches
vx = 3.4
vy = k * vx + 1.0
ax.plot([vx, 5.0], [vy, vy], color=GREY, lw=1.0, ls="--")
arc = mpatches.Arc((vx, vy), 1.0, 1.0, theta1=0, theta2=np.degrees(np.arctan(k)),
                   color=RED, lw=1.5)
ax.add_patch(arc)
ax.text(vx + 0.55, vy + 0.16, r"$\alpha$", fontsize=13, color=RED)

# 斜率 = 上升 / 前进
ax.plot([P[0], P[0] + 1.6], [P[1], P[1]], color=GREEN, lw=1.4)
ax.plot([P[0] + 1.6, P[0] + 1.6], [P[1], P[1] + 1.6 * k], color=GREEN, lw=1.4)
ax.text(P[0] + 0.55, P[1] + 0.10, r"$\Delta x$", fontsize=10.5, color=GREEN)
ax.text(P[0] + 1.70, P[1] + 0.55, r"$\Delta y$", fontsize=10.5, color=GREEN)
ax.annotate(r"$k=\tan\alpha=\dfrac{\Delta y}{\Delta x}$",
            xy=(2.6, k * 2.6 + 1.0), xytext=(0.35, 4.10), fontsize=12, color=INK)

ax.set_title("直线的倾斜角、斜率与点斜式", fontsize=12.5, color=INK)
ax.set_xlabel("$x$", fontsize=11, color=INK)
ax.set_ylabel("$y$", fontsize=11, color=INK)
axes_cross(ax, (-0.8, 5.2), (-0.6, 4.9))
style(ax)
fig.tight_layout()
fig.savefig(BASE + "geo-line-slope.png", dpi=150)
plt.close(fig)


# ============================================================
# 图2 点到直线的距离
# ============================================================
fig, ax = plt.subplots(figsize=(7.4, 5.2), dpi=150)
A, B, C = 3.0, 4.0, -12.0
x = np.linspace(-1.2, 5.0, 10)
ax.plot(x, (A * x + C) / (-B), color=BLUE, lw=2.4)
P = (2.6, 4.2)
t = -(A * P[0] + B * P[1] + C) / (A * A + B * B)
Q = (P[0] + A * t, P[1] + B * t)
ax.plot([P[0], Q[0]], [P[1], Q[1]], color=RED, lw=1.8)
ax.plot(*P, "o", color=ORANGE, ms=8, zorder=6)
ax.plot(*Q, "o", color=GREEN, ms=7, zorder=6)
ax.annotate("$P(x_0,y_0)$", xy=P, xytext=(P[0] + 0.18, P[1] + 0.16), fontsize=11, color=ORANGE)
ax.annotate("垂足 $Q$", xy=Q, xytext=(Q[0] - 0.85, Q[1] - 0.62), fontsize=10.5, color=GREEN)
ax.text((P[0] + Q[0]) / 2 + 0.16, (P[1] + Q[1]) / 2 + 0.02, r"$d$", fontsize=12.5, color=RED)

# 直角标记
u = np.array([Q[0] - P[0], Q[1] - P[1]]); u = u / np.hypot(*u)
w = np.array([-B, A]); w = w / np.hypot(*w)
s0 = 0.26
a1 = np.array(Q) + s0 * u
a2 = a1 + s0 * w
a3 = np.array(Q) + s0 * w
ax.plot([a1[0], a2[0], a3[0]], [a1[1], a2[1], a3[1]], color=RED, lw=1.0)

ax.annotate(r"$d=\dfrac{|Ax_0+By_0+C|}{\sqrt{A^2+B^2}}$", xy=(1.85, 3.02),
            xytext=(-1.05, 0.62), fontsize=12.5, color=INK,
            arrowprops=dict(arrowstyle="->", color=GREY, lw=1.0))
ax.annotate("$Ax+By+C=0$", xy=(3.55, (A * 3.55 + C) / (-B)),
            xytext=(3.45, 1.35), fontsize=11.5, color=BLUE,
            arrowprops=dict(arrowstyle="->", color=BLUE, lw=1.0))
ax.set_title("点到直线的距离：沿垂线量", fontsize=12.5, color=INK)
ax.set_xlabel("$x$", fontsize=11, color=INK)
ax.set_ylabel("$y$", fontsize=11, color=INK)
axes_cross(ax, (-1.4, 5.0), (-1.1, 5.4))
style(ax)
fig.tight_layout()
fig.savefig(BASE + "geo-point-line-dist.png", dpi=150)
plt.close(fig)


# ============================================================
# 图3 圆：位置关系、切线、弦
# ============================================================
fig, axes = plt.subplots(1, 3, figsize=(13.0, 4.6), dpi=150)
th = np.linspace(0, 2 * np.pi, 400)
r = 1.0

# (1) 点与圆
ax = axes[0]
ax.plot(r * np.cos(th), r * np.sin(th), color=BLUE, lw=2.2)
ax.plot([0], [0], "o", color=INK, ms=4)
pts = [(0.45, 0.30, GREEN, "$d<r$ 在圆内", (0.62, -1.35)),
       (-0.60, 0.80, ORANGE, "$d=r$ 在圆上", (-1.72, 1.05)),
       (1.45, 0.95, RED, "$d>r$ 在圆外", (0.72, 1.52))]
for px, py, col, lab, (tx, ty) in pts:
    ax.plot([0, px], [0, py], color=col, lw=1.0, ls="--")
    ax.plot([px], [py], "o", color=col, ms=7, zorder=5)
    ax.annotate(lab, xy=(px, py), xytext=(tx, ty), fontsize=10, color=col,
                arrowprops=dict(arrowstyle="->", color=col, lw=0.9))
ax.set_title("点与圆：比 $d$ 与 $r$", fontsize=11.5, color=INK, pad=10)
ax.set_aspect("equal"); ax.set_xlim(-1.95, 1.95); ax.set_ylim(-1.6, 2.0)

# (2) 直线与圆
ax = axes[1]
ax.plot(r * np.cos(th), r * np.sin(th), color=BLUE, lw=2.2)
y1 = -0.35
dx = np.sqrt(max(r ** 2 - y1 ** 2, 0))
ax.plot([-1.6, 1.6], [y1, y1], color=RED, lw=1.6)
ax.plot([-dx, dx], [y1, y1], "o", color=RED, ms=6)
ax.plot([0, 0], [0, y1], color=GREY, lw=1.0, ls=":")
ax.text(0.07, y1 / 2 - 0.12, "$d$", fontsize=10, color=GREY)
ax.text(-1.60, y1 - 0.52, "相交：$d<r$，两个交点", fontsize=10, color=RED)
ax.plot([-1.3, 1.3], [1.0, 1.0], color=GREEN, lw=1.6)
ax.plot([0], [1.0], "o", color=GREEN, ms=6)
ax.text(-1.28, 1.10, "相切：$d=r$，一个交点", fontsize=10, color=GREEN)
ax.plot([-1.45, 1.45], [-1.5, -1.5], color=ORANGE, lw=1.6)
ax.text(-1.42, -1.78, "相离：$d>r$，无交点", fontsize=10, color=ORANGE)
ax.set_title("直线与圆：三种位置关系", fontsize=11.5, color=INK, pad=10)
ax.set_aspect("equal"); ax.set_xlim(-1.95, 1.95); ax.set_ylim(-2.0, 1.8)

# (3) 切线长与切点弦
ax = axes[2]
ax.plot(r * np.cos(th), r * np.sin(th), color=BLUE, lw=2.2)
P2 = np.array([1.95, 0.85])
dP = np.hypot(*P2)
al = np.arccos(r / dP)
base = np.arctan2(P2[1], P2[0])
T1 = r * np.array([np.cos(base + al), np.sin(base + al)])
T2 = r * np.array([np.cos(base - al), np.sin(base - al)])
for T in (T1, T2):
    ax.plot([P2[0], T[0]], [P2[1], T[1]], color=RED, lw=1.6)
    ax.plot([0, T[0]], [0, T[1]], color=GREY, lw=1.0, ls="--")
    ax.plot(*T, "o", color=RED, ms=6, zorder=6)
ax.plot([T1[0], T2[0]], [T1[1], T2[1]], color=GREEN, lw=1.5)
ax.plot([0, P2[0]], [0, P2[1]], color=GREY, lw=1.0, ls=":")
ax.plot(*P2, "o", color=ORANGE, ms=7, zorder=6)
ax.text(T1[0] + 0.04, T1[1] + 0.09, "$T_1$", fontsize=10.5, color=RED)
ax.text(T2[0] - 0.16, T2[1] - 0.24, "$T_2$", fontsize=10.5, color=RED)
ax.text(P2[0] - 0.06, P2[1] + 0.12, "$P$", fontsize=11, color=ORANGE)
ax.text(-1.92, 1.55, "$|PT_1|=|PT_2|=\\sqrt{|PO|^2-r^2}$", fontsize=10.5, color=RED)
ax.text(-1.92, -1.75, "绿色：过两切点的弦 $T_1T_2$", fontsize=10.5, color=GREEN)
ax.set_title("切线长与切点弦", fontsize=11.5, color=INK, pad=10)
ax.set_aspect("equal"); ax.set_xlim(-2.0, 2.6); ax.set_ylim(-2.0, 1.8)

for a in axes:
    a.set_xlabel("$x$", fontsize=10, color=INK)
    a.set_ylabel("$y$", fontsize=10, color=INK)
    style(a)
fig.tight_layout()
fig.savefig(BASE + "geo-circle.png", dpi=150)
plt.close(fig)


# ============================================================
# 图4 椭圆的几何要素
# ============================================================
fig, ax = plt.subplots(figsize=(7.8, 5.6), dpi=150)
a, b = 3.0, 2.0
c = np.sqrt(a ** 2 - b ** 2)
t = np.linspace(0, 2 * np.pi, 500)
ax.plot(a * np.cos(t), b * np.sin(t), color=BLUE, lw=2.4)
ax.plot([-c, c], [0, 0], "o", color=RED, ms=8, zorder=6)
ax.plot([-a, a], [0, 0], "o", color=GREEN, ms=6, zorder=6)
ax.text(c + 0.05, 0.16, "$F_2(c,0)$", fontsize=10.5, color=RED)
ax.text(-c - 0.95, 0.16, "$F_1(-c,0)$", fontsize=10.5, color=RED)
ax.text(a - 0.85, -0.42, "$A_2(a,0)$", fontsize=10, color=GREEN)
ax.text(-a + 0.05, -0.42, "$A_1(-a,0)$", fontsize=10, color=GREEN)
# a, b, c 三角形
ax.plot([c, 0], [0, b], color=ORANGE, lw=1.6)
ax.plot([0, 0], [0, b], color=ORANGE, lw=1.6, ls="--")
ax.text(c / 2, -0.32, "$c$", fontsize=11, color=ORANGE)
ax.text(-0.28, b / 2, "$b$", fontsize=11, color=ORANGE)
ax.text(c / 2 + 0.12, b / 2 + 0.10, "$a$", fontsize=11, color=ORANGE)
ax.annotate("$a^2=b^2+c^2$", xy=(1.45, 1.30), xytext=(1.55, -1.35), fontsize=12, color=ORANGE,
            arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.0))
# 准线
for s in (-1, 1):
    ax.plot([s * a ** 2 / c] * 2, [-2.35, 2.35], color=GREY, lw=1.2, ls="--")
ax.text(a ** 2 / c, -2.55, r"$x=\dfrac{a^2}{c}$", fontsize=11, color=GREY, ha="center")
ax.text(-a ** 2 / c, -2.55, r"$x=-\dfrac{a^2}{c}$", fontsize=11, color=GREY, ha="center")
# 焦半径和
Pf = (a * np.cos(np.deg2rad(55)), b * np.sin(np.deg2rad(55)))
ax.plot([-c, Pf[0]], [0, Pf[1]], color=RED, lw=1.2)
ax.plot([c, Pf[0]], [0, Pf[1]], color=RED, lw=1.2)
ax.plot(*Pf, "o", color=INK, ms=5)
ax.text(Pf[0] + 0.13, Pf[1] - 0.10, "$P$", fontsize=11, color=INK)
ax.text(-2.55, 1.35, "$|PF_1|+|PF_2|=2a$", fontsize=11.5, color=RED)
ax.set_title("椭圆：$\\dfrac{x^2}{a^2}+\\dfrac{y^2}{b^2}=1$，离心率 $e=\\dfrac{c}{a}<1$",
             fontsize=12.5, color=INK)
ax.set_xlabel("$x$", fontsize=11, color=INK)
ax.set_ylabel("$y$", fontsize=11, color=INK)
axes_cross(ax, (-5.0, 5.0), (-2.9, 2.6))
style(ax)
fig.tight_layout()
fig.savefig(BASE + "geo-ellipse.png", dpi=150)
plt.close(fig)


# ============================================================
# 图5 双曲线的几何要素
# ============================================================
fig, ax = plt.subplots(figsize=(7.8, 5.4), dpi=150)
a, b = 2.0, 1.5
c = np.sqrt(a ** 2 + b ** 2)
xs = np.linspace(a, 3.5, 400)
for sgn in (1, -1):
    ax.plot(sgn * xs, b * np.sqrt(xs ** 2 / a ** 2 - 1), color=BLUE, lw=2.4)
    ax.plot(sgn * xs, -b * np.sqrt(xs ** 2 / a ** 2 - 1), color=BLUE, lw=2.4)
asym = np.linspace(-3.5, 3.5, 10)
ax.plot(asym, b / a * asym, color=GREY, lw=1.2, ls="--")
ax.plot(asym, -b / a * asym, color=GREY, lw=1.2, ls="--")
ax.annotate(r"$y=\dfrac{b}{a}x$", xy=(2.55, b / a * 2.55), xytext=(2.75, 2.90),
            fontsize=10.5, color=GREY,
            arrowprops=dict(arrowstyle="->", color=GREY, lw=0.9))
ax.annotate(r"$y=-\dfrac{b}{a}x$", xy=(-2.45, b / a * 2.45), xytext=(-3.65, 2.72),
            fontsize=10.5, color=GREY,
            arrowprops=dict(arrowstyle="->", color=GREY, lw=0.9))
ax.plot([-c, c], [0, 0], "o", color=RED, ms=8, zorder=6)
ax.plot([-a, a], [0, 0], "o", color=GREEN, ms=6, zorder=6)
ax.text(c + 0.10, 0.16, "$F_2(c,0)$", fontsize=10.5, color=RED)
ax.text(-c - 1.35, 0.16, "$F_1(-c,0)$", fontsize=10.5, color=RED)
ax.text(a + 0.10, -0.45, "$A_2(a,0)$", fontsize=10, color=GREEN)
ax.text(-a - 0.35, -0.45, "$A_1(-a,0)$", fontsize=10, color=GREEN)
# 直角三角形 (0,0)-(a,0)-(a,b)，斜边落在渐近线上，长 c
ax.plot([0, a], [0, 0], color=ORANGE, lw=1.5)
ax.plot([a, a], [0, b], color=ORANGE, lw=1.5)
ax.plot([0, a], [0, b], color=ORANGE, lw=1.5)
ax.text(a / 2, -0.30, "$a$", fontsize=11, color=ORANGE)
ax.text(a + 0.10, b / 2, "$b$", fontsize=11, color=ORANGE)
ax.text(a / 2 - 0.30, b / 2 + 0.16, "$c$", fontsize=11, color=ORANGE)
ax.annotate("$c^2=a^2+b^2$", xy=(1.92, 0.42), xytext=(0.20, -2.55), fontsize=12,
            color=ORANGE, arrowprops=dict(arrowstyle="->", color=ORANGE, lw=1.0))
ax.set_title("双曲线：$\\dfrac{x^2}{a^2}-\\dfrac{y^2}{b^2}=1$，离心率 $e=\\dfrac{c}{a}>1$",
             fontsize=12.5, color=INK)
ax.set_xlabel("$x$", fontsize=11, color=INK)
ax.set_ylabel("$y$", fontsize=11, color=INK)
axes_cross(ax, (-4.2, 4.2), (-3.0, 3.0))
style(ax)
fig.tight_layout()
fig.savefig(BASE + "geo-hyperbola.png", dpi=150)
plt.close(fig)


# ============================================================
# 图6 抛物线的焦点与准线
# ============================================================
fig, ax = plt.subplots(figsize=(7.8, 5.4), dpi=150)
p = 1.6
y = np.linspace(-3.2, 3.2, 500)
ax.plot(y ** 2 / (2 * p), y, color=BLUE, lw=2.4)
ax.plot([p / 2], [0], "o", color=RED, ms=8, zorder=6)
ax.text(p / 2 + 0.22, 0.30, r"$F\left(\dfrac{p}{2},0\right)$", fontsize=11, color=RED)
ax.axvline(-p / 2, color=GREY, lw=1.3, ls="--")
ax.text(-p / 2 - 0.05, 2.75, r"$x=-\dfrac{p}{2}$", fontsize=11, color=GREY, ha="right")
# 点 P、到焦点与到准线的两段
Py = 2.0
Px = Py ** 2 / (2 * p)
ax.plot(*[Px], *[Py], "o", color=INK, ms=6)
ax.plot([Px, p / 2], [Py, 0], color=GREEN, lw=1.5)
ax.plot([Px, -p / 2], [Py, Py], color=GREEN, lw=1.5)
ax.text(Px + 0.10, Py + 0.10, "$P$", fontsize=11, color=INK)
ax.annotate("两段一样长", xy=(Px / 2 + 0.02, Py / 2 + 0.02), xytext=(2.55, 2.75),
            fontsize=11, color=GREEN, arrowprops=dict(arrowstyle="->", color=GREEN, lw=1.0))
# 通径
ax.plot([p / 2, p / 2], [-p, p], color=ORANGE, lw=1.6)
ax.annotate("通径长 $=2p$", xy=(p / 2 - 0.02, -1.15), xytext=(1.10, -2.72),
            fontsize=10.5, color=ORANGE, arrowprops=dict(arrowstyle="->", color=ORANGE, lw=0.9))
ax.set_title("抛物线：$y^2=2px$，离心率 $e=1$", fontsize=12.5, color=INK)
ax.set_xlabel("$x$", fontsize=11, color=INK)
ax.set_ylabel("$y$", fontsize=11, color=INK)
axes_cross(ax, (-1.9, 5.6), (-3.4, 3.4))
style(ax)
fig.tight_layout()
fig.savefig(BASE + "geo-parabola.png", dpi=150)
plt.close(fig)

print("2D done")


# ============================================================
# 图7 用平面截双圆锥：椭圆、抛物线、双曲线
# ============================================================
fig = plt.figure(figsize=(13.4, 4.9), dpi=150)


def wire_cone(ax, H=2.2):
    th = np.linspace(0, 2 * np.pi, 200)
    for z, r in ((H, H), (-H, H)):
        ax.plot(r * np.cos(th), r * np.sin(th), z, color=BLUE, lw=1.1, alpha=0.85)
    for a in np.linspace(0, 2 * np.pi, 16, endpoint=False):
        ax.plot([0, H * np.cos(a)], [0, H * np.sin(a)], [0, H], color=BLUE, lw=0.8, alpha=0.6)
        ax.plot([0, H * np.cos(a)], [0, H * np.sin(a)], [0, -H], color=BLUE, lw=0.8, alpha=0.6)
    ax.plot([0, 0], [0, 0], [-H, H], color=GREY, lw=1.0, ls="--")


def section(ax, m, c, vrange, H=2.4):
    e1 = np.array([1, 0, m]) / np.hypot(1, m)
    e2 = np.array([0, 1, 0])
    P0 = np.array([0, 0, c])
    corners = [(-2.6, vrange[0]), (2.6, vrange[0]), (2.6, vrange[1]),
               (-2.6, vrange[1]), (-2.6, vrange[0])]
    for k in range(len(corners) - 1):
        u0, v0 = corners[k]; u1, v1 = corners[k + 1]
        ax.plot([P0[0] + u0 * e1[0], P0[0] + u1 * e1[0]],
                [P0[1] + u0 * e1[1], P0[1] + u1 * e1[1]],
                [P0[2] + u0 * e1[2], P0[2] + u1 * e1[2]], color=BLUE, lw=1.0, alpha=0.5)

    vs = np.linspace(vrange[0], vrange[1], 600)
    if abs(m - 1) < 1e-9:
        u = (vs ** 2 - c ** 2) / (np.sqrt(2) * c)
        pairs = [(u, vs)]
    else:
        A = (1 - m ** 2) / (1 + m ** 2)
        B = -2 * c * m / np.hypot(1, m)
        disc = B ** 2 - 4 * A * (vs ** 2 - c ** 2)
        ok = disc >= 0
        vs, disc = vs[ok], disc[ok]
        up = (-B + np.sqrt(disc)) / (2 * A)
        um = (-B - np.sqrt(disc)) / (2 * A)
        if A > 0:
            pairs = [(np.concatenate([up, um[::-1], up[:1]]),
                      np.concatenate([vs, vs[::-1], vs[:1]]))]
        else:
            pairs = [(up, vs), (um, vs)]
    for u, v in pairs:
        X = P0[0] + u * e1[0] + v * e2[0]
        Y = P0[1] + u * e1[1] + v * e2[1]
        Z = P0[2] + u * e1[2] + v * e2[2]
        ax.plot(X, Y, Z, color=RED, lw=2.8, zorder=10)


for k, (m, c, vr, title) in enumerate([
        (0.42, 1.0, (-1.55, 1.55), "截面比母线平：椭圆"),
        (1.0, 0.75, (-1.9, 1.9), "截面平行于母线：抛物线"),
        (1.85, 0.55, (-2.2, 2.2), "截面比母线陡：双曲线")]):
    ax = fig.add_subplot(1, 3, k + 1, projection="3d")
    wire_cone(ax)
    section(ax, m, c, vr)
    ax.set_title(title, fontsize=11, color=INK, pad=0)
    ax.set_box_aspect((1, 1, 1.25))
    ax.set_xlim(-3.0, 3.0); ax.set_ylim(-3.0, 3.0); ax.set_zlim(-3.0, 3.0)
    n = np.array([-m, 0.0, 1.0]); n = n / np.linalg.norm(n)
    ax.view_init(elev=np.degrees(np.arcsin(n[2])), azim=np.degrees(np.arctan2(n[1], n[0])))
    ax.set_axis_off()

fig.suptitle("圆锥曲线：用一个平面去截双圆锥", fontsize=13, color=INK, y=0.99)
fig.tight_layout(rect=(0, 0, 1, 0.94))
fig.savefig(BASE + "geo-conic-sections.png", dpi=150)
plt.close(fig)


# ============================================================
# 图8 统一定义：到焦点距离与到准线距离之比等于 e
# ============================================================
fig, axes = plt.subplots(1, 3, figsize=(13.0, 4.6), dpi=150)
d = 1.6
for ax, (e, ang_deg, title) in zip(axes, [(0.55, 52, "$e<1$：椭圆"),
                                          (1.0, 78, "$e=1$：抛物线"),
                                          (1.65, 102, "$e>1$：双曲线")]):
    th = np.linspace(-3.10, 3.10, 1400)
    r = e * d / (1 - e * np.cos(th))
    ok = r > 0
    ax.plot(r[ok] * np.cos(th[ok]), r[ok] * np.sin(th[ok]), color=BLUE, lw=2.3)
    ax.axvline(-d, color=GREY, lw=1.2, ls="--")
    ax.plot([0], [0], "o", color=RED, ms=8, zorder=6)
    ax.text(0.06, -0.28, "$F$", fontsize=11, color=RED)
    ax.text(-d + 0.10, 2.50, "准线", fontsize=10.5, color=GREY, ha="left")
    # 取一个点，画两条距离
    ang = np.deg2rad(ang_deg)
    rr = e * d / (1 - e * np.cos(ang))
    Px, Py = rr * np.cos(ang), rr * np.sin(ang)
    ax.plot([0, Px], [0, Py], color=GREEN, lw=1.4)
    ax.plot([Px, -d], [Py, Py], color=ORANGE, lw=1.4)
    ax.plot([Px], [Py], "o", color=INK, ms=5)
    ax.text(Px + 0.12, Py + 0.10, "$P$", fontsize=10.5, color=INK)
    ax.text(Px / 2 + 0.10, Py / 2 + 0.10, "$|PF|$", fontsize=10, color=GREEN)
    ax.text((-d + Px) / 2, Py + 0.12, "$d$", fontsize=10.5, color=ORANGE)
    ax.set_title(title, fontsize=11.5, color=INK, pad=8)
    ax.text(0.02, 0.02, "$|PF|=e\\,d$", transform=ax.transAxes, fontsize=11.5, color=INK,
            va="bottom")
    ax.set_aspect("equal")
    ax.set_xlim(-2.3, 4.4); ax.set_ylim(-2.9, 2.9)
    ax.set_xlabel("$x$", fontsize=10, color=INK)
    ax.set_ylabel("$y$", fontsize=10, color=INK)
    style(ax)
fig.suptitle("统一定义：到定点的距离与到定直线的距离之比恒为 $e$", fontsize=12.5, color=INK)
fig.tight_layout()
fig.savefig(BASE + "geo-conic-unified.png", dpi=150)
plt.close(fig)

print("conic done")


# ============================================================
# 图9 空间平面、法向量与点到平面距离
# ============================================================
fig = plt.figure(figsize=(7.6, 6.4), dpi=150)
ax = fig.add_subplot(111, projection="3d")
A, B, C, D = 0.18, 0.30, -1.0, 1.5
gx, gy = np.meshgrid(np.linspace(-0.4, 3.0, 2), np.linspace(-0.4, 3.0, 2))
gz = (-D - A * gx - B * gy) / C
ax.plot_surface(gx, gy, gz, color=CREAM, alpha=0.55, linewidth=0, shade=False)
n = np.array([A, B, C]); n = n / np.linalg.norm(n)
M0 = np.array([0.9, 0.7, (-D - A * 0.9 - B * 0.7) / C])
ax.quiver(M0[0], M0[1], M0[2], n[0], n[1], n[2], length=1.3, color=RED, lw=2.2,
          arrow_length_ratio=0.2)
ax.text(M0[0] + 1.35 * n[0] + 0.05, M0[1] + 1.35 * n[1], M0[2] + 1.35 * n[2],
        r"$\vec{n}=(A,B,C)$", fontsize=10.5, color=RED)
ax.scatter(*M0, color=RED, s=28, depthshade=False)
ax.text(M0[0] - 0.42, M0[1] - 0.30, M0[2] + 0.05, "$M_0$", fontsize=10, color=RED)

Pp = np.array([2.35, 2.30, 3.65])
tt = -(A * Pp[0] + B * Pp[1] + C * Pp[2] + D) / (A * A + B * B + C * C)
Q = Pp + tt * np.array([A, B, C])
ax.plot([Pp[0], Q[0]], [Pp[1], Q[1]], [Pp[2], Q[2]], color=GREEN, lw=2.6)
ax.scatter(*Pp, color=ORANGE, s=50, depthshade=False)
ax.scatter(*Q, color=GREEN, s=40, depthshade=False)
ax.text(Pp[0] + 0.12, Pp[1] + 0.10, Pp[2] + 0.14, "$P$", fontsize=11, color=ORANGE)
ax.text(Q[0] - 0.95, Q[1] + 0.10, Q[2] + 0.10, "垂足 $Q$", fontsize=9.5, color=GREEN)
ax.text((Pp[0] + Q[0]) / 2 + 0.24, (Pp[1] + Q[1]) / 2 + 0.10, (Pp[2] + Q[2]) / 2 + 0.06,
        "$d$", fontsize=12, color=GREEN)
ax.set_xlabel("$x$", fontsize=10); ax.set_ylabel("$y$", fontsize=10); ax.set_zlabel("$z$", fontsize=10)
ax.set_xlim(-0.5, 3.2); ax.set_ylim(-0.5, 3.2); ax.set_zlim(-0.4, 4.4)
ax.view_init(elev=20, azim=-66)
ax.set_title("平面、法向量与点到平面的距离", fontsize=12, color=INK, pad=0)
for pane in (ax.xaxis, ax.yaxis, ax.zaxis):
    pane.pane.set_facecolor("white"); pane.pane.set_edgecolor("#dddddd")
fig.text(0.5, 0.035, r"$Ax+By+Cz+D=0$，$d=\dfrac{|Ax_0+By_0+Cz_0+D|}{\sqrt{A^2+B^2+C^2}}$",
         ha="center", fontsize=12, color=BLUE)
fig.tight_layout(rect=(0, 0.07, 1, 1))
fig.savefig(BASE + "geo-plane-3d.png", dpi=150)
plt.close(fig)


# ============================================================
# 图10 空间直线：方向向量、与平面的夹角
# ============================================================
fig = plt.figure(figsize=(7.6, 6.0), dpi=150)
ax = fig.add_subplot(111, projection="3d")
# 平面 z = 0.35x + 1.2
gx, gy = np.meshgrid(np.linspace(-2.0, 2.4, 2), np.linspace(-2.0, 2.4, 2))
ax.plot_surface(gx, gy, 0.35 * gx + 1.2, color=CREAM, alpha=0.7, linewidth=0, shade=False)
# 空间直线
s = np.array([1.2, 0.8, 1.0])
L0 = np.array([-1.2, -0.6, 0.2])
ts = np.linspace(-0.6, 1.6, 10)
ax.plot(L0[0] + ts * s[0], L0[1] + ts * s[1], L0[2] + ts * s[2], color=RED, lw=2.4)
ax.text(L0[0] + 1.6 * s[0], L0[1] + 1.6 * s[1], L0[2] + 1.6 * s[2],
        r"$\vec{s}=(m,n,p)$", fontsize=10.5, color=RED)
ax.scatter(*L0, color=ORANGE, s=40, depthshade=False)
ax.text(L0[0] - 0.35, L0[1] - 0.35, L0[2] + 0.1, "$M_0$", fontsize=10.5, color=ORANGE)
# 直线在平面上的投影
tt = -(0.35 * L0[0] - L0[1] * 0 + 1.2 - L0[2]) / (0.35 * s[0] - s[2])
proj = []
for t in [tt - 0.6, tt + 1.6]:
    Qp = L0 + t * s
    Qp = np.array([Qp[0], Qp[1], 0.35 * Qp[0] + 1.2])
    proj.append(Qp)
ax.plot([proj[0][0], proj[1][0]], [proj[0][1], proj[1][1]], [proj[0][2], proj[1][2]],
        color=GREEN, lw=2.0, ls="--")
ax.text(proj[1][0] + 0.1, proj[1][1] + 0.1, proj[1][2], "投影", fontsize=9.5, color=GREEN)
ax.set_xlabel("$x$", fontsize=10); ax.set_ylabel("$y$", fontsize=10); ax.set_zlabel("$z$", fontsize=10)
ax.set_xlim(-2.0, 2.4); ax.set_ylim(-2.0, 2.4); ax.set_zlim(-1.0, 3.2)
ax.view_init(elev=18, azim=-62)
ax.set_title("空间直线：点向式与它在平面上的投影", fontsize=12, color=INK, pad=0)
for pane in (ax.xaxis, ax.yaxis, ax.zaxis):
    pane.pane.set_facecolor("white"); pane.pane.set_edgecolor("#dddddd")
fig.tight_layout()
fig.savefig(BASE + "geo-line-3d.png", dpi=150)
plt.close(fig)


# ============================================================
# 图11 常见二次曲面
# ============================================================
fig = plt.figure(figsize=(12.6, 8.2), dpi=150)
u = np.linspace(0, 2 * np.pi, 60)
v = np.linspace(0, np.pi, 40)
U, V = np.meshgrid(u, v)


def show(ax, X, Y, Z, title, elev=18, azim=-58, lim=None):
    ax.plot_surface(X, Y, Z, color=CREAM, alpha=0.9, linewidth=0.3,
                    edgecolor="#cbb193", shade=True, rstride=2, cstride=2)
    ax.set_title(title, fontsize=10.5, color=INK, pad=-2)
    ax.view_init(elev=elev, azim=azim)
    ax.set_box_aspect((1, 1, 0.85))
    if lim is not None:
        ax.set_xlim(-lim, lim); ax.set_ylim(-lim, lim); ax.set_zlim(-lim, lim)
    ax.set_xticks([]); ax.set_yticks([]); ax.set_zticks([])
    for pane in (ax.xaxis, ax.yaxis, ax.zaxis):
        pane.pane.set_facecolor("white"); pane.pane.set_edgecolor("#eeeeee")


# 椭球面
ax = fig.add_subplot(2, 3, 1, projection="3d")
show(ax, 1.4 * np.sin(V) * np.cos(U), 1.0 * np.sin(V) * np.sin(U), 0.8 * np.cos(V),
     "椭球面 $\\dfrac{x^2}{a^2}+\\dfrac{y^2}{b^2}+\\dfrac{z^2}{c^2}=1$", lim=1.55)

# 单叶双曲面
ax = fig.add_subplot(2, 3, 2, projection="3d")
vv = np.linspace(-1.4, 1.4, 40)
U2, V2 = np.meshgrid(u, vv)
show(ax, np.cosh(V2) * np.cos(U2), np.cosh(V2) * np.sin(U2) * 0.75, np.sinh(V2),
     "单叶双曲面 $\\dfrac{x^2}{a^2}+\\dfrac{y^2}{b^2}-\\dfrac{z^2}{c^2}=1$")

# 双叶双曲面
ax = fig.add_subplot(2, 3, 3, projection="3d")
vv = np.linspace(0.25, 1.5, 30)
U2, V2 = np.meshgrid(u, vv)
for sgn in (1, -1):
    show(ax, np.sinh(V2) * np.cos(U2), 0.8 * np.sinh(V2) * np.sin(U2), sgn * np.cosh(V2), "")
ax.set_title("双叶双曲面 $\\dfrac{x^2}{a^2}+\\dfrac{y^2}{b^2}-\\dfrac{z^2}{c^2}=-1$",
             fontsize=10.5, color=INK, pad=-2)

# 椭圆抛物面
ax = fig.add_subplot(2, 3, 4, projection="3d")
rr = np.linspace(0, np.sqrt(2.4), 30)
RR, UU = np.meshgrid(rr, u)
show(ax, RR * np.cos(UU), 0.85 * RR * np.sin(UU), RR ** 2,
     "椭圆抛物面 $z=\\dfrac{x^2}{a^2}+\\dfrac{y^2}{b^2}$")

# 双曲抛物面
ax = fig.add_subplot(2, 3, 5, projection="3d")
gx, gy = np.meshgrid(np.linspace(-1.5, 1.5, 30), np.linspace(-1.5, 1.5, 30))
show(ax, gx, gy, gx ** 2 - gy ** 2, "双曲抛物面（马鞍面）$z=\\dfrac{x^2}{a^2}-\\dfrac{y^2}{b^2}$")

# 圆锥面
ax = fig.add_subplot(2, 3, 6, projection="3d")
vv = np.linspace(-1.3, 1.3, 30)
U2, V2 = np.meshgrid(u, vv)
show(ax, V2 * np.cos(U2), V2 * np.sin(U2) * 0.85, V2,
     "圆锥面 $z^2=a^2(x^2+y^2)$")

fig.suptitle("常见二次曲面", fontsize=13.5, color=INK)
fig.tight_layout()
fig.savefig(BASE + "geo-quadrics.png", dpi=150)
plt.close(fig)


# ============================================================
# 图12 球面、柱面、旋转曲面
# ============================================================
fig = plt.figure(figsize=(12.6, 4.6), dpi=150)

ax = fig.add_subplot(1, 3, 1, projection="3d")
show(ax, 1.2 * np.sin(V) * np.cos(U), 1.2 * np.sin(V) * np.sin(U), 1.2 * np.cos(V),
     "球面 $x^2+y^2+z^2=R^2$", elev=16, azim=-60)

ax = fig.add_subplot(1, 3, 2, projection="3d")
zz = np.linspace(-1.4, 1.4, 30)
U3, Z3 = np.meshgrid(u, zz)
show(ax, np.cos(U3), np.sin(U3), Z3,
     "圆柱面 $x^2+y^2=R^2$（缺 $z$）", elev=16, azim=-60)

ax = fig.add_subplot(1, 3, 3, projection="3d")
tt = np.linspace(0.0, 1.55, 34)
RR4, U4 = np.meshgrid(np.sqrt(tt), u)
TT, _ = np.meshgrid(tt, u)
show(ax, RR4 * np.cos(U4), RR4 * np.sin(U4), TT,
     "旋转抛物面：$yOz$ 面上的 $z=y^2$ 绕 $z$ 轴旋转", elev=16, azim=-60)

fig.tight_layout()
fig.savefig(BASE + "geo-sphere-cylinder.png", dpi=150)
plt.close(fig)

print("3D done")
