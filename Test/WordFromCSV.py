# -*- coding: utf-8 -*-
##################
# Author:Yuki Ueda
# CreatedOn: 2015/09/27
# Summary: This program extract the review's suggestion.
##################

import MeCab
import csv


wordList = []

wordList = csv.reader(open('message.csv', 'rb'), delimiter=' ', quotechar='|')
    for row in wordList:
        print ', '.join(row)
