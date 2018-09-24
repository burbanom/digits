#!/usr/bin/env python3

"""digits.py: Script to identify digits written as pipes and undescores. To be run using python 3.
    Proposed solution to: https://codingdojo.org/kata/BankOCR/"""

__author__ = "Mario Burbano"
__version__ = "0.1"
__maintainer__ = "Mario Burbano"
__email__ = "burbanom@tcd.ie"

import numpy as np
from scipy import signal 
import itertools
import argparse
from pathlib import Path

def parse_commandline_arguments():
    parser = argparse.ArgumentParser( description = 'Script to identify digits written as pipes and underscores' )
    ###########################################################################################################################################
    parser.add_argument( '--file', '-f', metavar = 'S', type=str, required = True, help='The file that contains the input digits' )
    parser.add_argument( '--debug', '-d', required = False, action = 'store_true', help='Activate debug/testing mode' )
    ############################################################################################################################################
    return parser.parse_args()

def get_arrangements_num():
    """ Generate number patterns for all arrangements of 0, -1 and 1 in a 3x3 matrix. """
    arrangements = dict()
    for index, *rest in enumerate(list(itertools.product([True,False], repeat=3))):
        line = 3*[0]
        if rest[0][0]:
            line[0] = 1
        if rest[0][1]:
            line[1] = -1
        if rest[0][2]:
            line[2] = 1
        arrangements[str(index)] = line
    return arrangements

def gen_characters_num():
    """ Create dictionary with all 3x3 matrices that represent digits from 0 to 9 """
    arrangements = get_arrangements_num()

    top = {'0':3*[0], '1':[0, -1, 0]}
    
    # N.B arrangements['3'] and arrangements['5'] are not present in middle section
    # and in addition to these, arrangements['2'] is not present in the bottom
    zero =  np.array([top['1'], arrangements["2"], arrangements["0"]])
    one =   np.array([top['0'], arrangements['6'], arrangements['6']])
    two =   np.array([top['1'], arrangements['4'], arrangements['1']])
    three = np.array([top['1'], arrangements['4'], arrangements['4']])
    four =  np.array([top['0'], arrangements['0'], arrangements['6']])
    five =  np.array([top['1'], arrangements['1'], arrangements['4']])
    six =   np.array([top['1'], arrangements['1'], arrangements['0']])
    seven = np.array([top['1'], arrangements['6'], arrangements['6']])
    eight = np.array([top['1'], arrangements['0'], arrangements['0']])
    nine =  np.array([top['1'], arrangements['0'], arrangements['4']])
    
    characters = {'0':zero, '1':one, '2':two, '3':three, \
                  '4':four, '5':five, '6':six, '7':seven, \
                  '8':eight, '9':nine}
    return characters    

def indexer(iterable, step):
    return [iterable[i:i+step] for i in range(0, len(iterable), step)]

def to_num(a_string):
    """Function to convert underscores and pipes into 0, 1 and -1 """
    nums = list()
    for x in a_string.rstrip('\n'):
        if x == '_':
            nums.append(-1)
        elif x == '|':
            nums.append(1)
        else:
            nums.append(0)
    return nums

def checksum(account):
    """ Used to determine if an account number is valid or not """
    if account[-1] == ' ':
        to_check = account[:-1]
    else:
        to_check = account
        
    to_check = np.flip(np.array(to_check, dtype=np.int),0)

    if np.mod(np.dot(to_check, np.arange(1,10)),11) == 0:
        return account
    else:
        account.append(' ERR ')
        return account

def get_acc_num(matrix, dictionary):
    """ We take sclices of the entire character matrix read from the digits.txt file and assign to them the corresponding number. """
    sizes = np.array([x[x!=0].size for x in indexer(matrix.T, 3)])
    acc = 9*['?'] 
    second_best_corrs = dict() # this dictionary contains the correlations and positions where a given 3x3 matrix had a good match
    for key, val in dictionary.items():
        # number of non-zero character matrix elements
        non_zero = val[val!=0].size
		
        # correlation calculation between the matrix slice and the 3x3 val matrix that is mapped to a given number
		# From scipy: https://docs.scipy.org/doc/scipy/reference/generated/scipy.signal.correlate.html
		# This approach is limited by the fact that the 3x3 matrix is likely to be matched in many places throughout the character file matrix. 
		# This is circumvented, however by making sure that the size (non-zero), as well as the correlation provide a good match.
        corr = signal.correlate(matrix, val, 'valid')

        holder = np.zeros(len(corr[0]), dtype = np.int8)
        for i, x in enumerate((corr != non_zero)[0]):
            if x:
                holder[i] = corr[0][i]
              
		# We keep track of the digigs that provide a good match, so that if we need to guess the identity of a character 
		# we do not have to perform this loop again!	  
        second_best = np.where(holder == holder.max())
        second_best_corrs[key] = (holder.max(),(second_best[0]/3).astype(int))


        overlaps, indices = np.where(corr == non_zero)

        if len(indices) > 0:
            indices = np.array(list(map(int,indices/3)))
            for index in indices:
                if sizes[index] == non_zero:
                    acc[index] = key
                    
    
    if '?' in acc: # if a number has not been properly assigned, we can use the second_best_corrs to propose values
        possibilities = list()
        for index in [i for i, x in enumerate(acc) if x == '?']:
            closest_index = dict()
            for key, val in second_best_corrs.items():
                if index in val[1]:
                    closest_index[key] = val[0]

            for replace in sorted(closest_index, key=closest_index.get, reverse=True):
                acc[index] = replace
                dummy = acc.copy()
                dummy.append(' ')

                possibilities.append(dummy)

        possibilities = [checksum(sublist) for sublist in possibilities if '?' not in sublist]
        possibilities = [item for sublist in possibilities for item in sublist]
        
        account = ''.join(possibilities)
            
    else:
        account = ''.join(checksum(acc))             
    return account

if __name__ == "__main__":

    args = parse_commandline_arguments()

    filename = Path(args.file)
    debug = args.debug

    if filename.is_file():
        # Here we read the file an transform its characters into a matrix
        digit_matrix = list()
        with open('digits.txt') as f:
            for index, lines in enumerate(indexer(f.readlines(), 4)):
                for line in lines[:3]:
                    digit_matrix.append(to_num(line))
    else:
        print('The filename provided is not valid')
        exit()

    # matrix containing all the characters in the file converted to 0, -1, 1                    
    digit_matrix = np.array(digit_matrix)

    characters_num = gen_characters_num()

    for row in indexer(digit_matrix, 3):
        acc = get_acc_num(row, characters_num)
        print(acc)
