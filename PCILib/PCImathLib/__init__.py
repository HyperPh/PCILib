# -*- coding: UTF-8 -*-
"""
PCI math Lib

大整数请用python内建类型int

大浮点数请用decimal.Decimal或sympy.Float,比如Decimal('3.1415926535')或Float('1e-3', 3)
"""

import PCILib.PCImathLib.analysis as pcianalysis
import PCILib.PCImathLib.discrete as pcidiscrete
import PCILib.PCImathLib.stat as pcistat


__all__=[]


class Cartesian(object):
    """
    Python 计算笛卡尔积

    计算多个集合的笛卡尔积，有规律可循，算法和代码也不难，但是很多语言都没有提供直接计算笛卡尔积的方法，需要自己写大段大段的代码计算笛卡尔积，python 提供了一种最简单的计算笛卡称积的方法(只需要一行代码)，详见下面的代码：
    >>> car = Cartesian([1, 2, 3, 4])
    >>> car.add_data([5, 6, 7, 8],[9, 10, 11, 12])
    >>> print(car.build(return_list=True))
    [(1, 5, 9), (1, 5, 10), (1, 5, 11), (1, 5, 12), (1, 6, 9), (1, 6, 10), (1, 6, 11), (1, 6, 12), (1, 7, 9), (1, 7, 10), (1, 7, 11), (1, 7, 12), (1, 8, 9), (1, 8, 10), (1, 8, 11), (1, 8, 12), (2, 5, 9), (2, 5, 10), (2, 5, 11), (2, 5, 12), (2, 6, 9), (2, 6, 10), (2, 6, 11), (2, 6, 12), (2, 7, 9), (2, 7, 10), (2, 7, 11), (2, 7, 12), (2, 8, 9), (2, 8, 10), (2, 8, 11), (2, 8, 12), (3, 5, 9), (3, 5, 10), (3, 5, 11), (3, 5, 12), (3, 6, 9), (3, 6, 10), (3, 6, 11), (3, 6, 12), (3, 7, 9), (3, 7, 10), (3, 7, 11), (3, 7, 12), (3, 8, 9), (3, 8, 10), (3, 8, 11), (3, 8, 12), (4, 5, 9), (4, 5, 10), (4, 5, 11), (4, 5, 12), (4, 6, 9), (4, 6, 10), (4, 6, 11), (4, 6, 12), (4, 7, 9), (4, 7, 10), (4, 7, 11), (4, 7, 12), (4, 8, 9), (4, 8, 10), (4, 8, 11), (4, 8, 12)]


    """

    def __init__(self, *data):
        self._data_list = []
        for datum in data:
            self._data_list.append(datum)

    def add_data(self, *data):  # 添加生成笛卡尔积的数据列表
        for datum in data:
            self._data_list.append(datum)

    def build(self, return_list=False):
        """计算笛卡尔积"""
        import itertools
        if return_list:
            return [item for item in itertools.product(*self._data_list)]
        else:  # 返回set类型
            return {item for item in itertools.product(*self._data_list)}


from .stat import (mean,std)


from .discrete import (factorial,Prime,fact,eular,gcd,lcm,sgn,euclidean_algorithm,euclidean_algorithm_recursion,
                       mod_m_inverse,solve_congruence,change_base,pow_n_mod_m,solve_congruence_set,primality_test,
                       primitive_root,discrete_logarithm,legendre_symbol,quick_pow)

from .analysis import (fourier_even,fourier_odd,fourier_series,fourier_transform_inverse,fourier_transform,
                       generalized_fourier,legrendre,legrendre_list,schmidt,schmidt_list,schmidt_orthogonalization,
                       schmidt_orthogonalization_list,convolution,convolution1,dot_product2)


if __name__ == '__main__':
    import time
    import doctest

    start_time = time.time()

    doctest.testmod()

    print("运行时间: {} s".format(time.time() - start_time))
