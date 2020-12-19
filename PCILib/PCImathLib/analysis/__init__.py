"""数学分析"""

import math

try:
    import sympy
    import sympy.abc
    from sympy import oo  # oo是无穷大
    # from sympy.abc import x
except ImportError as e:
    print(e)


# 另一种实现方法
# def fourier_odd(fx, x_tuple=(sympy.abc.x, 0, sympy.pi), T=0, silent=False):
#     x = x_tuple[0]
#     a = x_tuple[1]
#     b = x_tuple[2]


def fourier_odd(fx, x=sympy.abc.x, a=0, b=sympy.pi, T=0, silent=False):
    """
    计算奇延拓Fourier级数的Fourier系数,[0,b]区间,T周期(默认2b)
    """
    from sympy import pi
    n = sympy.Symbol('n', integer=True, positive=True)  # 定义符号n 为正整数

    if T == 0:
        T = 2 * b

    a0 = 0
    an = 0
    bn = sympy.simplify(sympy.integrate(fx * sympy.sin(2 * pi * n * x / T), (x, a, b)) * 4 / T)

    if not silent:
        print(f"{a0/2=}")
        print(f"{an=}")
        print(f"{bn=}")
    return [a0, an, bn]


def fourier_even(fx, x=sympy.abc.x, a=0, b=sympy.pi, T=0, silent=False):
    """计算偶延拓Fourier级数的Fourier系数,[0,b]区间,T周期(默认2b)"""
    from sympy import pi
    n = sympy.Symbol('n', integer=True, positive=True)  # 定义符号n 为正整数

    if T == 0:
        T = 2 * b

    a0 = sympy.simplify(sympy.integrate(fx, (x, a, b)) * 4 / T)
    an = sympy.simplify(sympy.integrate(fx * sympy.cos(2 * pi * n * x / T), (x, a, b)) * 4 / T)
    bn = 0

    if not silent:
        print(f"{a0/2=}")
        print(f"{an=}")
        print(f"{bn=}")
    return [a0, an, bn]


def fourier_series(fx, x=sympy.abc.x, a=-sympy.pi, b=sympy.pi, T=0, silent=False):
    """
    计算Fourier级数的Fourier系数,[a,b]区间,T周期(默认b-a)

    如果不加参数x=sympy.abc.x(即x=sympy.symbols('x')，没有限定条件)，则fx中其他的x会因与此函数中的x不是同一个x对象而导致计算错误

    注:sympy.fourier_series(1+x)或sympy.fourier_series(1+x, (x,-pi,pi))会得到
    FourierSeries(x + 1, (x, -pi, pi), (1, SeqFormula(Piecewise((2*sin(_n*pi)/_n, (_n > -oo) & (_n < oo) & Ne(_n, 0)), (2*pi, True))*cos(_n*x)/pi, (_n, 1, oo)), SeqFormula(Piecewise((-2*pi*cos(_n*pi)/_n + 2*sin(_n*pi)/_n**2, (_n > -oo) & (_n < oo) & Ne(_n, 0)), (0, True))*sin(_n*x)/pi, (_n, 1, oo))))
    这一串看不懂的东西，不如我这个好用

    """
    from sympy import pi
    n = sympy.Symbol('n', integer=True, positive=True)  # 定义符号n 为正整数

    if T == 0:
        T = b - a

    a0 = sympy.simplify(sympy.integrate(fx, (x, a, b)) * 2 / T)
    an = sympy.simplify(sympy.integrate(fx * sympy.cos(2 * pi * n * x / T), (x, a, b)) * 2 / T)
    bn = sympy.simplify(sympy.integrate(fx * sympy.sin(2 * pi * n * x / T), (x, a, b)) * 2 / T)

    if not silent:
        print(f"{a0/2=}")
        print(f"{an=}")
        print(f"{bn=}")
    return [a0, an, bn]


def generalized_fourier(fx, phi_nx, phi_0x=0, x=sympy.abc.x, a=-sympy.pi, b=sympy.pi, silent=False):
    """广义Fourier级数,phi_0x=0时不单独计算a0"""

    a0 = sympy.integrate(fx * phi_0x, (x, a, b))
    a0 = sympy.simplify(a0)

    an = sympy.integrate(fx * phi_nx, (x, a, b))
    an = sympy.simplify(an)

    if not silent:
        print(f"{a0=}")
        print(f"{an=}")
    return [a0, an]


def fourier_transform(fx, x=sympy.abc.x, silent=False):
    r"""Fourier变换

    .. math:: F(k) = \int_{-\infty}^\infty f(x) e^{- i x k} \mathrm{d} x.
    """
    k = sympy.symbols('k', real=True)
    # 无用 fx.subs(x, x1)  # 将fx中的 默认x 替换成 x1(实数x),若fx原来就是实数x也不会报错
    Fk = sympy.integrate(fx * sympy.exp(-sympy.I * k * x), (x, -oo, oo))
    if not silent:
        print(Fk)
    return Fk


def fourier_transform_inverse(Fk, k=sympy.abc.k, silent=False):
    r"""Fourier变换的逆变换

        .. math:: F(k) = \int_{-\infty}^\infty f(x) e^{- i x k} \mathrm{d} x.
        """
    x = sympy.symbols('x', real=True)
    fx = sympy.integrate(Fk * sympy.exp(sympy.I * k * x), (k, -oo, oo)) / (2 * sympy.pi)
    if not silent:
        print(fx)
    return fx



def dot_product2(fx, gx, x=sympy.abc.x, a=-1, b=1, silent=True):
    """积分形式的内积"""
    from sympy import integrate
    o1 = integrate(fx * gx, (x, a, b))
    if not silent:
        print(f"fx*gx={o1}")
    return o1


def schmidt_orthogonalization(fix: list, n, e: list, x=sympy.abc.x, a=-1, b=1):
    """施密特正交化,输出为列表,n=len(fix),手动选择积分区间[a,b]"""
    from sympy import sqrt
    # dot_product=dot_product2 #另一种实现方法,手动选择内积

    if n == 1:
        e[0] = fix[0] / sqrt(dot_product2(fix[0], fix[0], x, a, b))
    else:
        schmidt_orthogonalization(fix, n - 1, e, x, a, b)
        e[n - 1] = fix[n - 1]
        for j in range(0, n - 1):
            e[n - 1] -= dot_product2(fix[n - 1], e[j], x, a, b) * e[j]
        e[n - 1] /= sqrt(dot_product2(e[n - 1], e[n - 1], x, a, b))


def schmidt(fix: list, n, e: list, dot_product=dot_product2, x=sympy.abc.x):
    """施密特正交化,输出在e列表,n=len(fix),手动选择内积dot_product"""
    from sympy import sqrt

    if n == 1:
        e[0] = fix[0] / sqrt(dot_product(fix[0], fix[0], x))
    else:
        schmidt(fix, n - 1, e, dot_product, x)
        e[n - 1] = fix[n - 1]
        for j in range(0, n - 1):
            e[n - 1] -= dot_product(fix[n - 1], e[j], x) * e[j]
        e[n - 1] /= sqrt(dot_product(e[n - 1], e[n - 1], x))


def schmidt_orthogonalization_list(fix: list, n, x=sympy.abc.x, a=-1, b=1, silent=True):
    """施密特正交化,输出为列表,n=len(fix),手动选择积分区间[a,b]"""
    e = []
    for i in range(0, n):
        e.append(None)
    schmidt_orthogonalization(fix, n, e, x, a, b)
    if not silent:
        print(e)
    return e


def schmidt_list(fix: list, n, dot_product=dot_product2, x=sympy.abc.x, silent=True):
    """施密特正交化,输出为列表,n=len(fix),手动选择内积dot_product"""
    e = []
    for i in range(0, n):
        e.append(None)
    schmidt(fix, n, e, dot_product, x)
    if not silent:
        print(e)
    return e


def convolution1(ft, gx_t, silent=True):
    """卷积,核心算法"""
    from sympy import integrate
    t = sympy.symbols('t', real=True)
    o1 = integrate(ft * gx_t, (t, -oo, oo))
    if not silent:
        print(f"(f*g)(x)={o1}")
    return o1


def convolution(fx: str, gx: str):
    """卷积"""
    t = sympy.symbols('t', real=True)
    ft1 = fx.replace('x', 't')
    gx_t1 = gx.replace('x', '(x-t)')
    exec("ft2=" + ft1)
    exec("gx_t2=" + gx_t1)
    o1 = [None]  # 必须用引用类型(比如列表),否则报错
    exec("o1[0]=convolution1(ft2, gx_t2)")
    return o1[0]


def legrendre(n, x=sympy.abc.x):
    """勒让德多项式"""
    pnx = 1 / (2 ** n * sympy.factorial(n)) * sympy.diff((x * x - 1) ** n, x, n)
    # print(pnx)
    return pnx


def legrendre_list(n, x=sympy.abc.x):
    """勒让德多项式表"""
    l1 = []
    for i in range(0, n):
        l1.append(legrendre(i, x))
    print(l1)  # [1, x, (3*x**2 - 1)/2, x*(5*x**2 - 3)/2, (8*x**4 + 24*x**2*(x**2 - 1) + 3*(x**2 - 1)**2)/8]
    return l1


def laplace_transform(ft, t=sympy.abc.t, silent=False):
    r"""Laplace变换

    .. math:: F(p) = \int_{0}^\infty f(x) e^{-pt} \mathrm{d} t.
    """
    p = sympy.symbols('p')
    Fp = sympy.integrate(ft * sympy.exp(-p * t), (t, 0, oo))
    if not silent:
        print(Fp)
    return Fp


if __name__ == '__main__':
    x,t = sympy.symbols("x,t")  # sympy.symbols("x")等价于sympy.abc.x
    fourier_even(1 + x, x)
    fourier_odd(1 + x, x)
    fourier_series(1 + x, x, 0, sympy.pi)
    fourier_transform(sympy.sin(x), x)
    laplace_transform(1)
    laplace_transform(t ** 2, t)
    # 输出结果中Piecewise表示分段函数,Ne(n,0)表示n!=0,True表示除去前面(Ne(n,0))的情况(即n==0)
    # 已修复n的类型,不会输出上述结果了

