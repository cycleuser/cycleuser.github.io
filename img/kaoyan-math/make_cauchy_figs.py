import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

plt.rcParams["font.family"] = ["PingFang SC", "Arial Unicode MS", "DejaVu Sans"]
plt.rcParams["axes.unicode_minus"] = False

INK   = "#2b2b2b"
ORANGE = "#d2691e"
BLUE  = "#2f4f6f"
CREAM = "#f3e3ce"
RED   = "#b03a2e"

BASE = "/Users/fred/Documents/GitHub/cycleuser/blog/output/img/kaoyan-math/"

def style(ax):
    ax.spines[["top", "right"]].set_visible(False)
    for s in ax.spines.values():
        s.set_color("#888")
    ax.tick_params(colors="#555")


# ============ 图：三种形式共用同一个"非负二次函数"骨架 ============
fig, axes = plt.subplots(1, 3, figsize=(13.2, 4.4), dpi=150)
t = np.linspace(-3, 3, 400)

# 面板1：代数形式 q(t)=A t^2 + 2B t + C，最小值 (AC-B^2)/A >= 0
A, B, C = 1.0, 1.0, 2.0     # B^2=1 <= AC=2，最小值 1>0
q = A*t**2 + 2*B*t + C
ax = axes[0]
ax.plot(t, q, color=BLUE, lw=2.4)
tmin = -B/A; qmin = (A*C - B**2)/A
ax.plot([tmin], [qmin], "o", color=ORANGE, ms=8, zorder=6)
ax.axhline(qmin, color=ORANGE, lw=1.2, ls="--")
ax.annotate("最小值 $\\dfrac{AC-B^2}{A}\\geq 0$", xy=(tmin, qmin),
            xytext=(tmin+0.15, qmin+1.2), fontsize=10.5, color=ORANGE)
ax.axhline(0, color="#999", lw=0.9)
ax.set_title("代数：$q(t)=At^2+2Bt+C\\geq0$", fontsize=11.5, color=INK)
ax.set_xlabel("$t$", fontsize=11, color=INK); ax.set_ylabel("$q(t)$", fontsize=11, color=INK)
style(ax)

# 面板2：向量形式 ||u+tv||^2，最小值 = ||u||^2 - <u,v>^2/||v||^2 >= 0
# 取 u,v，令 q(t)=||u+tv||^2
ax = axes[1]
u = np.array([2.0, 1.0]); v = np.array([1.0, 0.5])
uv = u@v; vv = v@v; uu = u@u
q2 = uu + 2*uv*t + vv*t**2
ax.plot(t, q2, color=BLUE, lw=2.4)
tmin2 = -uv/vv; qmin2 = uu - uv**2/vv
ax.plot([tmin2], [qmin2], "o", color=ORANGE, ms=8, zorder=6)
ax.axhline(qmin2, color=ORANGE, lw=1.2, ls="--")
ax.annotate("最小值 $\\|u\\|^2-\\dfrac{\\langle u,v\\rangle^2}{\\|v\\|^2}\\geq0$",
            xy=(tmin2, qmin2), xytext=(tmin2+0.15, qmin2+1.2), fontsize=10.5, color=ORANGE)
ax.axhline(0, color="#999", lw=0.9)
ax.set_title("向量：$\\|u+tv\\|^2\\geq0$", fontsize=11.5, color=INK)
ax.set_xlabel("$t$", fontsize=11, color=INK); ax.set_ylabel("$\\|u+tv\\|^2$", fontsize=11, color=INK)
style(ax)

# 面板3：积分形式 int (tf+g)^2，最小值 = int f^2 - (int fg)^2/int g^2 >= 0
ax = axes[2]
f = lambda x: 1.0 + 0.6*np.sin(2*x)     # 正函数
g = lambda x: 0.5 + 0.4*np.cos(x)
xx = np.linspace(0, 2*np.pi, 800)
ff = f(xx); gg = g(xx)
dt = xx[1]-xx[0]
I_fg = np.sum(ff*gg)*dt; I_ff = np.sum(ff*ff)*dt; I_gg = np.sum(gg*gg)*dt
q3 = I_ff + 2*I_fg*t + I_gg*t**2
ax.plot(t, q3, color=BLUE, lw=2.4)
tmin3 = -I_fg/I_gg; qmin3 = I_ff - I_fg**2/I_gg
ax.plot([tmin3], [qmin3], "o", color=ORANGE, ms=8, zorder=6)
ax.axhline(qmin3, color=ORANGE, lw=1.2, ls="--")
ax.annotate("最小值 $\\int f^2-\\dfrac{(\\int fg)^2}{\\int g^2}\\geq0$",
            xy=(tmin3, qmin3), xytext=(tmin3+0.15, qmin3+1.2), fontsize=10.5, color=ORANGE)
ax.axhline(0, color="#999", lw=0.9)
ax.set_title("积分：$\\int(tf+g)^2\\geq0$", fontsize=11.5, color=INK)
ax.set_xlabel("$t$", fontsize=11, color=INK); ax.set_ylabel("$\\int(tf+g)^2$", fontsize=11, color=INK)
style(ax)

fig.suptitle("三种形式，同一个骨架：造一个非负的二次函数，它的最小值 ≥ 0 就是柯西不等式", fontsize=12.5, color=INK)
fig.tight_layout()
fig.savefig(BASE + "cauchy-three-forms.png", dpi=150)
plt.close(fig)


# ============ 图：代数形式 q(t) 的两种情形（最小值>0 / 相切=0 取等）============
fig, (axL, axR) = plt.subplots(1, 2, figsize=(10.4, 4.4), dpi=150)
t = np.linspace(-3, 3, 400)
# 左：严格 B^2 < AC，最小值 > 0，无交点
A, B, C = 1.0, 1.0, 2.0
qL = A*t**2 + 2*B*t + C
axL.plot(t, qL, color=BLUE, lw=2.4)
qminL = (A*C-B**2)/A; tminL = -B/A
axL.plot([tminL],[qminL],"o",color=ORANGE,ms=8,zorder=6)
axL.axhline(0,color="#999",lw=0.9)
axL.annotate("最小值 $>0$：整条在 $t$ 轴上方\n$B^2<AC$", xy=(tminL,qminL),
             xytext=(tminL+0.2,qminL+1.0), fontsize=10.5, color=ORANGE)
axL.set_title("情形：$B^2<AC$（严格大于）", fontsize=11.5, color=INK)
axL.set_xlabel("$t$",fontsize=11,color=INK); axL.set_ylabel("$q(t)$",fontsize=11,color=INK)
style(axL)
# 右：B^2 = AC，相切，最小值=0，取等
A, B, C = 1.0, 1.0, 1.0
qR = A*t**2 + 2*B*t + C
axR.plot(t, qR, color=BLUE, lw=2.4)
axR.plot([-B/A],[0],"o",color=RED,ms=9,zorder=6)
axR.axhline(0,color="#999",lw=0.9)
axR.annotate("与 $t$ 轴相切，最小值 $=0$\n$B^2=AC$，此处取等", xy=(-B/A,0),
             xytext=(-B/A+0.2,1.2), fontsize=10.5, color=RED)
axR.set_title("情形：$B^2=AC$（取等）", fontsize=11.5, color=INK)
axR.set_xlabel("$t$",fontsize=11,color=INK); axR.set_ylabel("$q(t)$",fontsize=11,color=INK)
style(axR)
fig.suptitle("代数形式：$q(t)\\geq0$ 恒成立，最小值 $\\dfrac{AC-B^2}{A}$ 必 ≥ 0；等于 0 时取等", fontsize=12, color=INK)
fig.tight_layout()
fig.savefig(BASE + "cauchy-algebra-cases.png", dpi=150)
plt.close(fig)

print("done")
