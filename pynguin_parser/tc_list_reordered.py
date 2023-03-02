#!/usr/bin/env python
'''
This utility reorder a test case number list

USAGE:
     python tc_list_reorder.py <seed> <ALL|<number of elements>> <test case list numbers>
'''

import sys
import random

def main(args=None):
   if not args:
      return

   seed = args[0]
   testCaseNumbers = args[2:]
   numberOfTests = len(testCaseNumbers)
   if (args[1].upper() != 'ALL'):
      numberOfTests = int(args[1])

   random.seed(seed)
   shuffleList = random.sample(testCaseNumbers, len(testCaseNumbers))

   print(" ".join(shuffleList[0:numberOfTests]))

if __name__ == '__main__':
    if len(sys.argv) <=3:
        print("\nUSAGE:\n\t tc_list_reordered.py <seed> <ALL|<number of elements>> <test case list numbers>")
        sys.exit(1)
    else:
        main(sys.argv[1:])