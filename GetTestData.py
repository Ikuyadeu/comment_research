##################
# Author:Ueda Yuki
# CreatedOn: 2015/12/25
# Summary: This program is to count current judge and incurrent judge.
##################

#comment is not correct

### Import lib
import sys
import string
import MySQLdb
from collections import defaultdict
from Util import ReviewerFunctions
from Class import ReviewerClass

### Connect DB
# db = qt or Openstack
cnct = MySQLdb.connect(db="qt",user="root", passwd="password")
csr = cnct.cursor()

### Main
# @ScoreOfReliability: the sum of all reviewers' reliability in each patch
# @VotingScore: the score that a reviewer voted. (+1 or -1)
print "ReviewId,Status" # print clumn name

for Id in range(1, 100):
	sql = "SELECT ReviewId, Status \
	FROM Review \
	WHERE ReviewId = '"+str(Id)+"' \
	AND (Status = 'merged' OR Status = 'abandoned');"
	csr.execute(sql)
	info = csr.fetchall()

	assert len(info) == 0 or len(info) == 1
	for information in info:
		status = information[1]

	sql = "SELECT ReviewId, AuthorId, Message \
	From Comment \
	WHERE ReviewId = '"+str(Id)+"' \
	AND AuthorId != '100049' \
	ORDER BY WrittenOn ASC;"

	csr.execute(sql)
	info = csr.fetchall()

	for index,information in enumerate(info):
		AuthorId = information[1]
		Message = information[2]
		Message = Message.replace('\n',' ')
		if ReviewerFunctions.JudgeDicisionMaking(Message)!= 0:
			if ReviewerFunctions.JudgeDicisionMaking(Message) == 2:
				score = "Merge"
			else:
				score = "Abandoned"
			print "%4d, %d,%4d, %s ,%s, %s" % (Id, index,AuthorId, Message, score, status)
			break
		elif ReviewerFunctions.IsUpdate(Message):
			score = "Update"
		else:
			if ReviewerFunctions.JudgeVoteScore(Message) == 1:
				score = "+1"
			elif ReviewerFunctions.JudgeVoteScore(Message) == -1:
				score = "-1"
			else:
				score = "0"
				continue
		print "%4d, %d,%4d, %s ,%s, %s" % (Id, index,AuthorId, Message, score, status)
