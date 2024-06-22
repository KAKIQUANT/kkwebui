from functools import wraps

import pandas as pd


def calc_by_date(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        other_args = []
        se_args = []
        se_names = []
        for arg in args:
            if type(arg) is not pd.Series:
                other_args.append(arg)
            else:
                se_args.append(arg)
                se_names.append(arg.name)
        if len(se_args) == 1:
            ret = se_args[0].groupby(level=0, group_keys=False).apply(lambda x: func(x, *other_args, **kwargs))
        elif len(se_args) > 1:
            count = len(se_args)
            df = pd.concat(se_args, axis=1)
            df.index = se_args[0].index
            ret = df.groupby(level=0, group_keys=False).apply(
                lambda sub_df: func(*[sub_df[name] for name in se_names], *other_args))
            ret.index = df.index
        else:
            print('len(args)==0', func)
        return ret

    return wrapper


def calc_by_symbol(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        other_args = []
        se_args = []
        se_names = []
        for i, arg in enumerate(args):
            if type(arg) is not pd.Series:
                other_args.append(arg)
            else:
                se_args.append(arg)
                if arg.name:
                    se_names.append(arg.name)
                else:
                    # print('func',func)
                    name = 'arg_{}'.format(i)
                    arg.name = name
                    se_names.append(name)
        if len(se_args) == 1:
            ret = se_args[0].groupby(level=1, group_keys=False).apply(lambda x: func(x, *other_args, **kwargs))
            ret.name = str(func) + se_names[0]
            if len(other_args):  # 这里的参数名，比如sum(close,5)，sum(close,10)，默认都是close，这是会命名为：sum_close_N
                ret.name += str(other_args[0])
        elif len(se_args) > 1:
            count = len(se_args)
            df = pd.concat(se_args, axis=1)
            df.index = se_args[0].index

            unique_level1 = df.index.get_level_values(1).unique()

            # 判断第一级索引是否只有一个元素
            if len(unique_level1) == 1:
                # print("第一级索引只有一个元素")
                ret = func(*[df[name] for name in se_names], *other_args)
            else:
                # print("第一级索引有多于一个元素")
                ret = df.groupby(level=1, group_keys=False).apply(
                    lambda sub_df: func(*[sub_df[name] for name in se_names], *other_args))
                ret.index = df.index
        else:
            print('errors:', len(se_args))
        return ret

    return wrapper
