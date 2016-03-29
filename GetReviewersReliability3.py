##################
# Author:Ueda Yuki
# Summary: This program is to count current judge and incurrent judge.
# Usage: python GetReviewersReliability3.py "dbname" > CSVdata_journal/Qt2.csv
##################

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
if argc == 2:
	CurrentDB = argv[1]
else:
	CurrentDB = "qt"

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

### Main
# @ScoreOfReliability: the sum of all reviewers' reliability in each patch
# @VotingScore: the score that a reviewer voted. (+1 or -1)
print "ReviewId, ReviewerId, CommentIndex, NumOfVotes, NumOfCurrent, NumOfincurrent, CurrentPar, IncurrentPar, ScoreOfReliability,  Case1, Case2, \
LaterNumOfVotes, LatterNumOfCurrent, LatterNumOfincurrent, LatterCurrentPar, LatterIncurrentPar, LatterScoreOfReliability,  LatterCase1, LatterCase2, \
VotingScore, Status, IncurrentVote, IsFirstVoteIncurrent, CurrentChain" # print clumn name

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

	### Count CommentNum and Get first_score and reviewers
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


	# save information of firstVote and reset incurrent_vote
	for index, (r) in enumerate(reviewers_written):
		if not ReviewerFunctions.IsReviewerClass(r, reviewer_class):
			ReviewerFunctions.MakeReviewerClass(r, reviewer_class)
		reviewer = reviewer_class[r]
		reviewer.saveFirst()

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
					reviewer.addCase(s)

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
			reviewer.addCase(s)

	# if len(reviewers_written) < 2 or Id < ReviewNum * 0.1:
	# 	continue

	# output infor mation of firstVote
	score = 0  # @score:ScoreOfReliabilitys
	latter_score = 0
	for index, (r, s) in enumerate(zip(reviewers_written, reviewers_first_score)):
		reviewer = reviewer_class[r]

		if reviewer.first_cur+reviewer.first_incur != 0:
			currentPar = float(reviewer.first_cur) / (reviewer.first_cur+reviewer.first_incur)
			incurrentPar = float(reviewer.first_incur) / (reviewer.first_cur+reviewer.first_incur)
		else:
			currentPar = 0
			incurrentPar = 0

		latter_currentPar = float(reviewer.cur) / (reviewer.cur+reviewer.incur)
		latter_incurrentPar = float(reviewer.incur) / (reviewer.cur+reviewer.incur)

		score = score + currentPar
		latter_score = latter_score + latter_currentPar
		voteNum = reviewer.first_cur + reviewer.first_incur
		latter_voteNum = reviewer.cur + reviewer.incur

		assert voteNum == reviewer.first_cur + reviewer.first_case1 + reviewer.first_case2
		print "%4d, %d, %2d, %3d, %3d, %3d, %f, %f, %f, %d, %d,\
 %3d, %3d, %3d, %f, %f, %f, %d,%d, \
 %d, %s, %d, %d, %d" % \
		(Id, r, index + 1, voteNum, reviewer.first_cur, reviewer.first_incur, currentPar, incurrentPar,score, reviewer.first_case1, reviewer.first_case2,\
		 latter_voteNum, reviewer.cur, reviewer.incur, latter_currentPar, latter_incurrentPar, latter_score, reviewer.case1, reviewer.case2,\
		 s, status, reviewer.incurrent_vote, reviewer.is_first_vote_incurrent-1, reviewer.first_current_chain)
