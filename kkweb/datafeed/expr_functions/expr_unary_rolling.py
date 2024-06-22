import numpy as np
import pandas as pd
from .expr_utils import calc_by_symbol, calc_by_date


@calc_by_symbol
def quantile(se: pd.Series, N, qscore=0.8):
    ret = se.rolling(N, min_periods=1).quantile(qscore)
    return ret


@calc_by_symbol
def delay(se: pd.Series, periods=5):
    return se.shift(periods=periods)


@calc_by_symbol
def ma(se: pd.Series, periods=20):
    return se.rolling(window=periods).mean()


@calc_by_symbol
def mean(se: pd.Series, periods=20):
    return se.rolling(window=periods).mean()


@calc_by_symbol
def delta(se: pd.Series, periods=20):
    se_result = se - se.shift(periods=periods)
    return se_result


@calc_by_symbol
def ts_min(se: pd.Series, periods=5):
    return se.rolling(window=periods).min()


@calc_by_symbol
def ts_max(se: pd.Series, periods=5):
    return se.rolling(window=periods).max()


@calc_by_symbol
def ts_argmin(se: pd.Series, periods=5):
    return se.rolling(periods, min_periods=2).apply(lambda x: x.argmin())


@calc_by_symbol
def ts_argmax(se: pd.Series, periods=5):
    return se.rolling(periods, min_periods=2).apply(lambda x: x.argmax())


@calc_by_symbol
def stddev(se, periods=5):
    return se.rolling(window=periods).std()


@calc_by_symbol
def std(se, periods=5):
    return se.rolling(window=periods).std()


@calc_by_symbol
def ts_rank(se: pd.Series, periods=9):
    ret = se.rolling(window=periods).rank(pct=True)
    return ret


@calc_by_symbol
def sum(se: pd.Series, N):
    ret = se.rolling(N).sum()
    ret.name = 'sum_{}'.format(N)
    return ret


@calc_by_symbol
def shift(se: pd.Series, N):
    return se.shift(N)


@calc_by_symbol
def roc(se: pd.Series, N):
    return se / shift(se, N) - 1


@calc_by_symbol
def product(se: pd.Series, d):
    return se.rolling(window=d).apply(np.product)


'''

@calc_by_symbol
def zscore(se: pd.Series, N):
    def _zscore(x):

        try:
            x.dropna(inplace=True)
            #print('sub', x)
            value = (x[-1] - x.mean()) / x.std()
            if value:
                return value
        except:
            return -1

    #print(se)
    ret = se.rolling(window=N).apply(lambda x: _zscore(x))
    return ret


@calc_by_symbol
def scale(x, a=1):
    """
    Scales the array x such that the sum of the absolute values equals a.

    Parameters:
    x (array-like): The input array to be scaled.
    a (float, optional): The target sum of absolute values. Default is 1.

    Returns:
    numpy.ndarray: The scaled array.
    """
    import numpy as np
    x = np.array(x)  # 确保输入是numpy数组
    sum_abs_x = np.sum(np.abs(x))  # 计算x的绝对值之和
    if sum_abs_x == 0:
        raise ValueError("The sum of absolute values of x is zero, cannot scale by a non-zero value.")
    scale_factor = a / sum_abs_x  # 计算缩放因子
    return x * scale_factor  # 应用缩放因子


@calc_by_symbol
def decay_linear(series, window):
    """
    对输入的时间序列进行线性衰减。

    :param series: 输入的时间序列。
    :param window: 衰减的窗口大小。
    :return: 衰减后的序列。
    """
    weights = np.arange(1, window + 1)
    decay = np.convolve(series, weights, 'valid') / np.sum(weights)
    return decay


#@calc_by_symbol
#def signed_power(se: pd.Series, a):
#    return np.where(se < 0, -np.abs(se) ** a, np.abs(se) ** a)
'''
