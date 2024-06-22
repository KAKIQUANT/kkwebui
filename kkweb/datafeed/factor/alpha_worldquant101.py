from datafeed.expr_functions import *


class AlphaBase:
    pass


# https://www.joinquant.com/data/dict/alpha101
class WorldQuant101(AlphaBase):
    def get_names_features(self):
        names = []
        features = []

        # names.append('alpha001')
        # features.append('(rank(ts_argmax(signed_power((stddev(returns, 20) if (returns < 0) else close), 2.), '
        #                '5)) - 0.5)')

        names.append('alpha002')
        features.append('(-1 * correlation(rank(delta(log(volume), 2)), rank(((close - open) / open)), 6))')

        names.append('alpha003')
        features.append('(-1 * correlation(rank(open), rank(volume), 10))')

        names.append('alpha004')
        features.append('(-1 * ts_rank(rank(low), 9))')

        '''
        Alpha#5: (rank((open - (sum(vwap, 10) / 10))) * (-1 * abs(rank((close - vwap))))) 
        Alpha#6: (-1 * correlation(open, volume, 10)) 
        '''

        names.append('alpha006')
        features.append('(-1 * correlation(open, volume, 10))')

        '''
        Alpha#7: ((adv20 < volume) ? ((-1 * ts_rank(abs(delta(close, 7)), 60)) * sign(delta(close, 7))) : (-1 * 1)) 
Alpha#8: (-1 * rank(((sum(open, 5) * sum(returns, 5)) - delay((sum(open, 5) * sum(returns, 5)), 10)))) 
        '''

        names.append('alpha008')
        features.append(
            '(-1 * rank(((sum(open, 5) * sum(returns, 5)) - delay((sum(open, 5) * sum(returns, 5)), 10))))')

        '''
        Alpha#11: ((rank(ts_max((vwap - close), 3)) + rank(ts_min((vwap - close), 3))) * rank(delta(volume, 3))) 
Alpha#12: (sign(delta(volume, 1)) * (-1 * delta(close, 1))) 
Alpha#13: (-1 * rank(covariance(rank(close), rank(volume), 5))) 
Alpha#14: ((-1 * rank(delta(returns, 3))) * correlation(open, volume, 10)) 
Alpha#15: (-1 * sum(rank(correlation(rank(high), rank(volume), 3)), 3)) 
        '''
        names.append('alpha012')
        features.append('(sign(delta(volume, 1)) * (-1 * delta(close, 1)))')

        names.append('alpha013')
        features.append('(-1 * rank(covariance(rank(close), rank(volume), 5))) ')

        names.append('alpha014')
        features.append('((-1 * rank(delta(returns, 3))) * correlation(open, volume, 10))')

        names.append('alpha015')
        features.append('(-1 * sum(rank(correlation(rank(high), rank(volume), 3)), 3))')

        '''
        Alpha#18: (-1 * rank(((stddev(abs((close - open)), 5) + (close - open)) + correlation(close, open, 10)))) 
Alpha#19: ((-1 * sign(((close - delay(close, 7)) + delta(close, 7)))) * (1 + rank((1 + sum(returns, 250))))) 
Alpha#20: (((-1 * rank((open - delay(high, 1)))) * rank((open - delay(close, 1)))) * rank((open - delay(low, 1)))) 
        '''
        names.append('alpha018')
        features.append('(-1 * rank(((stddev(abs((close - open)), 5) + (close - open)) + correlation(close, open, 10))))')

        names.append('alpha019')
        features.append(
            '((-1 * sign(((close - delay(close, 7)) + delta(close, 7)))) * (1 + rank((1 + sum(returns, 250)))))')

        names.append('alpha020')
        features.append(
            '(((-1 * rank((open - delay(high, 1)))) * rank((open - delay(close, 1)))) * rank((open - delay(low, 1))))')

        '''
        Alpha#22: (-1 * (delta(correlation(high, volume, 5), 5) * rank(stddev(close, 20))))
        Alpha#26: (-1 * ts_max(correlation(ts_rank(volume, 5), ts_rank(high, 5), 5), 3)) 
        Alpha#28: scale(((correlation(adv20, low, 5) + ((high + low) / 2)) - close)) 
        
        Alpha#29: (min(product(rank(rank(scale(log(sum(ts_min(rank(rank((-1 * rank(delta((close - 1), 5))))), 2), 1))))), 1), 5) + ts_rank(delay((-1 * returns), 6), 5)) 
Alpha#30: (((1.0 - rank(((sign((close - delay(close, 1))) + sign((delay(close, 1) - delay(close, 2)))) + sign((delay(close, 2) - delay(close, 3)))))) * sum(volume, 5)) / sum(volume, 20)) 

        '''
        names.append('alpha022')
        features.append(
            '(-1 * (delta(correlation(high, volume, 5), 5) * rank(stddev(close, 20))))')

        names.append('alpha026')
        features.append(
            '(-1 * ts_max(correlation(ts_rank(volume, 5), ts_rank(high, 5), 5), 3))')

        #names.append('alpha028')
        #features.append(
        #    'scale(((correlation(adv20, low, 5) + ((high + low) / 2)) - close))')

        names.append('alpha029')
        features.append(
            '(min(product(rank(rank(scale(log(sum(ts_min(rank(rank((-1 * rank(delta((close - 1), 5))))), 2), 1))))), 1), 5) + ts_rank(delay((-1 * returns), 6), 5))')

        names.append('alpha030')
        features.append('(((1.0 - rank(((sign((close - delay(close, 1))) + sign((delay(close, 1) - delay(close, 2)))) + sign((delay(close, 2) - delay(close, 3)))))) * sum(volume, 5)) / sum(volume, 20))')

        '''
        Alpha#31: ((rank(rank(rank(decay_linear((-1 * rank(rank(delta(close, 10)))), 10)))) + rank((-1 * delta(close, 3)))) + sign(scale(correlation(adv20, low, 12)))) 
Alpha#32: (scale(((sum(close, 7) / 7) - close)) + (20 * scale(correlation(vwap, delay(close, 5), 230)))) 
Alpha#33: rank((-1 * ((1 - (open / close))^1))) 
Alpha#34: rank(((1 - rank((stddev(returns, 2) / stddev(returns, 5)))) + (1 - rank(delta(close, 1))))) 
Alpha#35: ((Ts_Rank(volume, 32) * (1 - Ts_Rank(((close + high) - low), 16))) * (1 - Ts_Rank(returns, 32))) 
        '''

        names.append('alpha034')
        features.append(
            'rank(((1 - rank((stddev(returns, 2) / stddev(returns, 5)))) + (1 - rank(delta(close, 1)))))')

        names.append('alpha035')
        features.append(
            '((ts_rank(volume, 32) * (1 - ts_rank(((close + high) - low), 16))) * (1 - ts_rank(returns, 32)))')

        '''
        Alpha#36: (((((2.21 * rank(correlation((close - open), delay(volume, 1), 15))) + (0.7 * rank((open - close)))) + (0.73 * rank(Ts_Rank(delay((-1 * returns), 6), 5)))) + rank(abs(correlation(vwap, adv20, 6)))) + (0.6 * rank((((sum(close, 200) / 200) - open) * (close - open))))) 
Alpha#37: (rank(correlation(delay((open - close), 1), close, 200)) + rank((open - close))) 
Alpha#38: ((-1 * rank(Ts_Rank(close, 10))) * rank((close / open))) 
Alpha#39: ((-1 * rank((delta(close, 7) * (1 - rank(decay_linear((volume / adv20), 9)))))) * (1 + rank(sum(returns, 250)))) 
Alpha#40: ((-1 * rank(stddev(high, 10))) * correlation(high, volume, 10)) 
        '''

        names.append('alpha037')
        features.append(
            '(rank(correlation(delay((open - close), 1), close, 200)) + rank((open - close)))')

        names.append('alpha038')
        features.append(
            '((-1 * rank(ts_rank(close, 10))) * rank((close / open)))')

        names.append('alpha040')
        features.append(
            '((-1 * rank(stddev(high, 10))) * correlation(high, volume, 10))')

        '''
        Alpha#44: (-1 * correlation(high, rank(volume), 5)) 
Alpha#45: (-1 * ((rank((sum(delay(close, 5), 20) / 20)) * correlation(close, volume, 2)) * rank(correlation(sum(close, 5), sum(close, 20), 2)))) 
        '''

        names.append('alpha044')
        features.append(
            '(-1 * correlation(high, rank(volume), 5))')

        names.append('alpha045')
        features.append(
            '(-1 * ((rank((sum(delay(close, 5), 20) / 20)) * correlation(close, volume, 2)) * rank(correlation(sum(close, 5), sum(close, 20), 2))))')

        '''
        Alpha#52: ((((-1 * ts_min(low, 5)) + delay(ts_min(low, 5), 5)) * rank(((sum(returns, 240) - sum(returns, 20)) / 220))) * ts_rank(volume, 5)) 
Alpha#53: (-1 * delta((((close - low) - (high - close)) / (close - low)), 9)) 
Alpha#54: ((-1 * ((low - close) * (open^5))) / ((low - high) * (close^5))) 
Alpha#55: (-1 * correlation(rank(((close - ts_min(low, 12)) / (ts_max(high, 12) - ts_min(low, 12)))), rank(volume), 6)) 
Alpha#60: (0 - (1 * ((2 * scale(rank(((((close - low) - (high - close)) / (high - low)) * volume)))) - scale(rank(ts_argmax(close, 10)))))) 
        '''

        names.append('alpha052')
        features.append(
            '((((-1 * ts_min(low, 5)) + delay(ts_min(low, 5), 5)) * rank(((sum(returns, 240) - sum(returns, 20)) / 220))) * ts_rank(volume, 5))')

        names.append('alpha053')
        features.append(
            '(-1 * delta((((close - low) - (high - close)) / (close - low)), 9))')

        names.append('alpha055')
        features.append(
            '(-1 * correlation(rank(((close - ts_min(low, 12)) / (ts_max(high, 12) - ts_min(low, 12)))), rank(volume), 6))')

        names.append('alpha060')
        features.append('(0 - (1 * ((2 * scale(rank(((((close - low) - (high - close)) / (high - low)) * volume)))) - scale(rank(ts_argmax(close, 10))))))')

        names.append('alpha101')
        features.append('((close - open) / ((high - low) + .001))')
        return names, features


if __name__ == '__main__':
    from config import DATA_DIR
    from datafeed.expr import calc_expr

    names, features = WorldQuant101().get_names_features()
    name = names[-1]
    feature = features[-1]

    dfs = []
    for s in ['159915.SZ', '159920.SZ', '159934.SZ', '159967.SZ', '510050.SH', '510300.SH', '510500.SH', '510880.SH',
              '512100.SH', '513100.SH']:
        df = pd.read_csv(DATA_DIR.joinpath('universe').joinpath('20240415').joinpath('{}.csv'.format(s)).resolve())
        dfs.append(df)
    df_all = pd.concat(dfs)
    df_all.set_index(['date', 'symbol'], inplace=True)
    df_all.dropna(inplace=True)
    df_all.sort_index(level=0, inplace=True)
    df_all['returns'] = calc_expr(df_all, 'close/delay(close,1)-1')

    print(df_all)
    df_all[name] = calc_expr(df_all, feature)

    print(df_all)
