##################
# Author:Toshiki Hirao
# CreatedOn: 2016/03/28
# Summary: To extract the rows of top5% reviewers from csv data.
##################

## Import lib
import sys
import csv
from collections import defaultdict

### Read top5% List
top5_List = []
for line in open(sys.argv[1], "r"):
    values = line.strip().split(",")
    top5_List.append(values[0])

### Read csv
i = 1
for line in open(sys.argv[2], "r"):
    if i > 1:
        values = line.strip().split(",")
        if values[1] in top5_List:
            print line,
    i = i + 1
