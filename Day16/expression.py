from enum import Enum
from dataclasses import dataclass, field
from functools import reduce
from typing import List


class PacketType(Enum):
    SUM = 0
    PRODUCT = 1
    MINIMUM = 2
    MAXIMUM = 3
    LITERAL = 4
    GREATER_THAN = 5
    LESS_THAN = 6
    EQUAL_TO = 7


@dataclass
class Expression:
    type: PacketType
    args: List = field(default_factory=list)

    def evaluate(self):
        match self.type:
            case PacketType.LITERAL:
                return self.args[-1]
            case PacketType.PRODUCT:
                return reduce(lambda curr, k: curr*k.evaluate(), self.args, 1)
            case PacketType.MINIMUM:
                return min(expr.evaluate() for expr in self.args)
            case PacketType.MAXIMUM:
                return max(expr.evaluate() for expr in self.args)
            case PacketType.SUM:
                return sum(expr.evaluate() for expr in self.args)
            case PacketType.GREATER_THAN:
                if len(self.args) != 2:
                    raise ValueError(f"Error while evaluating {self.type} ({len(self.args)} args), {self.args=}")
                return self.args[0].evaluate() > self.args[1].evaluate()
            case PacketType.LESS_THAN:
                if len(self.args) != 2:
                    raise ValueError(f"Error while evaluating {self.type} ({len(self.args)} args), {self.args=}")
                return self.args[0].evaluate() < self.args[1].evaluate()
            case PacketType.EQUAL_TO:
                if len(self.args) != 2:
                    raise ValueError(f"Error while evaluating {self.type} ({len(self.args)} args), {self.args=}")
                return self.args[0].evaluate() == self.args[1].evaluate()

    def __str__(self):
        match self.type:
            case PacketType.LITERAL:
                return f'{self.args[-1]}'
            case PacketType.PRODUCT:
                return f'({" * ".join(str(expr) for expr in self.args)})'
            case PacketType.MINIMUM:
                return f'min({", ".join(str(expr) for expr in self.args)})'
            case PacketType.MAXIMUM:
                return f'max({", ".join(str(expr) for expr in self.args)})'
            case PacketType.SUM:
                return f'({" + ".join(str(expr) for expr in self.args)})'
            case PacketType.GREATER_THAN:
                return f'({" > ".join(str(expr) for expr in self.args)})'
            case PacketType.LESS_THAN:
                return f'({" < ".join(str(expr) for expr in self.args)})'
            case PacketType.EQUAL_TO:
                return f'({" == ".join(str(expr) for expr in self.args)})'
