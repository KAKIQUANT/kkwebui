from abc import abstractmethod, ABCMeta
from collections import namedtuple
from enum import IntEnum
from typing import Type, List


class FeatureType(IntEnum):
    OPEN = 0
    CLOSE = 1
    HIGH = 2
    LOW = 3
    VOLUME = 4
    VWAP = 5


class SequenceIndicatorType(IntEnum):
    BEG = 0
    SEP = 1


class Token:
    def __repr__(self):
        return str(self)

    def is_featured(self):
        return False


class ConstantToken(Token):
    def __init__(self, constant: float) -> None:
        self.constant = constant

    def __str__(self): return str(self.constant)


class DeltaTimeToken(Token):
    def __init__(self, delta_time: int) -> None:
        self.delta_time = delta_time

    def __str__(self): return str(self.delta_time)

    def is_featured(self):
        return False


class FeatureToken(Token):
    def __init__(self, feature: FeatureType) -> None:
        self.feature = feature

    def __str__(self): return self.feature.name.lower()

    def is_featured(self):
        return True


class OperatorToken(Token):
    def __init__(self, func) -> None:
        self.func = func
        self.children = []

    def __str__(self):
        args = [str(c) for c in self.children]
        return '{}({})'.format(self.func.__name__, ','.join(args))

    def is_featured(self):
        return True

    def add_children(self, children: list[Token]):
        self.children = children


class UnaryOpsToken(OperatorToken):
    def n_args(self): return 1


class UnaryRollingOpsToken(OperatorToken):
    def n_args(self): return 2


class BinaryOpsToken(OperatorToken):
    def n_args(self): return 2


class BinaryRollingOpsToken(OperatorToken):
    def n_args(self): return 3


class SequenceIndicatorToken(Token):
    def __init__(self, indicator: SequenceIndicatorType) -> None:
        self.indicator = indicator

    def __str__(self): return self.indicator.name

    def is_featured(self):
        return False


BEG_TOKEN = SequenceIndicatorToken(SequenceIndicatorType.BEG)
SEP_TOKEN = SequenceIndicatorToken(SequenceIndicatorType.SEP)

GenericOperator = namedtuple('GenericOperator', ['name', 'function', 'arity'])
from datafeed.expr_functions import *


def get_funcs():
    funcs: List[GenericOperator] = []
    for op in unary_funcs:
        funcs.append(GenericOperator(function=UnaryOpsToken(op), name=op.__name__, arity=1))
    for op in binary_funcs:
        funcs.append(GenericOperator(function=BinaryOpsToken(op), name=op.__name__, arity=2))
    for op in unary_rolling_funcs:
        for day in [10, 20, 30, 40, 50]:
            funcs.append(GenericOperator(function=UnaryRollingOpsToken(op, day), name=op.__name__ + str(day), arity=1))
    for op in binary_roilling_funcs:
        for day in [10, 20, 30, 40, 50]:
            funcs.append(GenericOperator(function=BinaryRollingOpsToken(op, day), name=op.__name__ + str(day), arity=2))


if __name__ == '__main__':
    pass
    #get_funcs()
