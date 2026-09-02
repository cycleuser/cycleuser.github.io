# -*- coding: utf-8 -*-
"""一维查找方法综述配图与 GIF。"""
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation, PillowWriter
import math, os

plt.rcParams["font.sans-serif"] = ["PingFang HK", "Heiti TC", "Arial Unicode MS", "SimHei"]
plt.rcParams["axes.unicode_minus"] = False
OUT = os.path.dirname(os.path.abspath(__file__))
phi = (math.sqrt(5) - 1) / 2


# ============ 图1：黄金分割为何能复用点 ============
fig, ax = plt.subplots(figsize=(8, 3.2))
a, b = 0, 1
c = b - phi*(b-a); d = a + phi*(b-a)
ax.plot([a, b], [1, 1], 'k-', lw=1)
for x, lab, col in [(a,'a','#333'),(b,'b','#333'),(c,'c','#e74c3c'),(d,'d','#2980b9')]:
    ax.plot(x, 1, 'o', color=col, ms=8)
    ax.annotate(lab, (x,1), textcoords="offset points", xytext=(0,10), ha='center', color=col)
a2, b2 = a, d
d2 = a2 + phi*(b2-a2); c2 = b2 - phi*(b2-a2)
ax.plot([a2, b2], [0.5, 0.5], 'k-', lw=1)
ax.plot(d2, 0.5, 'o', color='#2980b9', ms=8)
ax.annotate("旧 c → 新 d（复用！）", (d2,0.5), textcoords="offset points",
            xytext=(0,10), ha='center', color='#2980b9', fontsize=9)
ax.plot(c2, 0.5, 'o', color='#e74c3c', ms=8)
ax.annotate("新 c（唯一新增求值）", (c2,0.5), textcoords="offset points",
            xytext=(0,-16), ha='center', color='#e74c3c', fontsize=9)
ax.set_ylim(0.2, 1.4); ax.set_xlim(-0.05, 1.05); ax.set_yticks([0.5,1],['第2轮','第1轮'])
ax.set_title("黄金分割的秘密：比率恒为 φ=0.618，每轮只需 1 次新求值")
ax.spines[['top','right']].set_visible(False)
plt.tight_layout()
fig.savefig(os.path.join(OUT,"查找综述-复用.svg"))
fig.savefig(os.path.join(OUT,"查找综述-复用.png"), dpi=150)
plt.close(fig); print("saved 复用")


# ============ 图2：Fibonacci 比率逐轮变化却收敛到 φ ============
fib=[1,1]
while len(fib)<16: fib.append(fib[-1]+fib[-2])
ratios = [fib[k-1]/fib[k] for k in range(2,15)]
fig, ax = plt.subplots(figsize=(8, 4.2))
ax.plot(range(1,len(ratios)+1), ratios, 'o-', color='#8e44ad', ms=6, label='Fibonacci 每轮保留比率')
ax.axhline(phi, color='#f39c12', ls='--', lw=1.5, label=f'黄金比率 φ={phi:.4f}')
for i,(r) in enumerate(ratios[:6]):
    ax.annotate(f'{fib[i+1]}/{fib[i+2]}', (i+1, r), textcoords="offset points",
                xytext=(0,10 if i%2 else -14), ha='center', fontsize=8, color='#8e44ad')
ax.set_xlabel('迭代轮数'); ax.set_ylabel('该轮区间保留比率')
ax.set_title('Fibonacci 查找：比率逐轮变化(0.5→0.667→0.6→...)，却仍复用旧点，极限是 φ')
ax.legend(fontsize=9); ax.grid(True, alpha=0.3)
plt.tight_layout()
fig.savefig(os.path.join(OUT,"查找综述-fibonacci.svg"))
fig.savefig(os.path.join(OUT,"查找综述-fibonacci.png"), dpi=150)
plt.close(fig); print("saved fibonacci")


# ============ 图3：总求值次数柱状对比 ============
labels = ['三分','黄金GS','Fibonacci','抛物线','Brent','二分\n(需导数)']
calls  = [560, 248, 240, 151, 136, 120]
colors = ['#16a085','#f39c12','#8e44ad','#3498db','#27ae60','#95a5a6']
notes  = ['无复用','复用,比率恒定','复用,比率变化\n(最优)','用曲率','曲率+兜底','需梯度']
fig, ax = plt.subplots(figsize=(9, 4.8))
bars = ax.bar(labels, calls, color=colors, alpha=0.85)
for bar, c, nt in zip(bars, calls, notes):
    ax.text(bar.get_x()+bar.get_width()/2, c+8, str(c), ha='center', fontsize=10, weight='bold')
    ax.text(bar.get_x()+bar.get_width()/2, c/2, nt, ha='center',
            color='white', fontsize=8)
ax.set_ylabel('8 个测试函数合计求值次数（越低越好）')
ax.set_title('一维查找方法总开销对比（全部收敛正确）')
ax.grid(True, axis='y', alpha=0.3)
plt.tight_layout()
fig.savefig(os.path.join(OUT,"查找综述-对比.svg"))
fig.savefig(os.path.join(OUT,"查找综述-对比.png"), dpi=150)
plt.close(fig); print("saved 对比")


# ============ 图4：方法家族关系图 ============
fig, ax = plt.subplots(figsize=(9, 5.2))
ax.axis('off')
boxes = {
    "只比大小\n(无导数)": (0.5, 0.9, '#34495e'),
    "三分查找\n不复用,2/轮": (0.15, 0.62, '#16a085'),
    "Fibonacci\n复用,比率变,最优": (0.5, 0.62, '#8e44ad'),
    "黄金分割\nFib的n→∞极限": (0.5, 0.34, '#f39c12'),
    "用函数值大小\n+曲率": (0.85, 0.62, '#3498db'),
    "抛物线插值\n超线性但不牢靠": (0.85, 0.34, '#3498db'),
    "Brent\n插值+黄金兜底": (0.85, 0.08, '#27ae60'),
    "用导数": (0.15, 0.34, '#95a5a6'),
    "二分/牛顿\n最快但需梯度": (0.15, 0.08, '#95a5a6'),
}
pos = {}
for txt,(x,y,col) in boxes.items():
    ax.add_patch(plt.Rectangle((x-0.11,y-0.05),0.22,0.1, facecolor=col, alpha=0.85,
                                edgecolor='k', lw=0.5, zorder=2))
    ax.text(x,y,txt, ha='center', va='center', color='white', fontsize=8.5, zorder=3, weight='bold')
    pos[txt]=(x,y)
def link(a,b):
    x1,y1=pos[a]; x2,y2=pos[b]
    ax.annotate("", (x2,y2+0.05),(x1,y1-0.05), arrowprops=dict(arrowstyle='->',color='#555',lw=1.2))
link("只比大小\n(无导数)","三分查找\n不复用,2/轮")
link("只比大小\n(无导数)","Fibonacci\n复用,比率变,最优")
link("只比大小\n(无导数)","用函数值大小\n+曲率")
link("Fibonacci\n复用,比率变,最优","黄金分割\nFib的n→∞极限")
link("用函数值大小\n+曲率","抛物线插值\n超线性但不稳")
link("抛物线插值\n超线性但不稳","Brent\n插值+黄金兜底")
ax.plot([0.5,0.15],[0.85,0.39],color='#555',lw=0) # spacer
ax.annotate("",(0.15,0.39),(0.5,0.85),arrowprops=dict(arrowstyle='->',color='#555',lw=1.2))
link("用导数","二分/牛顿\n最快但需梯度")
ax.set_xlim(0,1); ax.set_ylim(0,1)
ax.set_title('一维查找方法家族：信息用得越多，收敛越快，但要求也越高', fontsize=12)
plt.tight_layout()
fig.savefig(os.path.join(OUT,"查找综述-家族.svg"))
fig.savefig(os.path.join(OUT,"查找综述-家族.png"), dpi=150)
plt.close(fig); print("saved 家族")


# ============ 图5：GIF 三种方法同屏收缩对比 ============
f = lambda x: (x-0.35)**2 + 0.12*np.sin(5*x)
a0, b0 = 0.0, 1.0

def gs_frames():
    a,b=a0,b0; c=b-phi*(b-a); d=a+phi*(b-a); fc,fd=f(c),f(d); out=[(a,b)]
    for _ in range(16):
        if fc<fd: b,d,fd=d,c,fc; c=b-phi*(b-a); fc=f(c)
        else: a,c,fc=c,d,fd; d=a+phi*(b-a); fd=f(d)
        out.append((a,b))
    return out

def tern_frames():
    a,b=a0,b0; out=[(a,b)]
    for _ in range(16):
        c=a+(b-a)/3; d=b-(b-a)/3
        if f(c)<f(d): b=d
        else: a=c
        out.append((a,b))
    return out

def fib_frames():
    fib=[1,1]
    while fib[-1]<(b0-a0)/1e-4: fib.append(fib[-1]+fib[-2])
    n=len(fib)-1; a,b=a0,b0
    c=a+fib[n-2]/fib[n]*(b-a); d=a+fib[n-1]/fib[n]*(b-a); fc,fd=f(c),f(d); out=[(a,b)]
    for k in range(1,min(n-1,17)):
        if fc<fd: b,d,fd=d,c,fc; c=a+fib[n-k-2]/fib[n-k]*(b-a); fc=f(c)
        else: a,c,fc=c,d,fd; d=a+fib[n-k-1]/fib[n-k]*(b-a); fd=f(d)
        out.append((a,b))
    return out

gsf, tnf, fbf = gs_frames(), tern_frames(), fib_frames()
nf = max(len(gsf),len(tnf),len(fbf))
def pad(l): return l+[l[-1]]*(nf-len(l))
gsf,tnf,fbf = pad(gsf),pad(tnf),pad(fbf)
xs = np.linspace(a0,b0,400)
fig, axes = plt.subplots(1,3, figsize=(12,4))
titles=['三分 (2求值/轮)','黄金分割 (1求值/轮)','Fibonacci (1求值/轮,最优)']
cols=['#16a085','#f39c12','#8e44ad']
def frame(i):
    for ax,frames,t,col in zip(axes,[tnf,gsf,fbf],titles,cols):
        ax.clear()
        a,b=frames[i]
        ax.plot(xs,f(xs),color='#2c3e50',lw=1.5)
        ax.axvspan(a,b,color=col,alpha=0.25)
        ax.axvline(a,color=col,ls='--',lw=1); ax.axvline(b,color=col,ls='--',lw=1)
        ax.set_title(f'{t}\n第{i}轮 宽{b-a:.4f}',fontsize=10)
        ax.set_xlim(a0,b0); ax.set_ylim(f(xs).min()-0.05,f(xs).max()+0.05)
        ax.grid(True,alpha=0.3)
    plt.tight_layout()
ani=FuncAnimation(fig,frame,frames=nf,interval=600)
ani.save(os.path.join(OUT,"查找综述-对比过程.gif"),writer=PillowWriter(fps=2))
plt.close(fig); print("saved 对比过程.gif")
print("ALL DONE")
