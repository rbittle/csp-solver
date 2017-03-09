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
        # variables is an dictionary, where
        # key = variable name
        # value = array of possible values
        #
        # for example, a key/value pair might be
        # "B": [1,2,3,4]

        self.constraints = parse_con(con)
        # constraints is an array of tuples, where
        # the first value in a tuple is a tuple of values the constraint applies to,
        # the second value is an anonymous function that takes two variables and returns a boolean
        #
        # for example, an item in the array might be
        # (("A","B"), lambda a,b: a>b)

        self.fc = ce
        # fc is a boolean that tracks whether or not to use forward checking.

    def solve(self):
        print(self.constraints)


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
    constraints = []

    for constraint_line in con_file.readlines():
        constraint_line = constraint_line.strip()

        con_arr = constraint_line.split(" ")
        # split the line into the three parts
        var1, eq, var2 = con_arr[0], con_arr[1], con_arr[2]

        # construct a tuple representing the constraint and add it to the list
        if   eq == "=":
            constraints.append(((var1,var2), lambda a,b: a==b))
        elif eq == "!":
            constraints.append(((var1,var2), lambda a,b: a!=b))
        elif eq == ">":
            constraints.append(((var1,var2), lambda a,b: a>b))
        elif eq == "<":
            constraints.append(((var1,var2), lambda a,b: a<b))
        else:
            raise Exception("Unknown operator in constraint file.", eq)

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
