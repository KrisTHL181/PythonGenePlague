"""PythonGenePlague: 一个受到Plague Inc.游戏启发制作小Python游戏.

该代码用于世界对象的定义.
"""

from __future__ import annotations

import typing

from .gene_codes import LongTermGeneCode
from .rate import random_boolean

if typing.TYPE_CHECKING:
    from .diseases import Disease


class World:
    def __init__(
        self,
        disease: Disease,  # 病原体
        countries: list[World.Country],  # 国家
        cure_required_money: int = 3000000,  # 解药研发所需总资金
        cure_importance: float = 0,  # 解药研发重视程度增量
        cure_investment: int = 0,  # 解药已有投入
    ) -> None:
        self.updater = World.Updater(self)
        self.disease = disease  # 病原体
        self.countries = countries  # 国家
        self.disease_detected = False  # 瘟疫是否已被世界发现
        self.time = 0  # 已经过的天数
        self.cure_money = 0  # 解药开发资金
        self.cure_required_money = cure_required_money  # 解药开发所需总资金
        self.total_population = self.__total_populations(countries)  # 世界总人数
        self.cure_importance = cure_importance  # 解药研发重视程度增量
        self.cure_investment = cure_investment  # 解药已有投入
        self.full_deathed = False  # 是否全部死去
        self.cure_finished = False  # 解药是否开发完成

    def total_infections(self) -> int:
        """统计总感染人数."""
        return sum(country.infected_population for country in self.countries)

    def total_deaths(self) -> int:
        """统计总死亡人数."""
        return sum(country.deathed_population for country in self.countries)

    @staticmethod
    def __total_populations(countries: list[Country]) -> int:
        return sum(country.population for country in countries)

    def update(self) -> int:
        """模拟每天更新."""
        self.time += 1  # 时间增加一天
        self.updater.update_infection()  # 更新感染人数
        self.updater.update_death()  # 更新死亡人数
        self.updater.update_cure()  # 更新解药研发进度
        self.updater.update_by_genecode()  # 根据基因代码更新
        self.updater.update_healing()
        self.updater._call_callbacks("on_update")

    def print_information(self) -> None:
        """打印世界信息."""
        print(f"时间: {self.time}天")
        print(f"总人数: {self.total_population}")
        print(f"解药开发资金: {self.cure_money}")
        print(f"解药开发所需总资金: {self.cure_required_money}")
        print(f"解药研发重视程度增量: {self.cure_importance}")
        for country in self.countries:
            print(f"{country.name} 已感染人数: {country.infected_population}")
            print(f"{country.name} 死亡总人数: {country.deathed_population}")


class Country:
    def __init__(
        self,
        name: str,  # 国家名称
        population: int,  # 人口规模
        density: float,  # 人口密度
        wealth: float,  # 财富
        cure_budget: int,  # 治疗研究资金预算
        environmental_conditions: dict[str, bool] = {
            "Hot": False,
            "Cold": False,
            "Humid": False,
            "Arid": False,
        },  # 环境条件
        global_importance: float = 1.0,  # 全球重要性因素
    ) -> None:
        self.name = name
        self.population = population
        self.density = density
        self.wealth = wealth
        self.environment = self.__validate_environmental_conditions(
            environmental_conditions,
        )
        self.global_importance = global_importance
        self.cure_budget = cure_budget
        self.infected_population = 0  # 已感染人数
        self.deathed_population = 0  # 死亡人数
        self.internal_infectivity = 1.0  # 国家内传播性
        self.internal_severity = 1.0  # 国家内严重性
        self.internal_lethality = 1.0  # 国家内致死性

    def __validate_environmental_conditions(
        self,
        conditions: dict[str, bool],
    ) -> dict[str, bool]:
        """确保环境条件中的'热'和'寒冷'不能同时存在."""
        if conditions["Hot"] and conditions["Cold"]:
            msg = "热和寒冷不能同时存在"
            raise ValueError(msg)
        if conditions["Humid"] and conditions["Arid"]:
            msg = "潮湿和干燥不能同时存在"
            raise ValueError(msg)
        return conditions


class Updater:
    def __init__(
        self,
        world: World,
        callbacks: dict[str, list[typing.Callable]] = {},  # 回调函数
    ) -> None:
        self.world = world
        self.callbacks = callbacks

    def register_callback(self, event: str, callback: typing.Callable) -> None:
        """注册回调函数."""
        if event in self.callbacks:
            self.callbacks[event].append(callback)
        else:
            self.callbacks[event] = [callback]

    def _call_callbacks(
        self,
        event: str,
        *args: typing.Any,
        **kwargs: typing.Any,
    ) -> None:
        """调用回调函数."""
        if event not in self.callbacks:
            return
        for callback in self.callbacks[event]:
            callback(self.world, *args, **kwargs)

    def update_infection(self) -> None:
        """更新每天感染人数."""
        for country in self.world.countries:
            # 根据国家的环境数据和病原体的数据来计算感染率
            infection_rate = (
                self.world.disease.infectivity.value * country.internal_infectivity
            )
            for key, value in country.environment.items():
                if value:
                    infection_rate *= (
                        1 + self.world.disease.environmental_conditions[key].value
                    )
            infections = round(infection_rate * country.population * country.density)
            if infections > 0:
                country.infected_population += infections
                # 检查感染人数是否超过总人数
                country.infected_population = min(
                    country.infected_population,
                    country.population,
                )
                # 确保感染者和死亡者的和不超过总人数
                if (
                    country.infected_population + country.deathed_population
                    > country.population
                ):
                    country.infected_population = (
                        country.population - country.deathed_population
                    )

    def update_death(self) -> None:
        """更新每天死亡人数."""
        for country in self.world.countries:
            # 根据国家的财富、全球重要性等因素和病原体的致命性来计算死亡率
            death_rate = self.world.disease.lethality.value * country.internal_lethality
            death_rate *= 1 - country.wealth * 0.01
            death_rate *= 1 - country.global_importance * 0.01
            deaths = round(death_rate * country.infected_population)
            if deaths < 1 and country.infected_population > 0:
                deaths = country.infected_population
            country.infected_population -= deaths
            country.deathed_population += deaths

            country.infected_population = max(country.infected_population, 0)

            country.deathed_population = min(
                country.deathed_population,
                country.population,
            )
            if (
                country.infected_population + country.deathed_population
                > country.population
            ):
                country.deathed_population = min(
                    country.deathed_population,
                    country.population,
                )
                country.infected_population = (
                    country.population - country.deathed_population
                )
            if self.world.total_population - self.world.total_deaths() <= 0:
                self._call_callbacks("full_deathed")
                self.world.full_deathed = True

    def update_cure(self) -> None:
        """更新解药研发进度."""
        if self.world.full_deathed:
            return
        if not self.world.disease_detected and random_boolean(
            self.world.disease.severity,
        ):
            self._call_callbacks("disease_detected")
            self.world.disease_detected = True
        if self.world.disease_detected:
            base_cure = (self.world.cure_importance + 1) + (
                1 + self.world.cure_investment
            )
            base_cure *= 1 - self.world.disease.cure_resistance.pct_to_float()
            self.world.cure_money += base_cure * max(1.01, self.world.cure_importance)
            self.world.cure_required_money += round(
                self.world.disease.severity.pct_to_float() * 100,
            )
            self.world.cure_importance += self.world.disease.severity + abs(
                self.world.disease.lethality.apply_stddev(
                    self.world.disease.lethality.value,
                ),
            )
            if self.world.cure_money >= self.world.cure_required_money:
                self.world.cure_money = self.world.cure_required_money
                self.world.disease.infectivity.value = 0  # 将传播性设置为0
                self.world.disease.infectivity.stddev = 0  # 设置标准差为0(不再随机感染)
                self._call_callbacks("cure_finished")
                self.world.cure_finished = True

    def update_by_genecode(self) -> None:
        """根据长期效用基因代码更新数值."""
        for gene_code in self.world.disease.gene_codes:
            if isinstance(gene_code, LongTermGeneCode):
                gene_code.apply_effects(self.world)

    def update_healing(self) -> None:
        """更新每天治愈人数."""
        if self.world.cure_money >= self.world.cure_required_money:
            heal_rate = 0.25  # 每天治愈25%的感染者
            for country in self.world.countries:
                healed = round(country.infected_population * heal_rate)
                if healed < 1 and country.infected_population > 0:
                    healed = country.infected_population
                country.infected_population -= healed
                country.infected_population = max(country.infected_population, 0)
            if self.world.total_infections() <= 0:
                self._call_callbacks("full_healthed")
