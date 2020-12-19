"""统计"""

import math


def mean(values):
    """平均值

    :param values:Any
    :return:float

    Example:
        >>> print(mean([20, 30, 10]))
        20.0
        >>>

    """
    return sum(values) / len(values)


def std(a, ddof=1, return_2=False):
    """
    样本标准差,默认除以n-1(无偏),除以n的是有偏的(相当于np.std(ddof=0)),return_2=True时返回样本方差

    ddof - Means Delta Degrees of Freedom (n-自由度)

    pandas的std默认无偏。
    以下是numpy对其默认有偏的解释:

    The average squared deviation is normally calculated as
    ``x.sum() / N``, where ``N = len(x)``.  If, however, `ddof` is specified,
    the divisor ``N - ddof`` is used instead. In standard statistical
    practice, ``ddof=1`` provides an unbiased estimator of the variance
    of the infinite population. ``ddof=0`` provides a maximum likelihood
    estimate of the variance for normally distributed variables. The
    standard deviation computed in this function is the square root of
    the estimated variance, so even with ``ddof=1``, it will not be an
    unbiased estimate of the standard deviation per se.

    Example:
        >>> print(std([20, 30, 10]))
        10.0000000000000
        >>> print(std([1200, 3299.5, 2133, 5433, 3299.5, 4432]))
        1523.35163373398
        >>> print(std([1200, 3299.5, 2133, 5433, 3299.5, 4432],'n'))
        1390.62342134742
        >>>
    """
    std1 = 0
    ave1 = mean(a)
    for v1 in a:
        std1 += (v1 - ave1) ** 2
    std1 /= (len(a) - ddof)

    if return_2:
        return std1
    else:
        return std1**0.5


if __name__ == '__main__':
    print(std([1,2,3]))#1
    print(std([1200, 3299.5, 2133, 5433, 3299.5, 4432]))
    print(std([1200, 3299.5, 2133, 5433, 3299.5, 4432],ddof=0))
