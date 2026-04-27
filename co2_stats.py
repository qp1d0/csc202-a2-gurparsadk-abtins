import csv
from typing import *
from dataclasses import dataclass
import unittest
import math
import sys
sys.setrecursionlimit(10**6)


@dataclass (frozen=True)
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
@dataclass (frozen=True)
class RLNode:
    first: Row
    rest: RLNode

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
def answer_6(ll_Rows: RowList):
    pass

# China's electricity-and-heat emissions in 2070.
def answer_7(ll_Rows: RowList):
    pass


# EXAMPLES
# filter_ex1 = RLNode('' ) -> should be reading csv file


# TEST CASES
# (illegal test for filter)
class Tests(unittest.TestCase):
    # def test_filter_ValueError(self):
    #     self.assertRaises(filter(filter_ex1, 'country', 'less_than', 6509), ValueError)
      
    #     self.assertEqual(filter)


if (__name__ == '__main__'):
    unittest.main()