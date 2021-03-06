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
#print "ReviewId, ReviewersNum, AveReliability, MimReliability, Status, PatchType" # print clumn name
print "ReviewId, ReviewerId ,CommentNum, cur, incur, currentPar" # print clumn name

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

	reviewers = {}
	reviewers_List = []
	reviewers_first_score = []
	reviewers_score = []

	### Extract status
	assert len(info) == 0 or len(info) == 1
	for information in info:
		status = information[1]

	### Analysis (If CommentNum equals only ReserchCommentNum, the following code works)
	CommentNum = 0
	for comment in comments:
		reviewer = int(comment[1])
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
			reviewers[reviewer] = s

		CommentNum = len(reviewers)

	# output information of firstVote
	if CommentNum > 0:
		score = 0  # @score:ScoreOfReliabilitys
		mimScore = 1
		IsConsensus = True
		beforeVote = 0
		for r, s in reviewers.items():
			if beforeVote != 0 and s != beforeVote:
				IsConsensus = False
			else:
				beforeVote = s

			if not ReviewerFunctions.IsReviewerClass(r, reviewer_class):
				ReviewerFunctions.MakeReviewerClass(r, reviewer_class)

			reviewer = reviewer_class[r]
			if reviewer.cur+reviewer.incur != 0:
				currentPar = float(reviewer.cur) / (reviewer.cur+reviewer.incur)
			else:
				currentPar = 0
			if currentPar < mimScore:
				mimScore = currentPar
			score = score + currentPar
			if (CurrentDB=="qt" and (Id==8141 or Id==1048 or Id==7375 or Id==28257)) or (CurrentDB=="Openstack" and (Id==10363 or Id == 10305)):
				print "%4d, %d, %d, %d, %d, %2f" % (Id, r ,CommentNum, reviewer.cur, reviewer.incur, currentPar)
		if IsConsensus:
			if (beforeVote == 1 and status == "merged") or (beforeVote == -1 and status == "abandoned"):
				PatchType = "AllCorrect"
			else:
				PatchType = "AllInCorrect"
		else:
			PatchType = "NotConsensus"

		scoreAve = float(score) / CommentNum
		#if Id > StartId:
			#print "%4d, %d, %2f, %2f, %s, %s" % (Id, CommentNum, scoreAve, mimScore, status, PatchType)

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
