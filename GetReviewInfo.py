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
elif CurrentDB == "Openstack":
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
StartId = int(ReviewNum * 0.1)

### Main
# @ScoreOfReliability: the sum of all reviewers' reliability in each patch
# @VotingScore: the score that a reviewer voted. (+1 or -1)
print "ReviewId, Reviewerid, CommentIndex, NumOfCurrent, NumOfincurrent, CurrentPar, IncurrentPar, ScoreOfReliability, VotingScore, Status" # print clumn name

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
	reviewers_first_score = []
	reviewers_score = []

	### Extract status
	assert len(info) == 0 or len(info) == 1
	for information in info:
		status = information[1]

	### Analysis (If CommentNum equals only ReserchCommentNum, the following code works)
	CommentNum = 0
	for comment in comments:
		reviewer = comment[1]
		message = comment[2]

		judge = ReviewerFunctions.JudgeDicisionMaking(message)

		# comment is judge vote
		if judge != 0:
			break

		if ReviewerFunctions.IsUpdate(message):
			continue

		# get vote message and reviewer's Id
		s = ReviewerFunctions.JudgeVoteScore(message)
		if s != 0:	# remove update comment and not votecomment
			if reviewer not in reviewers_written:
				reviewers_written.append(reviewer)
				reviewers_first_score.append(s)
				CommentNum += 1


	assert CommentNum == len(reviewers_written)

	# output information of firstVote
	if Id > StartId:
		score = 0  # @score:ScoreOfReliabilitys
		for index, (r, s) in enumerate(zip(reviewers_written, reviewers_first_score)):
			if not ReviewerFunctions.IsReviewerClass(r, reviewer_class):
				ReviewerFunctions.MakeReviewerClass(r, reviewer_class)

			reviewer = reviewer_class[r]
			if CommentNum == ReserchCommentNum:
				if reviewer.cur+reviewer.incur != 0:
					currentPar = float(reviewer.cur) / (reviewer.cur+reviewer.incur)
					incurrentPar = float(reviewer.incur) / (reviewer.cur+reviewer.incur)
				else:
					currentPar = 0
					incurrentPar = 0
				score = score + currentPar
				print "%4d, %d, %2d, %3d, %3d, %f, %f, %f, %d, %s" % (Id, r, index + 1, reviewer.cur, reviewer.incur, currentPar, incurrentPar, score, s, status)

	# collect all vote in comments
	for comment in comments:
		message = comment[2]
		judge = ReviewerFunctions.JudgeDicisionMaking(message)
		if judge != 0:
			break

		if not ReviewerFunctions.IsUpdate(message):
			s = ReviewerFunctions.JudgeVoteScore(message)
			if(s == 1 or s == -1):
				reviewer = comment[1]
				reviewers_List.append(reviewer)
				reviewers_score.append(s)

		else:
			# calc Current
			judge = -2
			assert len(reviewers_List) == len(reviewers_score)
			for (r, s) in zip(reviewers_List, reviewers_score):
				if not ReviewerFunctions.IsReviewerClass(r, reviewer_class):
					ReviewerFunctions.MakeReviewerClass(r, reviewer_class)

				reviewer = reviewer_class[r]
				if ReviewerFunctions.IsCorrectVoting(r, s, judge):
					reviewer.addCur()
				else:
					reviewer.addIncur()

			reviewers_List = []
			reviewers_score = []

	# calc Current
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
