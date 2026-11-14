import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.family"] = ["PingFang SC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

INK, ORANGE, BLUE = "#2b2b2b", "#d2691e", "#2f4f6f"
RED, GREEN, GREY = "#b03a2e", "#4a7c59", "#8a8a8a"
BASE = "/Users/fred/Documents/GitHub/cycleuser/blog/output/img/kaoyan-math/"
F = 11.5

def frame(ax, xlim, ylim, title, grid=False):
    ax.axhline(0, color="#dcdcdc", lw=0.9)
    ax.axvline(0, color="#dcdcdc", lw=0.9)
    ax.set_xlim(*xlim); ax.set_ylim(*ylim)
    ax.set_aspect("equal"); ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_color("#cccccc")
    ax.set_title(title, fontsize=12, color=INK, pad=8)

# ============ 内摆线 ============
def hypocycloid(R, r, t):
    k = R / r
    return ((R - r) * np.cos(t) + r * np.cos((k - 1) * t),
            (R - r) * np.sin(t) - r * np.sin((k - 1) * t))

fig, axes = plt.subplots(1, 3, figsize=(12.6, 4.6), dpi=150)
cases = [(3, "R=3r", "三尖点（三角摆线）"), (4, "R=4r", "四尖点 = 星形线"), (5, "R=5r", "五尖点")]
for ax, (k, lab, name) in zip(axes, cases):
    t = np.linspace(0, 2 * np.pi, 2000)
    x, y = hypocycloid(k, 1.0, t)
    frame(ax, (-5.6, 5.6), (-5.6, 5.6), f"{lab}：{name}")
    th = np.linspace(0, 2 * np.pi, 300)
    ax.plot(k * np.cos(th), k * np.sin(th), color="#e2d9cb", lw=1.4, ls="--", zorder=2)
    ax.plot(x, y, color=BLUE, lw=2.4, zorder=3)
    for j in range(k):
        ang = 2 * np.pi * j / k
        cx, cy = k * np.cos(ang), k * np.sin(ang)
        ax.plot([cx], [cy], "o", color=RED, ms=4, zorder=4)

fig.subplots_adjust(left=0.01, right=0.99, top=0.89, bottom=0.02, wspace=0.03)
fig.savefig(BASE + "param-hypocycloid.png", dpi=150); plt.close(fig)

# ============ 特殊双曲线 ============
fig, axes = plt.subplots(1, 2, figsize=(11.6, 5.0), dpi=150)

ax = axes[0]
frame(ax, (-4.4, 4.4), (-4.0, 4.0), "等轴双曲线：$a=b$，$e=\\sqrt{2}$，渐近线互相垂直")
a = 1.8
s = np.linspace(-2.0, 2.0, 400)
ax.plot(a * np.cosh(s), a * np.sinh(s), color=BLUE, lw=2.4, zorder=3)
ax.plot(-a * np.cosh(s), a * np.sinh(s), color=BLUE, lw=2.4, zorder=3)
xx = np.linspace(-4.3, 4.3, 10)
ax.plot(xx, xx, color=GREY, lw=1.2, ls="--", zorder=2)
ax.plot(xx, -xx, color=GREY, lw=1.2, ls="--", zorder=2)
ax.plot([a], [0], "o", color=RED, ms=6, zorder=5)
ax.plot([-a], [0], "o", color=RED, ms=6, zorder=5)
ax.text(a + 0.10, 0.16, "$A_2$", fontsize=F - 1, color=RED)
ax.text(-a - 0.40, 0.16, "$A_1$", fontsize=F - 1, color=RED)
ax.text(2.55, 1.10, "$y=x$", fontsize=F - 2, color=GREY)
ax.text(2.55, -1.35, "$y=-x$", fontsize=F - 2, color=GREY)


ax = axes[1]
frame(ax, (-4.4, 4.4), (-4.0, 4.0), "共轭双曲线：共用渐近线与焦点圆 $x^{2}+y^{2}=a^{2}+b^{2}$")
a, b = 1.6, 1.15
ax.plot(a * np.cosh(s), b * np.sinh(s), color=BLUE, lw=2.4, zorder=4)
ax.plot(-a * np.cosh(s), b * np.sinh(s), color=BLUE, lw=2.4, zorder=4)
ax.plot(b * np.sinh(s), a * np.cosh(s), color=ORANGE, lw=2.4, zorder=4)
ax.plot(b * np.sinh(s), -a * np.cosh(s), color=ORANGE, lw=2.4, zorder=4)
for sgn in (1, -1):
    ax.plot(xx, sgn * (b / a) * xx, color=GREY, lw=1.2, ls="--", zorder=2)
c = np.hypot(a, b)
th_c = np.linspace(0, 2 * np.pi, 400)
ax.plot(c * np.cos(th_c), c * np.sin(th_c), color="#b8a88f", lw=1.2, ls=":", zorder=2)
ax.plot([a, -a], [0, 0], "o", color=BLUE, ms=6, zorder=6)
ax.plot([0, 0], [a, -a], "o", color=ORANGE, ms=6, zorder=6)
for sx in (1, -1):
    for sy in (1, -1):
        ax.plot([sx * c], [sy * c / c * 0], "o", color=GREY, ms=0, zorder=1)
ax.plot([c, -c, 0, 0], [0, 0, c, -c], "o", color=RED, ms=6, zorder=7, mfc="white", mew=1.4)
ax.text(c + 0.10, -0.34, "$F$", fontsize=F - 2, color=RED)
ax.text(-c - 0.42, -0.34, "$F'$", fontsize=F - 2, color=RED)
ax.text(0.16, c - 0.10, "$F$", fontsize=F - 2, color=RED)
ax.text(0.16, -c - 0.02, "$F'$", fontsize=F - 2, color=RED)
ax.text(2.45, 0.55, "$\\frac{x^{2}}{a^{2}}-\\frac{y^{2}}{b^{2}}=1$", fontsize=F - 2, color=BLUE)
ax.text(-0.05, 3.45, "$\\frac{y^{2}}{a^{2}}-\\frac{x^{2}}{b^{2}}=1$", fontsize=F - 2, color=ORANGE, ha="center")


fig.tight_layout(); fig.savefig(BASE + "geo7-hyperbola-special.png", dpi=150); plt.close(fig)
print("ok")
