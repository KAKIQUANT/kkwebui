# from alphagen.data.expression import *
from typing import List

from datafeed.mining.tokens import *
from datafeed.expr_functions import *


class ExpressionBuilder:
    stack: List[Token]

    def __init__(self):
        self.stack = []

    def get_tree(self) -> Token:
        if len(self.stack) == 1:
            return self.stack[0]
        else:
            raise InvalidExpressionException(f"Expected only one tree, got {len(self.stack)}")

    def add_token(self, token: Token):
        if not self.validate(token):
            raise InvalidExpressionException(f"Token {token} not allowed here, stack: {self.stack}.")
        if isinstance(token, OperatorToken):
            n_args: int = token.n_args()
            children = []
            for _ in range(n_args):
                children.append(self.stack.pop())
                token.add_children(list(reversed(children)))
            self.stack.append(token)
        elif isinstance(token, ConstantToken):
            self.stack.append(token)
        elif isinstance(token, DeltaTimeToken):
            self.stack.append(token)
        elif isinstance(token, FeatureToken):
            self.stack.append(token)
        else:
            assert False

    def is_valid(self) -> bool:
        return len(self.stack) == 1 and self.stack[0].is_featured

    def validate(self, token: Token) -> bool:
        if isinstance(token, OperatorToken):
            return self.validate_op(token)
        elif isinstance(token, DeltaTimeToken):
            return self.validate_dt()
        elif isinstance(token, ConstantToken):
            return self.validate_const()
        elif isinstance(token, FeatureToken):
            return self.validate_feature()
        else:
            assert False

    def validate_op(self, op: Type[OperatorToken]) -> bool:
        if len(self.stack) < op.n_args():
            return False

        if isinstance(op, UnaryOpsToken):
            if not self.stack[-1].is_featured:
                return False
        elif isinstance(op, BinaryOpsToken):
            if not self.stack[-1].is_featured and not self.stack[-2].is_featured:
                return False
            if (isinstance(self.stack[-1], DeltaTimeToken) or
                    isinstance(self.stack[-2], DeltaTimeToken)):
                return False
        elif isinstance(op, UnaryRollingOpsToken):
            if not isinstance(self.stack[-1], DeltaTimeToken):
                return False
            if not self.stack[-2].is_featured:
                return False
        elif isinstance(op, BinaryRollingOpsToken):
            if not isinstance(self.stack[-1], DeltaTimeToken):
                return False
            if not self.stack[-2].is_featured or not self.stack[-3].is_featured:
                return False
        else:
            assert False
        return True

    def validate_dt(self) -> bool:
        return len(self.stack) > 0 and self.stack[-1].is_featured

    def validate_const(self) -> bool:
        return len(self.stack) == 0 or self.stack[-1].is_featured

    def validate_feature(self) -> bool:
        return not (len(self.stack) >= 1 and isinstance(self.stack[-1], DeltaTimeToken))


class InvalidExpressionException(ValueError):
    pass


if __name__ == '__main__':
    tokens = [
        FeatureToken(FeatureType.LOW),
        UnaryOpsToken(abs),
        DeltaTimeToken(10),
        UnaryRollingOpsToken(rank),
        FeatureToken(FeatureType.HIGH),
        FeatureToken(FeatureType.CLOSE),
        BinaryOpsToken(Div),
        BinaryOpsToken(Add),
    ]

    builder = ExpressionBuilder()
    for token in tokens:
        # print(token)
        builder.add_token(token)
        # print(builder.stack)
    print(f'系统生成: {str(builder.get_tree())}')
    print(f'参考结果: Add(rank(abs(low),10),Div(high,close))')
