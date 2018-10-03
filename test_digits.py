#!/usr/bin/env python3

"""test_digits.py: Script to test digits.py."""

__author__ = "Mario Burbano"
__version__ = "0.1"
__maintainer__ = "Mario Burbano"
__email__ = "burbanom@tcd.ie"

import os
script_path = os.path.dirname(os.path.realpath(__file__))
import unittest
from digits import *
from random import randint
import numpy as np
import sys

def random_with_N_digits(n):
    """ To generate a random number with n digits """
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

class TestGetAccNum(unittest.TestCase):

    def setUp(self):
        self.characters_num = gen_characters_num()
        # generate a random number of N digits
        self.digit_to_test = random_with_N_digits(9)
        start = 0
        end = 3
        matrix_shape = (3,27)
        self.matrix = np.zeros(matrix_shape)
        for index, digit in enumerate(list(str(self.digit_to_test))):
            self.matrix[start:end,start + index * 3:end + index * 3] =  self.characters_num[digit]

    def test_get_acc_num(self):
        print(f"Testing the digit {self.digit_to_test}")

        acc_num = get_acc_num(self.matrix, self.characters_num)
        print(f"Value obtained {acc_num}")
        acc_num = acc_num.split()
        val_to_compare = int(acc_num[0])
        self.assertTrue(val_to_compare == self.digit_to_test)

if __name__ == '__main__':
    unittest.main()
