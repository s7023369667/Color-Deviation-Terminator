#!/usr/bin/python
import sys
from collections import Counter, defaultdict
import ast
lineDict = {}
#c = Counter()
for line in sys.stdin.readlines():
    lineDict = ast.literal_eval(line)
    #c.update(lineDict)
print (lineDict)