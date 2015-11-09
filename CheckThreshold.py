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

# set original ReviewNum
argv = sys.argv
argc = len(argv)
threshold = []
vote = [] # Reserch vote score

if argc >= 7:
	CurrentDB = argv[1]
	ReserchCommentNum = int(argv[2])
	threshold = [float(argv[3]),float(argv[4]),float(argv[5])]
	vote.append(int(argv[6]))
	if argc >= 8:
		vote.append(int(argv[7]))
else:
	CurrentDB = "qt"
	ReserchCommentNum = 1
	threshold = [0.8897, 0.8872, 0.8782]
	vote.append(1)

assert len(vote) == ReserchCommentNum

# Number of Comments to the patch one

TP = [0,0,0] # True Positive
FP = [0,0,0]
TN = [0,0,0]
FN = [0,0,0] # False Nagative

### Connect DB
cnct = MySQLdb.connect(db=CurrentDB,user="root", passwd="password")
csr = cnct.cursor()

### Set default ReviewNum
sql = "SELECT COUNT(*) FROM Review;"
csr.execute(sql)
ReviewNum = csr.fetchall()[0][0] # 70705 <= Number Of Qt project's patchsets

# out put Reviewid min
outId = 10000;

# Num of Patch in Vote Comment
inVoteNum = 0

for Id in range(outId+1, ReviewNum):
	sql = "SELECT Message "\
	"FROM Comment "\
	"WHERE ReviewId = '"+str(Id)+"';"
	csr.execute(sql)
	comments = csr.fetchall()
	for comment in comments:
		message = comment[0]
		s = ReviewerFunctions.JudgeVoteScore(message)
		if(s == 1 or s == -1):
			inVoteNum += 1
			break

StartNum = outId + int(inVoteNum * 0.8) + 1


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
				#if CommentNum == ReserchCommentNum:
				if ReviewerFunctions.IsCorrectVoting(r, s, judge):
					reviewer.addCur()
				else:
					reviewer.addIncur()

				notReserchVote = False
				for j,(v, rs) in enumerate(zip(vote, reviewers_score)):
					if v != rs:
						notReserchVote = True


				if Id < StartNum or notReserchVote or i + 1 != ReserchCommentNum:
					continue

				if (reviewer.cur+reviewer.incur == 0):
					currentPar = 0
				else:
					currentPar = reviewer.cur / float(reviewer.cur+reviewer.incur)

				for j, t in enumerate(threshold):
					if CommentNum == ReserchCommentNum:
						if currentPar >= t:
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

	for i,(r, s) in enumerate(zip(reviewers_List, reviewers_score)):
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

		notReserchVote = False
		for j,(v, rs) in enumerate(zip(vote, reviewers_score)):
			if v != rs:
				notReserchVote = True


		if Id < StartNum or notReserchVote or i + 1 != ReserchCommentNum:
			continue

		if (reviewer.cur+reviewer.incur == 0):
			currentPar = 0
		else:
			currentPar = reviewer.cur / float(reviewer.cur+reviewer.incur)

		for j, t in enumerate(threshold):
			if CommentNum == ReserchCommentNum:
				if currentPar >= t:
					TP[j] = TP[j] + 1
				else:
					FN[j] = FN[j] + 1
			else:
				if currentPar < t:
					FP[j] = FP[j] + 1
				else:
					TN[j] = TN[j] + 1

print vote
print "TP, TN, FP, FN, Precision, Recall, Accuracy, F1"
for i, t in enumerate(threshold):
	Precision = TP[i] / float(TP[i] + FP[i])
	Recall = TP[i] / float(TP[i] + FN[i])
	Accuracy = float(TP[i] + TN[i]) / float(TP[i] + FP[i] + TN[i] + FN[i])
	if Precision + Recall == 0:
		F1 = 0
	else:
		F1 = 2 * Precision * Recall / (Precision + Recall)
	print "%d,%d,%d,%d,%f,%f,%f,%f" % (TP[i], TN[i], FP[i], FN[i], Precision, Recall, Accuracy, F1)
