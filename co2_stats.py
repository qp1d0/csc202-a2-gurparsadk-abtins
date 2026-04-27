import csv
from typing import *
from dataclasses import dataclass
import unittest
import math
import sys
sys.setrecursionlimit(10**6)

@dataclass(frozen=True)
class Row:
    country: str
    year: int
    electricity_and_heat_co2_emissions: Union[float, None]
    electricity_and_heat_co2_emissions_per_capita: Union[float, None]
    energy_co2_emissions: Union[float, None]
    energy_co2_emissions_per_capita: Union[float, None]
    total_co2_emissions_excluding_lucf: Union[float, None]
    total_co2_emissions_excluding_lucf_per_capita: Union[float, None]

RowList = Union[None, 'RLNode']

@dataclass(frozen=True)
class RLNode:
    first: Row
    rest: RLNode


class Tests(unittest.TestCase):
    pass




if (__name__ == '__main__'):
    unittest.main()