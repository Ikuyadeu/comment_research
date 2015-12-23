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
if argc == 3:
	CurrentDB = argv[1]
	ReserchCommentNum = int(argv[2])
else:
	CurrentDB = "qt"
	ReserchCommentNum = 3

# definition bot's id that must be removed
if CurrentDB == "qt":
	botId = 1000049
else if CurrentDB = "Openstack":
	botId = 3
else:
	botId = 0

### Connect DB
# db = qt or Openstack
cnct = MySQLdb.connect(db=CurrentDB,user="root", passwd="password")
csr = cnct.cursor()

### Set default ReviewNum
sql = "SELECT COUNT(*) FROM Review;"
csr.execute(sql)
ReviewNum = csr.fetchall()[0][0] # 70705 <= Number Of Qt project's patchsets


# out put Reviewid min
outId = 0;

# Num of Patch in Vote Comment
#inVoteNum = 0

#for Id in range(outId+1, ReviewNum):
#	sql = "SELECT Message "\
#	"FROM Comment "\
#	"WHERE ReviewId = '"+str(Id)+"';"
#	csr.execute(sql)
#	comments = csr.fetchall()
#	for comment in comments:
#		message = comment[0]
#		s = ReviewerFunctions.JudgeVoteScore(message)
#		if(s == 1 or s == -1):
#			inVoteNum += 1
#			break

#ReviewNum = outId + int(inVoteNum * 0.8)


### Main
# @ScoreOfReliability: the sum of all reviewers' reliability in each patch
# @VotingScore: the score that a reviewer voted. (+1 or -1)
print "ReviewId, Reviewerid, CommentIndex, NumOfCurrent, NumOfincurrent, CurrentPar, IncurrentPar, ScoreOfReliability, VotingScore, Status" # print clumn name

#for Id in range(1, ReviewNum):
for Id in range(1, ReviewNum):
	sql = "SELECT ReviewId, Status \
	FROM Review \
	WHERE ReviewId = '"+str(Id)+"' \
	AND (Status = 'merged' OR Status = 'abandoned');"
	csr.execute(sql)
	info = csr.fetchall()

	sql = "SELECT ReviewId, AuthorId, Message \
	FROM Comment \
	WHERE ReviewId = '"+str(Id)+"' \
	AND AuthorId != '"+str(botId)+"' \
	ORDER BY WrittenOn ASC;"
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
	CommentNum = vCt

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
							print "%4d, %d, %2d, %3d, %3d, %f, %f, %f, %d, %s" % (Id, r, index, reviewer.cur, reviewer.incur, currentPar, incurrentPar, score, s, status)

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
				print "%4d, %d, %2d, %3d, %3d, %f, %f, %f, %d, %s" % (Id, r, index, reviewer.cur, reviewer.incur, currentPar, incurrentPar, score, s, status)
			index = index + 1
