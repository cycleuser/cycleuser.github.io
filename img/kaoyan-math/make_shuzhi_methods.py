"""数值方法动画：牛顿法、割线法、二分法、迭代法等。

每个动画统一风格：深蓝函数曲线、棕色切线/割线、绿色迭代点，
标题实时显示迭代步数与当前近似值。
"""

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from PIL import Image
import os

plt.rcParams["font.family"] = ["PingFang SC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

BASE = os.path.dirname(os.path.abspath(__file__)) + "/"
CURVE, TAN, POINT, INK, GREY = "#1f2d5a", "#7a5230", "#4a7c59", "#2b2b2b", "#9aa4ae"


def save_gif(frames, name, dur=600):
    pal = [f.convert("P", palette=Image.ADAPTIVE) for f in frames]
    pal[0].save(BASE + name, save_all=True, append_images=pal[1:], duration=dur,
                loop=0, optimize=True)
    print("ok", name, len(frames))


def grab(fig):
    fig.canvas.draw()
    img = Image.fromarray(np.asarray(fig.canvas.buffer_rgba())[:, :, :3])
    plt.close(fig)
    return img


def frame(f, a, b, title, dots, segs, extra=None, ylim=None, figsize=(6.4, 3.6)):
    fig, ax = plt.subplots(figsize=figsize, dpi=100)
    xs = np.linspace(a, b, 600)
    ys = f(xs)
    if ylim:
        keep = (ys > ylim[0]) & (ys < ylim[1])
        xs, ys = xs[keep], ys[keep]
    ax.plot(xs, ys, color=CURVE, lw=2.2, zorder=3)
    ax.axhline(0, color=GREY, lw=1.2)
    for (x0, y0, x1, y1) in segs:
        ax.plot([x0, x1], [y0, y1], color=TAN, lw=1.6, ls="--", zorder=2)
    for i, (px, py) in enumerate(dots):
        ax.plot([px], [py], "o", ms=7 if i == len(dots) - 1 else 5,
                color=POINT if i == len(dots) - 1 else INK, zorder=5)
    if extra:
        extra(ax)
    if ylim:
        ax.set_ylim(*ylim)
    ax.set_xlim(a, b)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_color("#d8dde3")
    ax.set_title(title, fontsize=12, color=INK, loc="left", pad=8)
    fig.tight_layout()
    return grab(fig)


# ---------------------------------------------------------------- 牛顿法
def newton_gif(name, f, df, x0, n=6, a=0.2, b=4.0, ylim=(-2.2, 3.2)):
    frames, segs, dots = [], [], []
    x = x0
    for k in range(n):
        y = f(x)
        dots.append((x, y))
        xn = x - y / df(x)
        segs.append((x, y, xn, 0.0))
        frames.append(frame(f, a, b, "第 %d 步：x = %.5f → %.5f" % (k, x, xn),
                            dots[:], segs[:], ylim=ylim))
        x = xn
    save_gif(frames, name, dur=700)


newton_gif("shuzhi-newton.gif", lambda t: t**3 - 2 * t - 5, lambda t: 3 * t**2 - 2,
           2.4, n=6, a=1.2, b=3.4, ylim=(-6, 12))


# ------------------------------------------------------- 阻尼牛顿法/简化牛顿法
def damped_newton_gif(name):
    f = lambda t: t**3 - 2 * t - 5
    df = lambda t: 3 * t**2 - 2
    x, frames, segs, dots = 2.4, [], [], []
    for k in range(7):
        y = f(x)
        dots.append((x, y))
        step = y / df(x)
        # 阻尼：步长乘以 0.6，避免冲过根
        xn = x - 0.6 * step
        segs.append((x, y, xn, 0.0))
        frames.append(frame(f, 1.2, 3.4, "第 %d 步：阻尼因子 0.6，x = %.5f" % (k, xn),
                            dots[:], segs[:], ylim=(-6, 12)))
        x = xn
    save_gif(frames, name)


def simplified_newton_gif(name):
    f = lambda t: t**3 - 2 * t - 5
    df0 = 3 * 2.4**2 - 2          # 导数固定在初值处，不再更新
    x, frames, segs, dots = 2.4, [], [], []
    for k in range(8):
        y = f(x)
        dots.append((x, y))
        xn = x - y / df0
        segs.append((x, y, xn, 0.0))
        frames.append(frame(f, 1.2, 3.4, "第 %d 步：导数固定为 f′(2.4)，x = %.5f" % (k, xn),
                            dots[:], segs[:], ylim=(-6, 12)))
        x = xn
    save_gif(frames, name)


def secant_gif(name):
    f = lambda t: t**3 - 2 * t - 5
    x0, x1 = 3.2, 2.4
    frames, segs, dots = [], [], []
    for k in range(7):
        y0, y1 = f(x0), f(x1)
        dots += [(x0, y0), (x1, y1)]
        x2 = x1 - y1 * (x1 - x0) / (y1 - y0)
        segs.append((x0, y0, x1, y1))
        frames.append(frame(f, 1.2, 3.6, "第 %d 步：割线两点 (%.4f, %.4f)，x = %.5f"
                            % (k, x0, x1, x2), dots[:], segs[:], ylim=(-6, 12)))
        x0, x1 = x1, x2
    save_gif(frames, name)


def bisection_gif(name):
    f = lambda t: t**3 - 2 * t - 5
    lo, hi = 2.0, 3.0
    frames, dots = [], []
    for k in range(8):
        mid = (lo + hi) / 2
        dots.append((mid, 0.0))
        if f(lo) * f(mid) <= 0:
            hi = mid
        else:
            lo = mid

        def band(ax, lo=lo, hi=hi):
            ax.axvspan(lo, hi, color="#e8eef7", zorder=1)
            ax.text((lo + hi) / 2, 9, "[%.4f, %.4f]" % (lo, hi),
                    fontsize=9, color=GREY, ha="center")

        frames.append(frame(f, 1.8, 3.2, "第 %d 步：区间长度 %.5f" % (k, hi - lo),
                            dots[:], [], extra=band, ylim=(-6, 12)))
    save_gif(frames, name)


def false_position_gif(name):
    f = lambda t: t**3 - 2 * t - 5
    lo, hi = 2.0, 3.0
    frames, segs, dots = [], [], []
    for k in range(7):
        flo, fhi = f(lo), f(hi)
        x = hi - fhi * (hi - lo) / (fhi - flo)
        segs.append((lo, flo, hi, fhi))
        dots.append((x, 0.0))
        frames.append(frame(f, 1.8, 3.2, "第 %d 步：割线截距 x = %.5f" % (k, x),
                            dots[:], segs[:], ylim=(-6, 12)))
        if f(lo) * f(x) <= 0:
            hi = x
        else:
            lo = x
    save_gif(frames, name)


def fixed_point_gif(name):
    f = lambda t: np.sqrt(2 * t + 5)      # x = sqrt(2x+5)
    x, frames, segs, dots = 1.0, [], [], []
    xs = np.linspace(0.5, 4.2, 400)
    for k in range(8):
        y = f(x)
        dots.append((x, y))
        segs.append((x, x, x, y))          # 竖线：到曲线上
        segs.append((x, y, y, y))          # 横线：投到 y=x
        frames.append(frame(lambda t: f(t) - t, 0.5, 4.2,
                            "第 %d 步：x = %.5f" % (k, y), dots[:], segs[:],
                            ylim=(-2.5, 2.0)))
        x = y
    save_gif(frames, name)


def muller_gif(name):
    f = lambda t: t**3 - 2 * t - 5
    x0, x1, x2 = 3.4, 3.0, 2.5
    frames, dots, segs = [], [], []
    for k in range(6):
        # 过三点的抛物线
        xs = np.array([x0, x1, x2], float)
        ys = f(xs)
        coeff = np.polyfit(xs, ys, 2)
        xx = np.linspace(1.4, 3.6, 300)
        dots.append((x2, f(x2)))
        segs.append((xx[0], np.polyval(coeff, xx[0]), xx[-1], np.polyval(coeff, xx[-1])))

        def para(ax, coeff=coeff, xx=xx):
            ax.plot(xx, np.polyval(coeff, xx), color=TAN, lw=1.4, alpha=0.9, zorder=2)

        roots = np.roots(coeff)
        real = [r.real for r in roots if abs(r.imag) < 1e-6]
        xn = min(real, key=lambda r: abs(r - x2)) if real else x2
        frames.append(frame(f, 1.4, 3.6, "第 %d 步：抛物线近似，x = %.5f" % (k, xn),
                            dots[:], segs[:], extra=para, ylim=(-6, 12)))
        x0, x1, x2 = x1, x2, xn
    save_gif(frames, name)


def rk4_gif(name):
    """四阶龙格-库塔解 y' = y - t，和精确解对比。"""
    f = lambda t, y: y - t
    exact = lambda t: t + 1            # y(0)=1 时 y = t + 1
    frames = []
    ts = np.linspace(0, 4, 9)
    ys = [1.0]
    for i in range(1, len(ts)):
        t, y = ts[i - 1], ys[-1]
        h = ts[i] - ts[i - 1]
        k1 = f(t, y)
        k2 = f(t + h / 2, y + h * k1 / 2)
        k3 = f(t + h / 2, y + h * k2 / 2)
        k4 = f(t + h, y + h * k3)
        ys.append(y + h * (k1 + 2 * k2 + 2 * k3 + k4) / 6)

        fig, ax = plt.subplots(figsize=(6.4, 3.6), dpi=100)
        tt = np.linspace(0, 4, 300)
        ax.plot(tt, exact(tt), color=CURVE, lw=2.0, label="精确解")
        ax.plot(ts[: i + 1], ys, "o-", color=POINT, ms=6, lw=1.6, label="RK4 近似")
        ax.set_xlim(0, 4)
        ax.set_ylim(0, 6)
        ax.set_xticks([]); ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_color("#d8dde3")
        ax.legend(frameon=False, fontsize=9, loc="upper left")
        ax.set_title("第 %d 步：龙格-库塔四阶，误差 %.2e" % (i, abs(ys[-1] - exact(ts[i]))),
                     fontsize=12, color=INK, loc="left", pad=8)
        fig.tight_layout()
        frames.append(grab(fig))
    save_gif(frames, name, dur=800)


def hill_climb_gif(name):
    f = lambda t: -(t - 1.5) ** 2 + 3        # 求最大值
    x, frames = 0.2, []
    for k in range(9):
        seg = []
        for dx in (-0.3, 0.3):
            seg.append((x + dx, f(x + dx), x, f(x)))

        def arrows(ax, x=x):
            ax.annotate("", xy=(x + 0.25, f(x + 0.25)), xytext=(x, f(x)),
                        arrowprops=dict(arrowstyle="->", color=GREY, lw=1.2))

        frames.append(frame(f, -0.4, 3.4, "第 %d 步：x = %.3f，f = %.3f（求最大值）"
                            % (k, x, f(x)), [(x, f(x))], seg, extra=arrows,
                            ylim=(-1.5, 3.6)))
        x += 0.25 if f(x + 0.3) > f(x - 0.3) else -0.25
        x = float(np.clip(x, -0.3, 3.3))
    save_gif(frames, name, dur=700)


def steepest_descent_gif(name):
    """最速下降法求 f(x,y)=(x-1)^2+(y-2)^2 的最小值。"""
    f2 = lambda x, y: (x - 1) ** 2 + (y - 2) ** 2
    frames = []
    x, y = np.array([-1.2, 0.2])
    path = [tuple(np.array([x, y]))]
    gx, gy = np.meshgrid(np.linspace(-2, 3, 120), np.linspace(-1, 4, 120))
    for k in range(12):
        g = np.array([2 * (x - 1), 2 * (y - 2)])
        step = 0.35
        x, y = x - step * g[0], y - step * g[1]
        path.append((x, y))
        fig, ax = plt.subplots(figsize=(6.4, 3.6), dpi=100)
        ax.contour(gx, gy, f2(gx, gy), levels=10, colors="#c9d3e2", linewidths=1.0)
        px, py = zip(*path)
        ax.plot(px, py, "o-", color=POINT, ms=5, lw=1.5)
        ax.plot([1], [2], "*", color="#b03a2e", ms=14)
        ax.set_xlim(-2, 3); ax.set_ylim(-1, 4)
        ax.set_xticks([]); ax.set_yticks([])
        for sp in ax.spines.values():
            sp.set_color("#d8dde3")
        ax.set_title("第 %d 步：(%.3f, %.3f)，f = %.4f" % (k + 1, x, y, f2(x, y)),
                     fontsize=12, color=INK, loc="left", pad=8)
        fig.tight_layout()
        frames.append(grab(fig))
    save_gif(frames, name, dur=600)


# ---------------------------------------------------------------- 三个静态图
def quadratic_png():
    fig, ax = plt.subplots(figsize=(9.6, 5.1), dpi=100)
    xs = np.linspace(-4, 6, 400)
    for c, col, note, ytxt in [(-6, "#1f2d5a", "Δ>0 两个不等实根", -4.4),
                               (-1, "#c0504d", "Δ=0 重根", -2.1),
                               (2.5, "#4a7c59", "Δ<0 无实根", 0.4)]:
        ax.plot(xs, xs**2 - 2 * xs + c, color=col, lw=2.2)
        ax.text(4.2, ytxt, note, fontsize=12, color=col)
    ax.axhline(0, color=GREY, lw=1.0)
    ax.axvline(1, color=GREY, lw=1.0, ls=":")
    ax.plot([-1.449], [0], "o", color="#1f2d5a", ms=7)
    ax.plot([3.449], [0], "o", color="#1f2d5a", ms=7)
    ax.plot([1], [0], "o", color="#c0504d", ms=7)
    ax.text(-1.6, -0.5, "x₁", fontsize=12)
    ax.text(3.5, -0.5, "x₂", fontsize=12)
    ax.text(1.05, -0.5, "x₁=x₂", fontsize=12)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_color("#d8dde3")
    ax.set_title("同一条抛物线上下平移，判别式的符号决定它与 x 轴的交点个数",
                 fontsize=12, color=INK, pad=10)
    fig.tight_layout()
    fig.savefig(BASE + "shuzhi-quadratic.png", dpi=100)
    plt.close(fig)
    print("ok shuzhi-quadratic.png")


def quintic_png():
    fig, ax = plt.subplots(figsize=(9.6, 5.1), dpi=100)
    xs = np.linspace(0.4, 2.2, 400)
    ax.plot(xs, xs**5 - 3 * xs - 1, color=CURVE, lw=2.2)
    ax.axhline(0, color=GREY, lw=1.0)
    ax.plot([1.1329], [0], "o", color=POINT, ms=8)
    ax.annotate("唯一的实根 x ≈ 1.1329", xy=(1.1329, 0), xytext=(1.45, 4),
                fontsize=12, color=POINT,
                arrowprops=dict(arrowstyle="->", color=POINT, lw=1.2))
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_color("#d8dde3")
    ax.set_title("五次方程 x⁵-3x-1=0：实根附近函数单调，迭代法收敛得快", fontsize=12,
                 color=INK, pad=10)
    fig.tight_layout()
    fig.savefig(BASE + "shuzhi-quintic.png", dpi=100)
    plt.close(fig)
    print("ok shuzhi-quintic.png")


def transcendental_png():
    fig, ax = plt.subplots(figsize=(9.6, 5.1), dpi=100)
    xs = np.linspace(0.1, 3.2, 400)
    ax.plot(xs, np.exp(xs) - 3 * xs, color=CURVE, lw=2.2)
    ax.plot(xs, np.zeros_like(xs), color=GREY, lw=1.0)
    for r in (0.6191, 1.5121):
        ax.plot([r], [0], "o", color=POINT, ms=8)
    ax.text(0.66, -0.35, "x₁≈0.619", fontsize=12, color=POINT)
    ax.text(1.56, -0.35, "x₂≈1.512", fontsize=12, color=POINT)
    ax.set_xticks([]); ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_color("#d8dde3")
    ax.set_title("超越方程 eˣ-3x=0 有两个根，初值选在哪一侧决定收敛到哪一个",
                 fontsize=12, color=INK, pad=10)
    fig.tight_layout()
    fig.savefig(BASE + "shuzhi-transcendental.png", dpi=100)
    plt.close(fig)
    print("ok shuzhi-transcendental.png")


def golden_section_gif(name):
    """黄金分割法（0.618 法）求单峰函数极小值。"""
    f = lambda t: (t - 1.2) ** 2 + 0.4 * np.sin(6 * t) + 2
    lo, hi = 0.0, 3.0
    g = (np.sqrt(5) - 1) / 2
    frames = []
    for k in range(10):
        x1 = hi - g * (hi - lo)
        x2 = lo + g * (hi - lo)
        if f(x1) < f(x2):
            hi = x2
        else:
            lo = x1

        def band(ax, lo=lo, hi=hi, x1=x1, x2=x2):
            ax.axvspan(lo, hi, color="#e8eef7", zorder=1)
            for x, c in ((x1, POINT), (x2, POINT)):
                ax.plot([x], [f(x)], "o", color=c, ms=6, zorder=6)
            ax.text((lo + hi) / 2, 6.2, "[%.4f, %.4f]" % (lo, hi),
                    fontsize=9, color=GREY, ha="center")

        frames.append(frame(f, -0.1, 3.1, "第 %d 步：区间长度 %.5f" % (k, hi - lo),
                            [], [], extra=band, ylim=(1.0, 6.6)))
    save_gif(frames, name, dur=750)


if __name__ == "__main__":
    golden_section_gif("shuzhi-golden-section.gif")
    damped_newton_gif("shuzhi-damped-newton.gif")
    simplified_newton_gif("shuzhi-simplified-newton.gif")
    secant_gif("shuzhi-secant.gif")
    bisection_gif("shuzhi-bisection.gif")
    false_position_gif("shuzhi-false-position.gif")
    fixed_point_gif("shuzhi-fixed-point.gif")
    muller_gif("shuzhi-muller.gif")
    rk4_gif("shuzhi-rk4.gif")
    hill_climb_gif("shuzhi-hill-climb.gif")
    steepest_descent_gif("shuzhi-steepest-descent.gif")
    quadratic_png()
    quintic_png()
    transcendental_png()
