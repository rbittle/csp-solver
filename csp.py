#! /usr/bin/python3

import argparse
import re

parser = argparse.ArgumentParser()

parser.add_argument("var", action="store", help="Name of the variables file used.")
parser.add_argument("con", action="store", help="Name of the constrains file used.")
parser.add_argument("consistency", action="store", help="Consistency-enforcing procedure. Either fc or none.")

args = parser.parse_args()



if __name__ == "__main__":
    try:
        var = open(args.var, "r")
        con = open(args.con, "r")


    except Exception e:
        print(e)
    finally:
        pass
