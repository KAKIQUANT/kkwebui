import pandas as pd
import talib
from datafeed.expr_functions.expr_utils import calc_by_symbol

@calc_by_symbol
def bbands_up(close, timeperiod=20, nbdevup=2, nbdevdn=2):
    upper_band, middle_band, lower_band = talib.BBANDS(close, timeperiod=timeperiod, nbdevup=nbdevup, nbdevdn=nbdevdn)
    return upper_band

@calc_by_symbol
def bbands_down(close, timeperiod=20, nbdevup=2, nbdevdn=2):
    upper_band, middle_band, lower_band = talib.BBANDS(close, timeperiod=timeperiod, nbdevup=nbdevup, nbdevdn=nbdevdn)
    return lower_band


@calc_by_symbol
def ta_atr(high, low, close, period=14):
    se = talib.ATR(high, low, close, period)
    se = pd.Series(se)
    se.index = high.index
    return se


def _obv(close, volume):
    return talib.OBV(close, volume)


def ta_obv(close, volume):
    close.name = 'close'
    volume.name = 'volume'
    df = pd.concat([close, volume], axis=1)
    se = df.groupby('symbol', group_keys=False).apply(lambda sub_df: _obv(sub_df['close'], sub_df['volume']))
    if type(se) is pd.DataFrame:
        se = se.T
        se = se[se.columns[0]]
    return se
