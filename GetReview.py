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

# set original ReviewNum
argv = sys.argv
argc = len(argv)
if argc == 2:
	CurrentDB = argv[1]
else:
	CurrentDB = "qt"

### Connect DB
# db = qt or Openstack
cnct = MySQLdb.connect(db=CurrentDB,user="root", passwd="password")
csr = cnct.cursor()

### Set default ReviewNum
sql = "SELECT COUNT(*) FROM Review;"
csr.execute(sql)
ReviewNum = csr.fetchall()[0][0] # 70705 <= Number Of Qt project's patchsets
StartNum = ReviewNum * 0.1

### Main
# @ScoreOfReliability: the sum of all reviewers' reliability in each patch
# @VotingScore: the score that a reviewer voted. (+1 or -1)
print "ReviewId,Status" # print clumn name

for Id in range(int(StartNum), ReviewNum):
	sql = "SELECT ReviewId, Status \
	FROM Review \
	WHERE ReviewId = '"+str(Id)+"' \
	AND (Status = 'merged' OR Status = 'abandoned');"
	csr.execute(sql)
	info = csr.fetchall()

	assert len(info) == 0 or len(info) == 1
	for information in info:
		status = information[1]
	print "%4d, %s" % (Id, status)
