"""该代码用于创建多个带有随机的百分比."""

import random


class PctBase:
    def __init__(self, value: int, stddev: float = 30) -> None:
        self.value = value / 100  # 将百分比转换为小数
        self.stddev = stddev

    def pct_to_float(self) -> float:
        """将百分比转换为浮点数."""
        return self.value

    def apply_stddev(self, value: float) -> float:
        """应用标准差, 返回波动后的值."""
        return random.gauss(value, self.stddev / 100)

    def __float__(self) -> float:
        return float(self.value)

    def __int__(self) -> int:
        return round(self.value)

    def __str__(self) -> str:
        return f"{self.value * 100:.2f}%"

    def __repr__(self) -> str:
        return (
            f"{self.__class__.__name__}({int(self.value * 100)}, stddev={self.stddev})"
        )

    def __add__(self, other: float) -> float:
        return (self.value + other)

    def __sub__(self, other: float) -> float:
        return (self.value - other)

    def __mul__(self, other: float) -> float:
        return (self.value * other)

    def __truediv__(self, other: float) -> float:
        if other == 0:
            msg = "除数不能为0"
            raise ValueError(msg)
        return (self.value / other)


class PctWithStddev(PctBase):
    def __add__(self, other: float) -> float:
        return self.apply_stddev(self.value + other)

    def __sub__(self, other: float) -> float:
        return self.apply_stddev(self.value - other)

    def __mul__(self, other: float) -> float:
        return self.apply_stddev(self.value * other)

    def __truediv__(self, other: float) -> float:
        if other == 0:
            msg = "除数不能为0"
            raise ValueError(msg)
        return self.apply_stddev(self.value / other)


class PctNoNeg(PctWithStddev):
    def apply_stddev(self, value: float) -> float:
        result = super().apply_stddev(value)
        return max(result, 0)


class PctNoNegSelfStddev(PctNoNeg):
    def __init__(self, value: int, stddev: float = 50) -> None:
        super().__init__(value, stddev / 50)

    def apply_stddev(self, value: float) -> float:
        result = random.gauss(value, random.gauss(self.value, self.stddev))
        return max(result, 0)


class PctWithStddevNonLinearDecay(PctWithStddev):
    def __init__(self, value: int, stddev: float = 30, decay_rate: float = 0.01):
        super().__init__(value, stddev)
        self.initial_stddev = stddev
        self.decay_rate = decay_rate

    def apply_stddev(self, value: float) -> float:
        result = super().apply_stddev(value)

        if self.stddev <= 0.05 * self.initial_stddev:
            self.decay_rate *= 0.8

        self.stddev -= self.decay_rate
        self.stddev = max(self.stddev, 0.001)
        self.decay_rate = max(self.decay_rate, 0.001)

        return result


class PctWithStddevNonLinearDecayNoNeg(PctWithStddevNonLinearDecay):
    def apply_stddev(self, value: float) -> float:
        result = super().apply_stddev(value)
        return max(result, 0)


class PctWithSelfStddevNonLinearDecayNoNeg(PctWithStddevNonLinearDecay):
    def apply_stddev(self, value: float) -> float:
        result = random.gauss(value, random.gauss(self.value, self.stddev))
        return max(result, 0)


def random_boolean(probability: float | PctBase):
    return random.random() < (
        probability
        if isinstance(probability, float | int)
        else probability.pct_to_float()
    )
