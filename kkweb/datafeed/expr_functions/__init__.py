from collections import namedtuple

from .expr_unary import *
from .expr_binary import *
from .expr_unary_rolling import *
from .expr_binary_rolling import *
from .expr_funcs_talib import *
from .expr_others import *


def Sub(left, right):
    return left - right


def Add(left, right):
    return left + right


def Mul(left, right):
    return left * right


def Div(left, right):
    return left / right


def list_funcs(mod):
    import inspect
    funcs = []

    name_funcs = {name: func for name, func in inspect.getmembers(mod, inspect.isfunction)}

    for name, func in name_funcs.items():
        if name in ['calc_by_date', 'calc_by_symbol', 'wraps']:
            continue

        funcs.append(name)
    return funcs


unary_funcs = list_funcs(expr_unary)
binary_funcs = list_funcs(expr_binary)
unary_rolling_funcs = list_funcs(expr_unary_rolling)
binary_roilling_funcs = list_funcs(expr_binary_rolling)
