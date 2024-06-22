import pandas as pd

from .expr_functions import *


def expr_transform(df, expr):
    # close/shift(close,5) -1
    for col in df.columns:
        expr = expr.replace(col, 'df["{}"]'.format(col))
    return expr


def calc_expr(df: pd.DataFrame, expr: str):  # correlation(rank(open),rank(volume))
    # 列若存在，就直接返回
    if expr in list(df.columns):
        return df[expr]

    expr = expr_transform(df, expr)

    try:
    #print('计算',expr)
        se = eval(expr)
        return se
    except:
        import traceback
        print(expr)
        traceback.print_exc()
    # raise NameError('{}——eval异常'.format(expr))
    # shift(close,1) -> shift(df['close'],1)
    return None
