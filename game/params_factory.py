"""PythonGenePlague: 一个受到Plague Inc.游戏启发制作小Python游戏.

此代码用于定义一个默认函数参数的工厂类.
"""

import typing

from .gene_codes import GeneCode
from .rate import (
    PctWithSelfStddevNonLinearDecayNoNeg,
    PctWithStddev,
    PctWithStddevNonLinearDecayNoNeg,
)


class ParamsFactory:
    def __init__(self, kwargs: dict) -> None:
        self.kwargs = kwargs

    def __iter__(self) -> iter:
        return iter(self.kwargs.items())

    def __getitem__(self, key) -> object:
        return self.kwargs[key]

    def keys(self):
        return self.kwargs.keys()

    def values(self):
        return self.kwargs.values()

    def items(self):
        return self.kwargs.items()

    def get(self, key: typing.Hashable, default: typing.Any) -> object:
        return self.kwargs.get(key, default)

    @classmethod
    def get_default_symptoms_params(cls) -> typing.Mapping:
        return cls(
            {
                "mutation_multiplier": 0.0,
                "cure_resistance": 0.0,
                "base_cross_country_transmission": {
                    "Air": 0,
                    "Sea": 0,
                    "Land": 0,
                },
                "base_environmental_effectivity": {
                    "Rich": 0,
                    "Poor": 0,
                    "Urban": 0,
                    "Rural": 0,
                },
                "environmental_conditions": {
                    "Hot": 0.0,
                    "Cold": 0.0,
                    "Humid": 0.0,
                    "Arid": 0.0,
                },
                "infectivity": 0.0,
                "severity": 0.0,
                "lethality": 0.0,
            },
        )

    @classmethod
    def get_default_gene_code_params(cls) -> typing.Mapping:
        return cls(
            {
                "mutation_multiplier": 0.0,
                "cure_resistance": 0.0,
                "base_cross_country_transmission": {
                    "Air": 0,
                    "Sea": 0,
                    "Land": 0,
                },
                "base_environmental_effectivity": {
                    "Rich": 0,
                    "Poor": 0,
                    "Urban": 0,
                    "Rural": 0,
                },
                "environmental_conditions": {
                    "Hot": 0.0,
                    "Cold": 0.0,
                    "Humid": 0.0,
                    "Arid": 0.0,
                },
                "other_world_modifys": {},
                "other_disease_modifys": {},
            },
        )

    @classmethod
    def get_default_world_params(cls) -> typing.Mapping:
        return cls(
            {
                "cure_required_money": 3000000,
                "cure_importance": 0,
                "cure_investment": 0,
            },
        )

    @classmethod
    def get_default_country_params(cls) -> typing.Mapping:
        return cls(
            {
                "density": 1.0,
                "wealth": 1.0,
                "cure_budget": 1000000,
                "environmental_conditions": {
                    "Hot": False,
                    "Cold": False,
                    "Humid": False,
                    "Arid": False,
                },
                "global_importance": 1.0,
            },
        )

    @classmethod
    def get_default_disease_params(cls) -> typing.Mapping:
        return cls(
            {
                "infectivity": PctWithSelfStddevNonLinearDecayNoNeg(1, 30),
                "severity": PctWithStddev(1),
                "lethality": PctWithStddevNonLinearDecayNoNeg(0),
                "mutation_multiplier": PctWithStddev(50),
                "cure_resistance": PctWithStddev(0),
                "base_cross_country_transmission": {
                    "Air": 1,
                    "Sea": 1,
                    "Land": 1,
                },
                "base_environmental_effectivity": {
                    "Rich": 0,
                    "Poor": 1,
                    "Urban": 1,
                    "Rural": 1,
                },
                "environmental_conditions": {
                    "Hot": PctWithStddev(10),
                    "Cold": PctWithStddev(10),
                    "Humid": PctWithStddev(100),
                    "Arid": PctWithStddev(100),
                },
                "increase_speed": {
                    "Infectivity": PctWithStddev(10),
                    "Severity": PctWithStddev(10),
                    "Lethality": PctWithStddev(5),
                },
                "gene_codes": [
                    GeneCode(),
                    GeneCode(),
                    GeneCode(),
                    GeneCode(),
                    GeneCode(),
                ],
            },
        )
