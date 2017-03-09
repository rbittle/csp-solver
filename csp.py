#! /usr/bin/python3

import argparse
import re

parser = argparse.ArgumentParser()

parser.add_argument("var", action="store", help="Name of the variables file used.")
parser.add_argument("con", action="store", help="Name of the constrains file used.")
parser.add_argument("consistency", action="store", help="Consistency-enforcing procedure. Either fc or none.")

args = parser.parse_args()


class CSPsolver:

    def __init__(self, var, con, ce):
        self.variables = parse_vars(var)
        self.constraints = parse_con(con)
        self.fc = ce

    def solve(self):
        print(self.variables)


def parse_vars(var_file):
    '''Converts the input file into a dictionary, where
    the key is the variable name and the value is an array
    of possible values.
    '''

    variables = {}

    for variable_line in var_file.readlines():
        variable_line = variable_line.strip()

        # split the line into variable and possible values, which are seperated by ":"
        single_arr = variable_line.split(":")

        # variable name is first instance of the array, character(s) before the ":" symbol
        variable = single_arr[0].strip()

        # hande possible values
        values_arr = []
        for value in single_arr[1].strip().split(" "):
            values_arr.append(int(value))

        variables[variable] = values_arr

    return variables

def parse_con(con_file):
    constraints = {}

    for constraint_line in con_file.readlines():
        constraint_line = constraint_line.strip()


    return constraints


if __name__ == "__main__":
    try:
        var = open(args.var, "r")
        con = open(args.con, "r")
        ce  = True if args.consistency == "fc" else False

        problem = CSPsolver(var, con, ce)
        problem.solve()

    except Exception as e:
        print(e)
    finally:
        pass
