#! /usr/bin/python3

import argparse
import re
from queue import LifoQueue

# Command Line interface
parser = argparse.ArgumentParser()
parser.add_argument("var", action="store", help="Name of the variables file used.")
parser.add_argument("con", action="store", help="Name of the constrains file used.")
parser.add_argument("consistency", action="store", help="Consistency-enforcing procedure. Either fc or none.")
args = parser.parse_args()


class CSPsolver:

    def __init__(self, var, con, ce):
        self.variables, self.domains = parse_vars(var)
        # variables is an ordered tuple of variable names
        # ex: ("A", "B", "C")

        # domains is an dictionary, where
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

        self.checked = []
        # list of assignment states that have already been checked.

    def h_constrained(self, variables):
        '''Returns an array of tuples that get the current state of how constrained the values are.'''
        constrained = []
        # counts the number of possible values the number can have, and returns an array of tuples, where
        # (constrained order, value name), where constrained order is lower-is-better
        for variable in variables:
            value_count = len(self.domains[variable])
            constrained.append((value_count, variable))

        return sorted(constrained)

    def h_constraining(self, variables):
        '''Returns an array of tuples that gets the current state of how constraining each variable is.'''
        constraining = []

        for variable in variables:
            affects_count = 0
            # count the number of constraints each variable is a part of.
            for tup, funct in self.constraints:
                if variable in tup:
                    affects_count += 1

            constraining.append((affects_count, variable))
        # order by amount of constraints on other variables
        return sorted(constraining)

    def goal_test(self, assignments):
        '''Tests the set assignments to see if they fit as a solution.'''
        goal = False

        return goal

    def succ(self):
        '''Returns the next successor state(s?) using the variable and value selection heuristics.'''
        state = ()

        return state

    def propagate(self, assignments):
        '''Returns a dictionary of possible new assignments given the current set of constraints using forward propagation.'''
        values = {}

        return values

    def solve(self):
        '''Solves the problem as described in the class' variables.'''
        # initial set up


def parse_vars(var_file):
    '''Converts the input file into a dictionary, where
    the key is the variable name and the value is an array
    of possible values.
    '''

    variables = {}
    for variable_line in var_file.readlines():
        # clean up newlines
        variable_line = variable_line.strip()

        # split the line into variable and possible values, which are seperated by ":"
        single_arr = variable_line.split(":")

        # variable name is first instance of the array, character(s) before the ":" symbol
        variable = single_arr[0].strip()

        # add possible values to the array
        values_arr = []
        for value in single_arr[1].strip().split(" "):
            # cast values as ints
            values_arr.append(int(value))

        variables[variable] = values_arr

    return tuple(variables.keys()), variables

def parse_con(con_file):
    '''Converts the input file into an array, where each value is a tuple.
    Each tuple has a tuple of the two values the constraint applies to,
    and the second value is a lambda function that represents the constrant.
    '''
    constraints = []

    for constraint_line in con_file.readlines():
        # clean up newline characters
        constraint_line = constraint_line.strip()

        # split the line into the three parts
        con_arr = constraint_line.split(" ")
        var1, eq, var2 = con_arr[0], con_arr[1], con_arr[2]

        # construct a tuple representing the constraint and add it to the list of constraints
        if   eq == "=":
            # A = B
            constraints.append(((var1,var2), lambda a,b: a==b))
        elif eq == "!":
            # A ! B
            constraints.append(((var1,var2), lambda a,b: a!=b))
        elif eq == ">":
            # A > B
            constraints.append(((var1,var2), lambda a,b: a>b))
        elif eq == "<":
            # A < B
            constraints.append(((var1,var2), lambda a,b: a<b))
        else:
            # raise an exception if the .con file has a bad constraint
            raise Exception("Unknown operator in constraint file", eq)

    return constraints


if __name__ == "__main__":
    try:
        var = open(args.var, "r")
        con = open(args.con, "r")
        ce  = True if args.consistency == "fc" else False

        problem = CSPsolver(var, con, ce)
        problem.solve()

    except Exception as e:
        raise e
    finally:
        pass
