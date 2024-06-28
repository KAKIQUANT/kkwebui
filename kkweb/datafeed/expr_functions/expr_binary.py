import pandas as pd
import numpy as np

from .expr_utils import calc_by_symbol


@calc_by_symbol
def greater(left, right):
    return np.maximum(left, right)

@calc_by_symbol
def less(left, right):
    return np.minimum(left, right)
'''

@calc_by_symbol
def cross_up(left, right):
    left = pd.Series(left)
    right = pd.Series(right)
    diff = left - right
    diff_shift = diff.shift(1)
    se = (diff >= 0) & (diff_shift < 0)
    return se


@calc_by_symbol
def cross_down(left, right):
    left = pd.Series(left)
    right = pd.Series(right)
    diff = left - right
    diff_shift = diff.shift(1)
    return (diff <= 0) & (diff_shift > 0)


@calc_by_symbol
def calc_signal(long: pd.Series, exit: pd.Series):
    long.name = 'signal_long'
    exit.name = 'signal_exit'
    df = pd.concat([long, exit], axis=1)
    print(df)
    df['signal'] = np.where(df['signal_long'], 1, np.nan)
    df['signal'] = np.where(df['signal_exit'], 0, df['signal'])
    df['signal'] = df['signal'].ffill()
    df['signal'] = df['signal'].fillna(0)
    print(df['signal'])
    return df['signal']
'''
