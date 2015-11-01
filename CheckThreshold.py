##################
# Author:Ueda Yuki
# CreatedOn: 2015/10/14
# Summary: This program is to count current judge and incurrent judge.
##################

#comment is not correct

### Import lib
import sys
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
threshold = []
vote = [] # Reserch vote score

if argc >= 6:
	ReserchCommentNum = int(argv[1])
	threshold = [float(argv[2]),float(argv[3]),float(argv[4])]
	vote.append(int(argv[5]))
	if argc >= 7:
		vote.append(int(argv[6]))
else:
	ReserchCommentNum = 1
	threshold = [0.8897, 0.8872, 0.8782]
	vote.append(1)

assert len(vote) == ReserchCommentNum
# out put Reviewid min
outId = 10000;
# Number of Comments to the patch one

TP = [0,0,0] # True Positive
FP = [0,0,0]
TN = [0,0,0]
FN = [0,0,0] # False Nagative

### Main
# @ScoreOfReliability: the sum of all reviewers' reliability in each patch
# @VotingScore: the score that a reviewer voted. (+1 or -1)

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
	CommentNum = vCt

	### Analysis (If CommentNum equals only ReserchCommentNum, the following code works)
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

		else:
			assert len(reviewers_List) == len(reviewers_score)
			for (r, s) in zip(reviewers_List, reviewers_score):
				if not ReviewerFunctions.IsReviewerClass(r, reviewer_class):
					ReviewerFunctions.MakeReviewerClass(r, reviewer_class)

				reviewer = reviewer_class[r]
				if CommentNum == ReserchCommentNum:
					if ReviewerFunctions.IsCorrectVoting(r, s, judge):
						reviewer.addCur()
					else:
						reviewer.addIncur()

				judge2 = False
				for j,(v, rs) in enumerate(zip(vote, reviewers_score)):
					if v != rs:
						judge2 = True


				if Id < outId or judge2 or CommentNum < ReserchCommentNum:
					continue

				if (reviewer.cur+reviewer.incur == 0):
					currentPar = 0
				else:
					currentPar = reviewer.cur / float(reviewer.cur+reviewer.incur)

				for j, t in enumerate(threshold):
					if CommentNum > ReserchCommentNum:
						if currentPar < t:
							TP[j] = TP[j] + 1
						else:
							FN[j] = FN[j] + 1
					else:
						if currentPar < t:
							FP[j] = FP[j] + 1
						else:
							TN[j] = TN[j] + 1

			reviewers_List = []
			reviewers_score = []

	for (r, s) in zip(reviewers_List, reviewers_score):
		if status == "merged":
			judge = 2
		else: # status is abandoned
			judge = -2

		if not ReviewerFunctions.IsReviewerClass(r, reviewer_class):
			ReviewerFunctions.MakeReviewerClass(r, reviewer_class)

		reviewer = reviewer_class[r]
		if CommentNum == ReserchCommentNum:
			if ReviewerFunctions.IsCorrectVoting(r, s, judge):
				reviewer.addCur()
			else:
				reviewer.addIncur()

		judge2 = False
		for j,(v, rs) in enumerate(zip(vote, reviewers_score)):
			if v != rs:
				judge2 = True

		if Id < outId or judge2  or CommentNum < ReserchCommentNum:
			continue

		if reviewer.cur+reviewer.incur == 0:
			currentPar = 0
		else:
			currentPar = reviewer.cur / float(reviewer.cur+reviewer.incur)

		for i, t in enumerate(threshold):
			if CommentNum > ReserchCommentNum:
				if currentPar < t:
					TP[i] = TP[i] + 1
				else:
					FN[i] = FN[i] + 1
			else:
				if currentPar < t:
					FP[i] = FP[i] + 1
				else:
					TN[i] = TN[i] + 1

print vote
print "threshold, TP, TN, FP, FN"
for i, t in enumerate(threshold):
	print "%4f,%d,%d,%d,%d" % (t, TP[i], TN[i], FP[i], FN[i])
