#!/usr/bin/python3
##################
# Author:Toshiki Hirao
# CreatedOn: 2015/09/18
# Summary: This program is to define Functions for reviewer information.
##################
import re
import sys
import csv
import time
import MySQLdb
from collections import defaultdict
from datetime import datetime
from Class import ReviewerClass

### Define Functions
# JudgeVoteScore(m)
# @m:message
######
# If Score is '+1' -> return 1
# If Score is '-1' -> return -1
# If Score isn't '+1' or '-1' -> return 0
######
def JudgeVoteScore(m): # (Regular expression)
    # Score +1
	positiveVote = []
	positiveVote.append(r'Patch Set [1-9]*: Looks good to me, but someone else must approve') #
	positiveVote.append(r'Patch Set [1-9]*: Works for me')
	positiveVote.append(r'Patch Set [1-9]*: Verified')
	positiveVote.append(r'Patch Set [1-9]*: Sanity review passed') #
	positiveVote.append(r'Patch Set [1-9]*: Code-Review\+1')
	positiveVote.append(r'Patch Set [1-9]*: Workflow\+1')
	positiveVote.append(r'Patch Set [1-9]*: Looks good to me, approved') #
	positiveVote.append(r'Patch Set [1-9]*: Looks good to me<br>')

	for p in positiveVote:
		if re.compile(p).match(m):
			return 1

    # Score -1
	negativeVote = []
	negativeVote.append(r"Patch Set [1-9]*: I would prefer that you didn'*t submit this") #
	negativeVote.append(r'Patch Set [1-9]*: Sanity problems found') #
	negativeVote.append(r'Patch Set [1-9]*: Code-Review-1')
	negativeVote.append(r'Patch Set [1-9]*: Workflow-1')
	negativeVote.append(r"Patch Set [1-9]*: Doesn'*t seem to work")
	negativeVote.append(r"Patch Set [1-9]*: I would prefer that you didn'*t merge this")
	negativeVote.append(r'Patch Set [1-9]*: No score')
	negativeVote.append(r'Patch Set [1-9]*: Do not merge') #
	negativeVote.append(r'Patch Set [1-9]*: Do not submit') #
	negativeVote.append(r'Patch Set [1-9]*: Major sanity problems found') #
	negativeVote.append(r'Patch Set [1-9]*: Fails')

	for p in negativeVote:
		if re.compile(p).match(m):
			return -1

    # Score 0
	"""
	p1.append(r'Patch Set [1-9]*: No score')
	if p1.match(m):
		return 0
	"""
	# No Score
	return 0

# Judge whether the comment is Dicision or not
# @m:message
def JudgeDicisionMaking(m):
	# merge
	if re.compile(r'Change has been successfully cherry-picked').match(m):
		return 2

	# abandoned
	if re.compile(r'Abandoned').match(m):
		return -2

	# Not JudgeDicisionMaking
	return 0

def IsUpdate(m):
	return re.compile(r'Uploaded patch set [1-9]*').match(m)

def IsReviewerClass(r, reviewer_class):
	assert r > 0
	if reviewer_class[r] != 0:
		return True
	else:
		#print "False"
		return False

def MakeReviewerClass(r, reviewer_class):
	assert r > 0 and reviewer_class[r] == 0
	reviewer_class[r] = ReviewerClass.Reviewer(r)
	#print type(ReviewerClass.Reviewer(r))
	return r

def IsCorrectVoting(r, s, judge):
	if (s > 0 and judge > 0) or (s < 0 and judge < 0):
		assert (s == 1 and judge == 2) or (s == -1 and judge == -2)
		return True
	else:
		assert (s == -1 and judge == 2) or (s == 1 and judge == -2)
		return False
