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
    rest: RowList

EXPECTED_LABELS = ['country', 'year', 'electricity_and_heat_co2_emissions',
                   'electricity_and_heat_co2_emissions_per_capita',
                   'energy_co2_emissions', 'energy_co2_emissions_per_capita',
                   'total_co2_emissions_excluding_lucf',
                   'total_co2_emissions_excluding_lucf_per_capita']

#Converts a list of strings (one CSV line) into a Row.
#Numeric fields that are empty strings become None.
def list_to_row(line: List[str]) -> Row:
    def parse_float(s: str) -> Union[float, None]:
        if s == '':
            return None
        return float(s)
    return Row(
        country=line[0],
        year=int(line[1]),
        electricity_and_heat_co2_emissions=parse_float(line[2]),
        electricity_and_heat_co2_emissions_per_capita=parse_float(line[3]),
        energy_co2_emissions=parse_float(line[4]),
        energy_co2_emissions_per_capita=parse_float(line[5]),
        total_co2_emissions_excluding_lucf=parse_float(line[6]),
        total_co2_emissions_excluding_lucf_per_capita=parse_float(line[7])
    )

#Accepts a CSV filename and returns a linked list of Rows.
#Raises ValueError if the header line doesn't match expected labels.
def read_csv_lines(filename: str) -> RowList:
    with open(filename, newline='') as csvfile:
        iter = csv.reader(csvfile)
        topline: List[str] = next(iter)
        if topline != EXPECTED_LABELS:
            raise ValueError(f"unexpected first line: got: {topline}")
        result: RowList = None
        for line in iter:
            result = RLNode(list_to_row(line), result)
    return result

#Returns the length of a linked list of Rows.
def listlen(ll: RowList) -> int:
    if ll is None:
        return 0
    return 1 + listlen(ll.rest)

class Tests(unittest.TestCase):
    def test_list_to_row_full(self):
        line = ['USA', '2000', '1.5', '0.5', '2.0', '0.7', '3.0', '1.1']
        row = list_to_row(line)
        self.assertEqual(row.country, 'USA')
        self.assertEqual(row.year, 2000)
        self.assertEqual(row.electricity_and_heat_co2_emissions, 1.5)
        self.assertEqual(row.energy_co2_emissions_per_capita, 0.7)

    def test_list_to_row_missing(self):
        line = ['Andorra', '1990', '', '', '0.5', '0.2', '0.6', '0.3']
        row = list_to_row(line)
        self.assertIsNone(row.electricity_and_heat_co2_emissions)
        self.assertIsNone(row.electricity_and_heat_co2_emissions_per_capita)

    def test_read_csv_lines_returns_rlnode(self):
        result = read_csv_lines('sample-file.csv')
        self.assertIsInstance(result, RLNode)
        
    def test_listlen_empty(self):
        self.assertEqual(listlen(None), 0)

    def test_listlen_nonempty(self):
        row = Row('USA', 2000, 1.5, 0.5, 2.0, 0.7, 3.0, 1.1)
        ll = RLNode(row, RLNode(row, None))
        self.assertEqual(listlen(ll), 2)

if (__name__ == '__main__'):
    unittest.main()