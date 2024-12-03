"""PythonGenePlague: 一个受到Plague Inc.游戏启发制作小Python游戏.

该代码用于症状对象的定义.
"""

from __future__ import annotations

import typing

if typing.TYPE_CHECKING:
    from .diseases import Disease


class SymptomNode:
    def __init__(self, symptom: Symptoms, parent=None):
        self.symptom = symptom
        self.parent = parent
        self.children = []

    def add_child(self, child_symptom: Symptoms):
        child_node = SymptomNode(child_symptom, self)
        self.children.append(child_node)
        return child_node

    def find_symptom(self, symptom_name: str) -> SymptomNode:
        if self.symptom.name == symptom_name:
            return self
        for child in self.children:
            result = child.find_symptom(symptom_name)
            if result:
                return result
        return None

    def print_tree(self, level: int = 0):
        print(
            " " * level * 2
            + f"- {self.symptom.name} (Evolved: {self.symptom.evolved})",
        )
        for child in self.children:
            child.print_tree(level + 1)


class SymptomsTree:
    def __init__(self):
        self.roots = []

    def add_root(self, root_symptom: Symptoms):
        root_node = SymptomNode(root_symptom)
        self.roots.append(root_node)
        return root_node

    def add_child(self, parent_name: str, child_symptom: Symptoms):
        parent_node = None
        for root in self.roots:
            parent_node = root.find_symptom(parent_name)
            if parent_node:
                break
        if not parent_node:
            msg = f"Parent symptom {parent_name} not found."
            raise ValueError(msg)
        return parent_node.add_child(child_symptom)

    def evolve_symptom(self, symptom_name: str, disease: Disease):
        for root in self.roots:
            symptom_node = root.find_symptom(symptom_name)
            if symptom_node:
                if symptom_node.parent and not symptom_node.parent.symptom.evolved:
                    msg = "Parent symptom must be evolved first."
                    raise ValueError(msg)
                symptom_node.symptom.evolve(disease)
                return
        msg = f"Symptom {symptom_name} not found."
        raise ValueError(msg)

    def print_tree(self):
        for root in self.roots:
            root.print_tree()


class Symptoms:
    _instances: typing.ClassVar = {}

    def __new__(cls, *args: typing.Any, **kwargs: typing.Any) -> typing.Self:
        # 相同的参数只会实例化一个对象
        key = (cls, args, tuple(sorted(kwargs.items())))
        if key not in cls._instances:
            instance = super().__new__(cls)
            cls._instances[key] = instance
        return cls._instances[key]

    def __init__(
        self,
        name: str,
        dna_point: int,
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
        infectivity: float = 0.0,  # 传染性
        severity: float = 0.0,  # 严重性
        lethality: float = 0.0,  # 致命性
    ) -> None:
        if not hasattr(self, "_initialized"):
            self.initialized = True
            self.name = name
            self.dna_point = dna_point
            self.mutation_multiplier = mutation_multiplier
            self.cure_resistance = cure_resistance
            self.base_cross_country_transmission = base_cross_country_transmission
            self.base_environmental_effectivity = base_environmental_effectivity
            self.environmental_conditions = environmental_conditions
            self.infectivity = infectivity
            self.severity = severity
            self.lethality = lethality
            self.evolved = False  # 已进化?
            self.locked = False  # 初始化为未锁定

    def lock(self):
        """锁定症状, 阻止其进化."""
        self.locked = True

    def unlock(self):
        """解锁症状, 允许其进化."""
        self.locked = False

    def evolve(self, disease: Disease):
        """使疾病性状进化."""
        if self.evolved or self.locked:
            return
        self.apply_effects(disease)
        self.evolved = True
