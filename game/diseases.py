"""PythonGenePlague: 一个受到Plague Inc.游戏启发制作小Python游戏.

该代码用于病原体的定义.
"""

# TODO: IncreaseSpeed
# TODO: Symptons连接前端, 减去dna-point

from __future__ import annotations

from .gene_codes import GeneCode
from .rate import (
    PctWithSelfStddevNonLinearDecayNoNeg,
    PctWithStddev,
    PctWithStddevNonLinearDecayNoNeg,
)


class Disease:
    """基本的瘟疫类型."""

    def __init__(
        self,
        name: str,  # 病原体名称
        infectivity: PctWithSelfStddevNonLinearDecayNoNeg = PctWithSelfStddevNonLinearDecayNoNeg(
            1,
            30,
        ),  # 传染性
        severity: PctWithStddev = PctWithStddev(1),  # 严重性
        lethality: PctWithStddevNonLinearDecayNoNeg = PctWithStddevNonLinearDecayNoNeg(
            0,
        ),  # 致命性
        mutation_multiplier: PctWithStddev = PctWithStddev(50),  # 突变乘数
        cure_resistance: PctWithStddev = PctWithStddev(0),  # 解药抗性
        base_cross_country_transmission: dict[str, int] = {
            "Air": 1,
            "Sea": 1,
            "Land": 1,
        },  # 基础跨国传播能力
        base_environmental_effectivity: dict[str, int] = {
            "Rich": 0,
            "Poor": 1,
            "Urban": 1,
            "Rural": 1,
        },  # 基础环境适应性
        environmental_conditions: dict[str, PctWithStddev] = {
            "Hot": PctWithStddev(10),
            "Cold": PctWithStddev(10),
            "Humid": PctWithStddev(100),
            "Arid": PctWithStddev(100),
        },  # 环境条件
        increase_speed: dict[str, PctWithStddev] = {
            "Infectivity": PctWithStddev(10),
            "Severity": PctWithStddev(10),
            "Lethality": PctWithStddev(5),
        },  # 传播速度增加
        gene_codes: list[GeneCode] = [
            GeneCode,
            GeneCode,
            GeneCode,
            GeneCode,
            GeneCode,
        ],  # 基因代码
    ) -> None:
        self.name = name
        self.infectivity = infectivity
        self.severity = severity
        self.lethality = lethality
        self.mutation_multiplier = mutation_multiplier
        self.cure_resistance = cure_resistance
        self.base_cross_country_transmission = base_cross_country_transmission
        self.base_environmental_effectivity = base_environmental_effectivity
        self.environmental_conditions = environmental_conditions
        self.increase_speed = increase_speed
        self.gene_codes = gene_codes
        self.init()

    def init(self):
        # 应用基因代码
        for gene_code in self.gene_codes:
            if isinstance(gene_code, GeneCode):
                gene_code.apply_effects(self)
