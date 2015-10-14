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

# Number of Comments to the patch one

### Main
print "ReviewId,Reviewerid,CommentIndex,NumOfCurrent,NumOfincurrent,CurrentPar,IncurrentPar,Status" # print clumn name

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

	CommentNum = len(comments)
	### Analysis
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
					print "%4d,%2d,%3d,%3d,%f,%f,%s" % (Id, i+1, reviewer.cur, reviewer.incur, currentPar, incurrentPar, status)

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
			print "%4d,%2d,%3d,%3d,%f,%f,%s" % (Id, i+1, reviewer.cur, reviewer.incur, currentPar, incurrentPar, status)
