import numpy as np
import pandas as pd

from .expr_utils import *


@calc_by_symbol
def sign(se: pd.Series):
    return np.sign(se)


@calc_by_date
def rank(se: pd.Series):
    ret = se.rank(pct=True)
    return ret


@calc_by_symbol
def log(se: pd.Series):
    return np.log(se)


@calc_by_symbol
def abs(se):
    return np.abs(se)
