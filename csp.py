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

    def select_unset_variable(self, assignment):
        '''Returns the value to next search for, given the current assignment of variables, and the possible
        variables assigned in the class.
        '''
        # get possible unset variables
        vars_set = []
        for variable, value in assignment:
            vars_set.append(variable)
        unset = [variable for variable in self.variables if variable not in vars_set]

        # to select a variable, first use the most constrained heuristic
        possible = [] # list of possible values
        lowest = 9999 # constrained score to test against
        c_ed = self.h_constrained(unset) # current state of constrained values
        for score, variable in c_ed:
            # if most constrained so far, replace current possible variables array
            if score < lowest:
                possible = [variable]
                lowest = score
            # if tied for most constraining, add to the list
            elif score == lowest:
                possible.append(variable)
        # if the list only has one variable, return that variable
        if len(possible) == 1:
            return possible[0]

        # else, sort by the most constrained heuristic
        possible2 = []
        highest = 0
        c_ing = self.h_constraining(possible)
        for score, variable in c_ing:
            # if the variable has the most constraints so far, replace the possible variables list
            if score > highest:
                possible2 = [variable]
                highest = score
            # if tied for most constrained, add to the list
            elif score == highest:
                possible2.append(variable)

        # if the list only has one variable, return that variable
        if len(possible2) == 1:
            return possible2[0]

        # else, sort alphabetically
        return sorted(possible2)[0]

    def conflicts(self, assignment, trial):
        pass

    def backtrack_recurse(self, assignment):
        '''Recursive component for backtrack_search.'''
        # if the assignment has all variables set, then return it as a solution.
        if len(assignment) == len(self.variables):
            return assignment
        # else, pick the next variable to be assigned a value
        var = self.select_unset_variable(assignment)
        for value in self.domains[var]:
            # check for the conflicts given the new assignment
            if self.conflicts(assignment, (var, value)) == []:
                # if no assignments, recurse in that direction
                new_assign = assignment.append((var, value))
                result = self.backtrack_recurse(new_assign)
                if result is not None:
                    # back-propagate result
                    return result
        # Return none if no assignments found
        return None

    def backtrack_search(self):
        '''Starts a backtracking search given the class' current configuration.'''
        return self.backtrack_recurse([])


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
