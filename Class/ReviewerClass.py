#!/usr/bin/python3
##################
# Author:Toshiki Hirao
# CreatedOn: 2015/09/18
# Summary: This program is to define class for reviewer information.
##################

### Class Difinition
class Reviewer:
    """ reviewer information """
    def __init__(self, rid):
        self.id = rid;
        self.cur = 0;
        self.incur = 0;
        self.p_list = [];
        self.per_former = 0
        self.per_latter = 0
        self.flag = 0   # It means this whether or not this reviewer is focused on this research. # 1 means "focused"

    def addCur(self):
        self.cur = self.cur + 1;
        self.p_list.append(1); ## 1 means "Current"

    def addIncur(self):
        self.incur = self.incur + 1;
        self.p_list.append(0); ## 0 means "InCurrent"

    def SetPerFormer(self, n):
        former_list = self.p_list[0:n];
        assert len(former_list) == n;
        NumC = 0; # Numcur(tmp)
        for v in former_list:
            if v == 1:
                NumC = NumC + 1;
        self.per_former = float(NumC) / n;

    def SetPerLatter(self, n):
        fn = -1 * n;
        latter_list = self.p_list[fn:];
        assert len(latter_list) == n;
        NumC = 0; # Numcur(tmp)
        for v in latter_list:
            if v == 1:
                NumC = NumC + 1;
        self.per_latter = float(NumC) / n;
