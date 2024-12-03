"""PythonGenePlague: 一个受到Plague Inc.游戏启发制作小Python游戏.

该代码用于定义基因代码.
"""
from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from .diseases import Disease
    from .world import World


class GeneCode:
    def __init__(
        self,
        mutation_multiplier: float = 0.0,  # 突变乘数
        cure_resistance: float = 0.0,  # 解药抗性
        base_cross_country_transmission: dict[str, int] = {
            "Air": 0,
            "Sea": 0,
            "Land": 0,
        },  # 基础跨国传播能力
        base_environmental_effectivity: dict[str, int] = {
            "Rich": 0,
            "Poor": 0,
            "Urban": 0,
            "Rural": 0,
        },  # 基础环境适应性
        environmental_conditions: dict[str, float] = {
            "Hot": 0.0,
            "Cold": 0.0,
            "Humid": 0.0,
            "Arid": 0.0,
        },  # 环境条件
        other_disease_modifys: dict[str, typing.Callable] = {},  # 其他病原体修改
    ):
        self.mutation_multiplier = mutation_multiplier
        self.cure_resistance = cure_resistance
        self.base_cross_country_transmission = base_cross_country_transmission
        self.base_environmental_effectivity = base_environmental_effectivity
        self.environmental_conditions = environmental_conditions
        self.other_disease_modifys = other_disease_modifys

    def apply_effects(self, disease: Disease):
        """应用基因代码的效果到疾病上."""
        disease.mutation_multiplier.value += self.mutation_multiplier
        disease.cure_resistance.value += self.cure_resistance

        # 更新跨国传播能力
        for key in self.base_cross_country_transmission:
            disease.base_cross_country_transmission[
                key
            ] += self.base_cross_country_transmission[key]

        # 更新环境适应性
        for key in self.base_environmental_effectivity:
            disease.base_environmental_effectivity[
                key
            ] += self.base_environmental_effectivity[key]

        # 更新环境条件
        for key in self.environmental_conditions:
            disease.environmental_conditions[
                key
            ].value += self.environmental_conditions[key]

        # 设置其他病原体修改
        for key in self.other_disease_modifys:
            value = getattr(disease, key)
            setattr(
                disease,
                key,
                value + self.other_disease_modifys[key](value),
            )


class LongTermGeneCode:
    def __init__(self, modifys: dict[str, typing.Callable] = {}):  # 每次更新的修改
        self.modifys = modifys

    def apply_effects(self, world: World):
        """应用基因代码的效果到疾病上."""
        for key in self.modifys:
            setattr(world, key, self.modifys[key](world))
