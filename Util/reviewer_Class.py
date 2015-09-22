#!/usr/bin/python3
##################
# Author:Toshiki Hirao
# CreatedOn: 2015/09/18
# Summary: This program is to define class for reviewer information.
##################

### Class Difinition
class Reviewer:
    """ reviewer information """
    def __init__(self, id):
        self.id = rid;
        self.cur = 0;
        self.incur = 0;

    def addCur(self):
        self.cur = self.cur + 1;

    def addIncur(self):
        self.incur = self.incur + 1;
