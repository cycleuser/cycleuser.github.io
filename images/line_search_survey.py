# -*- coding: utf-8 -*-
"""一维查找方法综述：基准测试与正确性验证。

包含：二分(导数)、三分、黄金分割、Fibonacci、抛物线插值、Brent。
重点回答：能否在【保持复用】的前提下让收缩比率逐轮变化？
答案：Fibonacci 查找正是如此——每轮比率不同却仍复用一个旧点。
"""
import math

phi = (math.sqrt(5) - 1) / 2   # 0.6180339887...
TOL = 1e-6


# ---------- 测试函数集（单峰，[a,b]） ----------
TESTS = [
    ("二次 (x-0.3)^2",   lambda x:(x-0.3)**2,                          0.,1., (lambda x:2*(x-0.3))),
    ("四次 (x-0.7)^4",   lambda x:(x-0.7)**4,                          0.,1., (lambda x:4*(x-0.7)**3)),
    ("|x-0.4|^1.5",      lambda x:abs(x-0.4)**1.5,                     0.,1., None),
    ("cosh(x-0.55)",     lambda x:math.cosh(x-0.55),                   0.,1., (lambda x:math.sinh(x-0.55))),
    ("-sin(pi x)",       lambda x:-math.sin(math.pi*x),               0.,1., (lambda x:-math.pi*math.cos(math.pi*x))),
    ("尖谷 |x-0.618|",    lambda x:abs(x-0.618),                        0.,1., None),
    ("非对称 exp",        lambda x:math.exp(3*(x-0.2))+math.exp(-5*(x-0.2)), 0.,1.,
                          (lambda x:3*math.exp(3*(x-0.2))-5*math.exp(-5*(x-0.2)))),
    ("平底四次",          lambda x:(x-0.5)**4+1e-3*(x-0.5)**2,          0.,1., (lambda x:4*(x-0.5)**3+2e-3*(x-0.5))),
]


# ---------- 1. 二分法（需要导数符号） ----------
def bisection(f, a, b, df, tol=TOL):
    calls = 0
    def DF(x):
        nonlocal calls; calls += 1; return df(x)
    while (b - a) > tol:
        m = (a + b) / 2
        if DF(m) > 0: b = m
        else:         a = m
    return (a + b) / 2, calls


# ---------- 2. 三分查找 ----------
def ternary(f, a, b, tol=TOL):
    calls = 0
    def F(x):
        nonlocal calls; calls += 1; return f(x)
    while (b - a) > tol:
        c = a + (b - a) / 3
        d = b - (b - a) / 3
        if F(c) < F(d): b = d
        else:           a = c
    return (a + b) / 2, calls


# ---------- 3. 黄金分割（复用一点） ----------
def golden_section(f, a, b, tol=TOL):
    calls = 0
    def F(x):
        nonlocal calls; calls += 1; return f(x)
    c = b - phi*(b-a); d = a + phi*(b-a)
    fc, fd = F(c), F(d)
    while (b - a) > tol:
        if fc < fd:
            b, d, fd = d, c, fc
            c = b - phi*(b-a); fc = F(c)
        else:
            a, c, fc = c, d, fd
            d = a + phi*(b-a); fd = F(d)
    return (a + b) / 2, calls


# ---------- 4. Fibonacci 查找：比率逐轮变化，但仍复用一点！ ----------
def fibonacci_search(f, a, b, tol=TOL):
    calls = 0
    def F(x):
        nonlocal calls; calls += 1; return f(x)
    # 选 n 使 F_n >= (b-a)/tol
    fib = [1, 1]
    while fib[-1] < (b - a) / tol:
        fib.append(fib[-1] + fib[-2])
    n = len(fib) - 1
    # 初始两点，比率 = F_{n-1}/F_{n+1}
    c = a + fib[n-2] / fib[n] * (b - a)
    d = a + fib[n-1] / fib[n] * (b - a)
    fc, fd = F(c), F(d)
    for k in range(1, n - 1):
        if fc < fd:
            b, d, fd = d, c, fc
            c = a + fib[n-k-2] / fib[n-k] * (b - a)   # 每轮比率不同
            fc = F(c)                                  # 但只算 1 个新点
        else:
            a, c, fc = c, d, fd
            d = a + fib[n-k-1] / fib[n-k] * (b - a)
            fd = F(d)
    return (a + b) / 2, calls


# ---------- 5. 抛物线插值 ----------
def parabolic(f, a, b, tol=TOL, maxcalls=200):
    calls = 0
    def F(x):
        nonlocal calls; calls += 1; return f(x)
    x0, x2 = a, b
    x1 = a + phi*(b-a)
    f0, f1, f2 = F(x0), F(x1), F(x2)
    while (x2 - x0) > tol and calls < maxcalls:
        denom = (x1-x0)*(f1-f2) - (x1-x2)*(f1-f0)
        if abs(denom) < 1e-18: break
        xn = x1 - 0.5*((x1-x0)**2*(f1-f2) - (x1-x2)**2*(f1-f0)) / denom
        if not (x0 < xn < x2):
            xn = x1 + (1-phi)*(x2-x1) if (x2-x1) > (x1-x0) else x1 - (1-phi)*(x1-x0)
        fn = F(xn)
        if xn > x1:
            if fn < f1: x0,f0,x1,f1 = x1,f1,xn,fn
            else:       x2,f2 = xn,fn
        else:
            if fn < f1: x2,f2,x1,f1 = x1,f1,xn,fn
            else:       x0,f0 = xn,fn
    return x1, calls


# ---------- 6. Brent 方法：抛物线 + 黄金分割兜底 ----------
def brent(f, a, b, tol=TOL, maxcalls=200):
    calls = 0
    def F(x):
        nonlocal calls; calls += 1; return f(x)
    gr = 1 - phi
    x = w = v = a + phi*(b-a)
    fx = fw = fv = F(x)
    d = e = 0.0
    while calls < maxcalls:
        m = 0.5*(a+b)
        tol1 = tol*abs(x) + 1e-12
        if abs(x - m) <= 2*tol1 - 0.5*(b-a):
            break
        use_para = False
        if abs(e) > tol1:
            r = (x-w)*(fx-fv); q = (x-v)*(fx-fw); p = (x-v)*q - (x-w)*r
            q = 2*(q - r)
            if q > 0: p = -p
            q = abs(q)
            if abs(p) < abs(0.5*q*e) and p > q*(a-x) and p < q*(b-x):
                e = d; d = p/q; use_para = True
        if not use_para:
            e = (b-x) if x < m else (a-x); d = gr*e
        u = x + d if abs(d) >= tol1 else x + math.copysign(tol1, d)
        fu = F(u)
        if fu <= fx:
            if u < x: b = x
            else:     a = x
            v,fv,w,fw,x,fx = w,fw,x,fx,u,fu
        else:
            if u < x: a = u
            else:     b = u
            if fu <= fw or w == x: v,fv,w,fw = w,fw,u,fu
            elif fu <= fv or v == x or v == w: v,fv = u,fu
    return x, calls


def run():
    methods_bracket = [
        ("三分",   ternary),
        ("黄金GS", golden_section),
        ("Fibonacci", fibonacci_search),
        ("抛物线", parabolic),
        ("Brent",  brent),
    ]
    # 正确性
    print("正确性检查（与真解对比，阈值 1e-3）：")
    for mn, mf in methods_bracket:
        bad = 0
        for name,f,a,b,df in TESTS:
            xg,_ = golden_section(f,a,b)
            x,_ = mf(f,a,b)
            if abs(x-xg) > 1e-3: bad += 1
        print(f"  {mn:<10} 收敛错误 {bad}/{len(TESTS)}")
    # 二分单独（需导数）
    bad = sum(1 for name,f,a,b,df in TESTS if df and abs(bisection(f,a,b,df)[0]-golden_section(f,a,b)[0])>1e-3)
    ndf = sum(1 for *_ ,df in TESTS if df)
    print(f"  {'二分(导数)':<10} 收敛错误 {bad}/{ndf}（仅可导函数）")
    print()

    # 求值次数
    hdr = f"{'函数':<18}" + "".join(f"{m:>10}" for m,_ in methods_bracket) + f"{'二分*':>8}"
    print(hdr); print("-"*len(hdr))
    tot = {m:0 for m,_ in methods_bracket}; tot["二分"]=0; ndf2=0
    for name,f,a,b,df in TESTS:
        row = f"{name:<18}"
        for mn,mf in methods_bracket:
            _,c = mf(f,a,b); tot[mn]+=c; row += f"{c:>10}"
        if df:
            _,cb = bisection(f,a,b,df); tot["二分"]+=cb; ndf2+=1; row += f"{cb:>8}"
        else:
            row += f"{'-':>8}"
        print(row)
    print("-"*len(hdr))
    trow = f"{'合计':<18}" + "".join(f"{tot[m]:>10}" for m,_ in methods_bracket) + f"{tot['二分']:>8}"
    print(trow)
    print(f"\n(*二分需要导数，仅在 {ndf2} 个可导函数上统计)")

    # 验证 Fibonacci 逐轮比率确实在变
    print("\nFibonacci 前几轮的保留比率（证明比率在变但仍复用）：")
    fib=[1,1]
    while len(fib)<12: fib.append(fib[-1]+fib[-2])
    for k in range(2,9):
        print(f"  第{k-1}轮 比率 F_{k-1}/F_{k} = {fib[k-1]}/{fib[k]} = {fib[k-1]/fib[k]:.4f}")
    print(f"  ... 极限 -> φ = {phi:.4f}")


if __name__ == "__main__":
    run()
