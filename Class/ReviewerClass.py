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
        self.id = rid
        self.cur = 0
        self.incur = 0
        self.case1 = 0
        self.case2 = 0
        # first~ is reviewer's status before start voting
        self.first_cur = 0
        self.first_incur = 0
        self.first_case1 = 0
        self.first_case2 = 0
        self.p_list = [];
        self.per_former = 0
        self.per_latter = 0
        self.flag = 0   # It means this whether or not this reviewer is focused on this research. # 1 means "focused"
        self.incurrent_vote = 0
        self.is_first_vote_incurrent = 0

    def saveFirst(self):
        self.first_cur = self.cur
        self.first_incur = self.incur
        self.first_case1 = self.case1
        self.first_case2 = self.case2
        self.incurrent_vote = 0
        self.is_first_vote_incurrent = 0

    def addCur(self):
        self.cur = self.cur + 1;
        self.p_list.append(1); ## 1 means "Current"
        if self.is_first_vote_incurrent == 0:
            self.is_first_vote_incurrent = 1

    def addIncur(self):
        self.incur = self.incur + 1;
        self.p_list.append(0); ## 0 means "InCurrent"
        if self.is_first_vote_incurrent == 0:
            self.is_first_vote_incurrent = 2

    def addCase(self, s):
        if s > 0:
            self.case1 += 1
        else:
            self.case2 += 1
        self.incurrent_vote = 1
        assert self.case1 + self.case2 == self.incur
        assert self.is_first_vote_incurrent-1 != 1 or self.incurrent_vote != 0

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
