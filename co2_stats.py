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

# 'country' filed should only be comparable using 'equal' compare_type.
# Numerical measurement fields of CO2 emissions only compared using 'less_than' 
# - and 'greater_than' compare_type

# 3 ways: Return all of the rows where a given field is present:
# - 1) and is less than a specified value.
# - 2) and is equal to a specified value.
# - 3) and is greater than a specified value.

'''field_name should be chosen from strs in first line of CSV file -> read from csv file funtion(?)'''
# make clear in purpose statement about diff types for compare_val
# maybe dont use helper functions??
# single filter function with ..yeah


# Filter's through csv file data and returns all the rows where a given field is 
# present and either less than a specified value, equal to a specified value,
# or greater than a specified value. 

field_names = Literal['country', 'year', 'electricity_and_heat_co2_emissions', 
                      'electricity_and_heat_co2_emissions_per_capita',
                      'energy_co2_emissions', 'energy_co2_emissions_per_capita',
                      'total_co2_emissions_excluding_lucf',
                      'total_co2_emissions_excluding_lucf_per_capita']

def filter(ll_rows: RowList, field_name: field_names, 
           compare_type: Literal['less_than', 'equal', 'greater_than'], 
           compare_val: Union[int, float, str])-> RowList:
    
    if ll_rows is None:
        return  None
    
    val = getattr(ll_rows.first, field_name)
    
    if val is None:
        return filter(ll_rows.rest, field_name, compare_type, compare_val)
    
    match compare_type:
        case 'equal':
            if val == compare_val:
                return RLNode(ll_rows.first, filter(ll_rows.rest, field_name, compare_type,
                                                compare_val))
            else:
                return filter(ll_rows.rest, field_name, compare_type,
                                                compare_val)
                
        case "less_than":
            if field_name != 'country' and val < compare_val:
                return RLNode(ll_rows.first, filter(ll_rows.rest, field_name, compare_type, 
                                                compare_val))
            elif field_name == 'country':
                raise ValueError
            return filter(ll_rows.rest, field_name, compare_type, compare_val)
       
        case "greater_than":
            if field_name != 'country' and val > compare_val:
                return RLNode(ll_rows.first, filter(ll_rows.rest, field_name, compare_type, 
                                                    compare_val))
            elif field_name == 'country':
                raise ValueError
            return filter(ll_rows.rest, field_name, compare_type, compare_val)
    raise ValueError

# SOME QUESTIONS (No Test Cases Needed)
# Must use 'listlen' and 'filter' to produce an answer.

# Number of countries listed in 'll_Rows'.
def answer_1(ll_Rows: RowList):
    pass

# Years represented in 'll_Rows' for Mexico.
def answer_2(ll_Rows_Mex: RowList) -> RowList:
    pass

# Countries with higher per-capita total CO2 emissions (exclude lucf)
# - than US in 1990.
def answer_3(ll_Rows: RowList) -> RowList:
    pass

# Countries with higher per-capita total CO2 emissions (exclude lucf)
# - than US in 2020.
def answer_4(ll_Rows: RowList) -> RowList:
    pass

# Approximate opulation of Luxembourg in 2014 in people.
def answer_5(ll_Rows: RowList):
    pass

# Increase in total electricity-and-heat emissions in China from 
# - 1990 to 2020 in multiplier terms.
def answer_6(ll: RowList) -> float:
    china = filter(ll, 'country', 'equal', 'China')
        val_1990 = filter(china, 'year', 'equal', 1990).first.electricity_and_heat_co2_emissions
        val_2020 = filter(china, 'year', 'equal', 2020).first.electricity_and_heat_co2_emissions
        return val_2020 / val_1990

# China's electricity-and-heat emissions in 2070.
def answer_7(ll: RowList) -> float:
     china = filter(ll, 'country', 'equal', 'China')
        val_2020 = filter(china, 'year', 'equal', 2020).first.electricity_and_heat_co2_emissions
        annual_rate = answer_6(ll) ** (1 / 30)
        return val_2020 * (annual_rate ** 50)

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


# TEST CASES
# (illegal test for filter)
class Tests(unittest.TestCase):
    def test_filter_ValueError(self):
        lines : list[Row] = read_csv_lines('sample-file.csv')
        self.assertRaises(ValueError, filter, lines, 'country', 'less_than', 6509 )

    def test_filter_equal(self):
        lines : list[Row] = read_csv_lines('sample-file.csv')
        equal_ans = RLNode(Row('Lithuania',2002,5.33,1.5160139,10.93,3.108824,11.22,3.1913087
                            ), None)
        self.assertEqual(filter(lines, 'year', 'equal', 2002), equal_ans)

    def test_filter_less_than(self):
        lines : list[Row] = read_csv_lines('sample-file.csv')
        equal_ans = RLNode(Row('Lithuania',2003,5.24,1.5102245,10.94,3.1530259,11.23,3.2366068), 
                        RLNode(Row('Lithuania',2002,5.33,1.5160139,10.93,3.108824,11.22,3.1913087),
                            RLNode(Row('Lithuania',2001,5.53,1.5533075,10.87,3.0532465,11.16,3.1347039),
                                RLNode(Row('Lithuania',2000,5.07,1.4084746,10.22,2.8391736,10.52,2.9225154),
                                    None))))
        self.assertEqual(filter(lines, 'electricity_and_heat_co2_emissions', 'less_than', 6.05), equal_ans)

    def test_filter_greater_than(self):
        lines : list[Row] = read_csv_lines('sample-file.csv')
        equal_ans = RLNode(Row('Lithuania',1998,7.49,2.0433695,14.29,3.8984983,14.71,4.0130796),
                        RLNode(Row('Lithuania',1997,6.65,1.7997795,13.56,3.6699264,13.92,3.767358),
                            RLNode(Row('Lithuania',1996,7.11,1.9102515,13.92,3.7399015,14.24,3.8258765),
                                RLNode(Row('Lithuania',1994,7.27,1.9281462,14.44,3.8297703,14.82,3.930554), 
                                    None))))
        self.assertEqual(filter(lines, 'energy_co2_emissions', 'greater_than', 13.50), equal_ans)
      

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