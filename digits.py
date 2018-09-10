#!/usr/bin/env python3

"""digits.py: Script to identify digits written as pipes and undescores."""

__author__ = "Mario Burbano"
__version__ = "0.1"
__maintainer__ = "Mario Burbano"
__email__ = "burbanom@tcd.ie"

import os, sys
from pathlib import Path
import itertools

def get_arrangements():
    arrangements = dict()
    for index, *rest in enumerate(list(itertools.product([True,False], repeat=3))):
        line = 3*[' ']
        if rest[0][0]:
            line[0] = '|'
        if rest[0][1]:
            line[1] = '_'
        if rest[0][2]:
            line[2] = '|'
        arrangements[str(index)] = line
            
    return arrangements

def gen_digit(list_of_arrangements):
    return "\n".join([''.join((x)) for x in list_of_arrangements])

def gen_characters():
    arrangements = get_arrangements()

    top = {'0':3*[' '], '1':[' ', '_', ' ']}
    
    # N.B arrangements['3'] and arrangements['5'] are not present in middle section
    zero =  [top['1'], arrangements["2"], arrangements["0"], arrangements["7"]]
    one =   [top['0'], arrangements['6'], arrangements['6'], arrangements['7']]
    two =   [top['1'], arrangements['4'], arrangements['1'], arrangements['7']]
    three = [top['1'], arrangements['4'], arrangements['4'], arrangements['7']]
    four =  [top['0'], arrangements['0'], arrangements['6'], arrangements['7']]
    five =  [top['1'], arrangements['1'], arrangements['4'], arrangements['7']]
    six =   [top['0'], arrangements['1'], arrangements['0'], arrangements['7']]
    seven = [top['1'], arrangements['6'], arrangements['6'], arrangements['7']]
    eight = [top['1'], arrangements['0'], arrangements['0'], arrangements['7']]
    nine =  [top['1'], arrangements['0'], arrangements['6'], arrangements['7']]
    
    characters = {'0':zero, '1':one, '2':two, '3':three, \
                  '4':four, '5':five, '6':six, '7':seven, \
                  '8':eight, '9':nine}
    return characters    

def indexer(iterable, step):
    return [iterable[i:i+step] for i in range(0, len(iterable), step)]

if __name__ == "__main__":

    
    for char in gen_characters().values():    
        print(gen_digit(char))
    
    with open('digits.txt') as f:
#        for index, line in enumerate(f.readlines()):
        for index, line in enumerate(indexer(f.readlines(), 4)):
            print(f"{index} {line}")
#            if len(line) != 28:
#            line = line.strip('\n')
#            print(f"{index+1:} {indexer(line, 3)}")