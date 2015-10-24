##################
# Author:Ueda Yuki
# CreatedOn: 2015/10/14
# Summary: This program is to count current judge and incurrent judge.
##################

#comment is not correct

### Import lib
import sys
import csv
import MySQLdb
from collections import defaultdict
from Util import ReviewerFunctions
from Class import ReviewerClass

### Init
reviewer_class = defaultdict(lambda: 0)
reviewer = []

### Connect DB
cnct = MySQLdb.connect(db="qt",user="root", passwd="password")
csr = cnct.cursor()

### Set default ReviewNum
sql = "SELECT COUNT(*) FROM Review;"
csr.execute(sql)
ReviewNum = csr.fetchall()[0][0] # 70705 <= Number Of Qt project's patchsets

# set original ReviewNum
argv = sys.argv
argc = len(argv)
if argc == 2:
	ReserchCommentNum = int(argv[1])
else:
	ReserchCommentNum = 3

# out put Reviewid min
outId = 10000;
# Number of Comments to the patch one

### Main
# @ScoreOfReliability: the sum of all reviewers' reliability in each patch
# @VotingScore: the score that a reviewer voted. (+1 or -1)
print "ReviewId,Reviewerid,CommentIndex,NumOfCurrent,NumOfincurrent,CurrentPar,IncurrentPar,ScoreOfReliability,VotingScore,Status" # print clumn name

#for Id in range(1, ReviewNum):
for Id in range(1, ReviewNum):
	sql = "SELECT ReviewId, Status "\
	"FROM Review "\
	"WHERE ReviewId = '"+str(Id)+"' "\
	"AND (Status = 'merged' OR Status = 'abandoned');"
	csr.execute(sql)
	info = csr.fetchall()

	sql = "SELECT ReviewId, AuthorId, Message "\
	"FROM Comment "\
	"WHERE ReviewId = '"+str(Id)+"' "\
	"ORDER BY WrittenOn ASC;"
	csr.execute(sql)
	comments = csr.fetchall()

	reviewers_written = []	# Reviewer which has already written a comment in the patch
	reviewers_List = [] 	# Reviewer which wrote comments in the patch Set (patch not equal patch Set)
	reviewers_score = []

	### Extract status
	assert len(info) == 0 or len(info) == 1
	for information in info:
		status = information[1]

	### Limitation for CommentNum (@author:toshiki.hirao)
	vCt = 0 # Number of voting "+1" or ""-1"
	for comment in comments:
		message = comment[2]
		s = ReviewerFunctions.JudgeVoteScore(message)
		if(s == 1 or s == -1):
			vCt = vCt + 1
	if vCt != ReserchCommentNum:
		continue  # Skip the following
	CommentNum = vCt
	assert CommentNum == ReserchCommentNum

	### Analysis (If CommentNum equals only ReserchCommentNum, the following code works)
	index = 1  # @index:CommentIndex
	score = 0  # @score:ScoreOfReliabilitys
	for i, comment in enumerate(comments):
		message = comment[2]
		# Judge whether or not this patch was desided by decision comment<"merged, abandoned"> which mean [status] of reviewdata.
		# And, We regard that "updated ---" comment is also decision comment.
		# And, We regard that +2 score comment is the same as "merged", -2 score comment is the same as "abandoned".
		# Summary -> "merged, abandoned, 'updated --- ', +2, -2" is {JudgeDicisionMaking commnet}
		judge = ReviewerFunctions.JudgeDicisionMaking(message)
		if judge == 0:
			s = ReviewerFunctions.JudgeVoteScore(message)
			if(s == 1 or s == -1):
				reviewer = comment[1]
				reviewers_List.append(reviewer)
				reviewers_score.append(s)
				reviewers_written.append(reviewer)

		else:
			assert len(reviewers_List) == len(reviewers_score)
			for (r, s) in zip(reviewers_List, reviewers_score):
				if not ReviewerFunctions.IsReviewerClass(r, reviewer_class):
					ReviewerFunctions.MakeReviewerClass(r, reviewer_class)

				reviewer = reviewer_class[r]
				if ReviewerFunctions.IsCorrectVoting(r, s, judge):
					reviewer.addCur()
				else:
					reviewer.addIncur()

				if CommentNum == ReserchCommentNum:
					currentPar = reviewer.cur/float(reviewer.cur+reviewer.incur)
					incurrentPar = reviewer.incur/float(reviewer.cur+reviewer.incur)
					score = score + currentPar
					if Id > outId:
						print "%4d,%d,%2d,%3d,%3d,%f,%f,%f,%d,%s" % (Id, r, index, reviewer.cur, reviewer.incur, currentPar, incurrentPar, score, s, status)
					index = index + 1
			reviewers_List = []
			reviewers_score = []

	for (r, s) in zip(reviewers_List, reviewers_score):
		if status == "merged":
			judge = 2
		else:     # status is abandoned
			judge = -2

		if not ReviewerFunctions.IsReviewerClass(r, reviewer_class):
			ReviewerFunctions.MakeReviewerClass(r, reviewer_class)

		reviewer = reviewer_class[r]
		if ReviewerFunctions.IsCorrectVoting(r, s, judge):
			reviewer.addCur()
		else:
			reviewer.addIncur()

		if CommentNum == ReserchCommentNum:
			currentPar = reviewer.cur/float(reviewer.cur+reviewer.incur)
			incurrentPar = reviewer.incur/float(reviewer.cur+reviewer.incur)
			score = score + currentPar
			if Id > outId:
				print "%4d,%d,%2d,%3d,%3d,%f,%f,%f,%d,%s" % (Id, r, index, reviewer.cur, reviewer.incur, currentPar, incurrentPar, score, s, status)
			index = index + 1
	#assert index == 3
