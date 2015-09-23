# -*- coding: utf-8 -*-

import re
import sys
import csv
import time
import MySQLdb
from collections import defaultdict
from datetime import datetime


###
# Judge the message is vote message or not.
# @message:message contents
# @author:message author
def JudgeVoteScore(message, author, sAll, sa, sb, sc, sd, se):
	if("Patch Set 1: Looks good to me, approved" in message):
		sAll[author] += 1
		sa[author] += 1
		return 2
	if("Patch Set 1: Looks good to me, but someone else must approve" in message):
		sAll[author] += 1
		sb[author] += 1
		return 1
	if("Patch Set 1: Looks good to me" in message):
		sAll[author] += 1
		sa[author] += 1
		return 2
	if("Patch Set 1: Works for me" in message):
		sAll[author] += 1
		sb[author] += 1
		return 1
	if("Patch Set 1: Verified" in message):
		sAll[author] += 1
		sb[author] += 1
		return 1
	if("Patch Set 1: No score" in message):
		sAll[author] += 1
		sc[author] += 1
		return 0
	if("Patch Set 1: I would prefer that you didnt submit this" in message or "Patch Set 1: I would prefer that you didn't submit this" in message):
		sAll[author] += 1
		sd[author] += 1
		return -1
	if("Patch Set 1: I would prefer that you didnt merge this" in message or "Patch Set 1: I would prefer that you didn't merge this" in message):
		sAll[author] += 1
		se[author] += 1
		return -2
	if("Patch Set 1: Do not submit" in message):
		sAll[author] += 1
		se[author] += 1
		return -2
	########## auto test ##########
	if("Patch Set 1: Sanity review passed" in message): ## auto test
		sAll[author] += 1
		sb[author] += 1
		return 1
	if("Patch Set 1: Sanity problems found" in message): ## auto test
		sAll[author] += 1
		sd[author] += 1
		return -1
	if("Patch Set 1: Major sanity problems found" in message): ## auto test
		sAll[author] += 1
		se[author] += 1
		return -2
	###############################

	return 999

# Judge whether this message is "Abandoned" or "Change has been successfully cherry picked", or not.
# @comment:message
def IsDefinition(comment):
	pattern1 = re.compile(r'Patch Set 1: Abandoned') 					# "abandoned" about patchSet1
	pattern2 = re.compile(r'Change has been successfully cherry-picked as ')
	#pattern3 = re.compile(r'Successful integration')
	if(pattern1.match(comment)):
		return -1
	if(pattern2.match(comment)):
		return 1
	return 0

# Judge the author is Auto test machine or not
# @author:message author
def IsAutoTest(author):
	# 1000049 -> Qt Sanity Bot
	# -1 	  -> Gerrit System
	# 1000060 -> Qt Continuous Integration System
	# 1000191 -> Qt Submodule Update Bot
	# 1002169 -> Qt Doc Bot
	if(author == 1000049 or author == -1 or author == 1000060 or author == 1000191 or author == 1002169):
		return 1	## The author is Auto Test.
	else:
		return 0

### Set ReviewId to list
i = 0
Id_list = []
#Own_list = []
status_list = []
for row in open(sys.argv[1], "r"):
	if i > 0:
		words = row.split(",")
		Id_list.append(words[0])
		#Own_list.append(words[1])
		status_list.append(words[2])
	else:
		pass
	i += 1

cnct = MySQLdb.connect(db="qt",user="root", passwd="password")
csr = cnct.cursor()
time_csr = cnct.cursor()



FMT = '%Y-%m-%d %H:%M:%S'

i = 0
#for (Id, Own) in zip(Id_list, Own_list):
for (Id, st) in zip(Id_list, status_list):
	### hashtable about score
	sAll = defaultdict(lambda: 0)	# Number of total score
	sa = defaultdict(lambda: 0)		# Number of +2
	sb = defaultdict(lambda: 0)		# Number of +1
	sc = defaultdict(lambda: 0)		# Number of 0
	sd = defaultdict(lambda: 0)		# Number of -1
	se = defaultdict(lambda: 0)		# Number of -2
	own_com_num = 0					# Number of Owner Comments
	com_num = 0						# Number of Comments
	pos = 0							# Number of positive
	nor = 0							# Number of positive
	neg = 0							# Number of positive
	aut = []						# the list of Authors who wrote vote comment

	csr.execute("select ReviewId, Message, AuthorId, WrittenOn from Comment where ReviewId = '"+Id+"';")
	time_csr.execute("select ReviewId, CreatedOn from PatchSet where ReviewId = '"+Id+"' and PatchSetId = '1';")
	lines = csr.fetchall()
	sec_ps = time_csr.fetchall()
	time_list = []
	for sec in sec_ps:
		time_list.append(sec[1])
	assert len(time_list) == 1 or len(time_list) == 0

	message = []
	author = []
	writtenOn = []
	for line in lines:	## fix correct order from db messages.
		message.insert(-1, line[1].replace("\n", " "))
		author.insert(-1, line[2])
		writtenOn.insert(-1, datetime.strptime(str(line[3]), FMT))
	assert len(message) == len(author) and len(author) == len(writtenOn)


	process = []
	f = 0
	for (m, a, w) in zip(message, author, writtenOn):
		#score = 0
		#if(IsAutoTest(a) != 1 or IsAutoTest(a) == 1):
		#	score = JudgeVoteScore(m, a, sAll, sa, sb, sc, sd, se)
		#else:
		#	pass
		score = JudgeVoteScore(m, a, sAll, sa, sb, sc, sd, se)

		if(score == 1 or score == 2):	# +2, +1 comments
			process.append("P")
		if(score == -1 or score == -2):
			process.append("N")

		#f = IsDefinition(m)
	if(len(time_list) == 0):	# If patchsetId is 1, (PS-M, PS-A)
		if("1" in st):
			process.append("M")
		if("0" in st):
			process.append("A")
	else:						# If patchsetId is 2, 3, .... (Re-PS)
		process.append("Re")

	### Output
	#print "ReviewId LenOfPass status 1 2 3 4 5 6 7 8 9 10"
	print Id,
	print len(process)-1,
	print st,
	for i in range(0,len(process)):
		print process[i],
	print ""
