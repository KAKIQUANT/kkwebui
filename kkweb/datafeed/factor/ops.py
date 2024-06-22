import pandas as pd

from datafeed.expr_functions import calc_by_date


@calc_by_date
def cs_minmax(se: pd.Series):
    return (se - se.min()) / (se.max() - se.min())
