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
        self.var = parse_vars(var)
        self.con = parse_con(con)
        self.fc = ce

    def solve(self):
        pass

def parse_vars(var_file):
    pass

def parse_con(con_file):
    pass



if __name__ == "__main__":
    try:
        var = open(args.var, "r")
        con = open(args.con, "r")
        ce  = True if args.consistency == "fc" else False

        problem = CSPsolver(var, con, ce)
        problem.solve()

    except Exception e:
        print(e)
    finally:
        pass
