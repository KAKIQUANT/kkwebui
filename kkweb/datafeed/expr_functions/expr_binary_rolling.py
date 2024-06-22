import numpy as np
import pandas as pd
from .expr_utils import calc_by_symbol, calc_by_date


@calc_by_symbol
def correlation(left: pd.Series, right: pd.Series, periods=20):
    res = left.rolling(window=periods).corr(right)
    # left.rolling(window=periods).apply(func=func,right)
    res.loc[
        np.isclose(left.rolling(periods, min_periods=1).std(), 0, atol=2e-05)
        | np.isclose(right.rolling(periods, min_periods=1).std(), 0, atol=2e-05)
        ] = np.nan
    return res


@calc_by_symbol
def covariance(left: pd.Series, right: pd.Series, periods=10):
    res = left.rolling(window=periods).cov(right)
    return res


@calc_by_symbol
def slope_pair(se_left, se_right, N=18):
    slopes = []
    R2 = []
    # 计算斜率值
    for i in range(len(se_left)):
        if i < (N - 1):
            slopes.append(np.nan)
            R2.append(np.nan)
        else:
            x = se_right[i - N + 1:i + 1]
            y = se_left[i - N + 1:i + 1]
            slope, intercept = np.polyfit(x, y, 1)

            # lr = LinearRegression().fit(np.array(x).reshape(-1, 1), y)
            ## y_pred = lr.predict(x.reshape(-1, 1))
            # beta = lr.coef_[0]
            # r2 = r2_score(y, y_pred)
            #if slope is np.nan:
                #print(slope)
            slopes.append(slope)
            # R2.append(r2)
    slopes = pd.Series(slopes)
    slopes.index = se_left.index
    return slopes
