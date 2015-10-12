##################
# Author:Ueda Yuki
# CreatedOn: 2015/10/10
# Summary: This program is to count current judge and incurrent judge.
##################

#comment is not correct

### Import lib
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

sql = "SELECT COUNT(*) FROM Review;"
csr.execute(sql)
ReviewNum = csr.fetchall()[0][0] # 70705 <= Number Of Qt project's patchsets

### Main
for Id in range(1, ReviewNum/100):
	sql = "SELECT ReviewId, Status "\
	"FROM Review "\
	"WHERE ReviewId = '"+str(Id)+"';"
	csr.execute(sql)
	info = csr.fetchall()

	sql = "SELECT ReviewId, AuthorId, Message "\
	"FROM Comment "\
	"WHERE ReviewId = '"+str(Id)+"' "\
	"ORDER BY WrittenOn asc;"
	csr.execute(sql)
	comments = csr.fetchall()

	reviewers_written = []	# Reviewer which has already written a comment in the patch
	reviewers_List = [] 	# Reviewer which wrote comments in the patch Set (patch not equal patch Set)
	reviewers_score = []

	### Extract status
	assert len(info) == 0 or len(info) == 1
	for information in info:
		status = information[1]

	### Analysis
	if status not in ["merged" ,"abandoned"]: # We target the patches which were decided merged or abandoned
		continue

	for comment in comments:
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
				#print str(reviewer)+":"+str(message)
				if reviewer not in reviewers_written:	# A Reviewer who has already written for this patch
					reviewers_List.append(reviewer)
					reviewers_score.append(s)
					reviewers_written.append(reviewer)

		else:
			assert len(reviewers_List) == len(reviewers_score)
			for (r, s) in zip(reviewers_List, reviewers_score):
				if not ReviewerFunctions.IsReviewerClass(r, reviewer_class):
					ReviewerFunctions.MakeReviewerClass(r, reviewer_class)

				if ReviewerFunctions.IsCorrectVoting(r, s, judge):
					reviewer_class[r].addCur()
				else:
					reviewer_class[r].addIncur()
	###
	for (r, s) in zip(reviewers_List, reviewers_score):
		if status == "merged":
			judge = 2
		else:     # status is abandoned
			judge = -2

		if not ReviewerFunctions.IsReviewerClass(r, reviewer_class):
			ReviewerFunctions.MakeReviewerClass(r, reviewer_class)

		if ReviewerFunctions.IsCorrectVoting(r, s, judge):
			reviewer_class[r].addCur()
		else:
			reviewer_class[r].addIncur()

### Culcurate Former and Latter

### Output
print "Reviewid,NumOfCurrent,NumOfincurrent,CurrentPar,IncurrentPar" # print clumn name
for i in reviewer_class:
	currentPar = reviewer_class[i].cur/float(reviewer_class[i].cur+reviewer_class[i].incur)
	incurrentPar = reviewer_class[i].incur/float(reviewer_class[i].cur+reviewer_class[i].incur)
	print "%d,%d,%d,%f,%f" % (i, reviewer_class[i].cur, reviewer_class[i].incur,currentPar,incurrentPar)
