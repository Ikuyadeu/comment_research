# -*- coding: utf-8 -*-
##################
# Author:Yuki Ueda
# CreatedOn: 2015/09/22
# Summary: This program extract the review's suggestion.
##################

import re
import sys
import csv
import math
import MySQLdb
import treetaggerwrapper

# Term Frequency
def tf(word, document):
    return document.words.count(word) / len(document.words)

def n_containing(word, documents):
    return sum(1 for document in documents if word in document)

# Inverse Document Frequency
def idf(word, documents):
    return math.log(len(documents) / (1 + n_containing(word, documents)))

def tfidf(word, document, documents):
    return tf(word, document) * idf(word, documents)




voteComments = [[],[]]
voteComments[0].append(r'Patch Set [1-9]*: Looks good to me, but someone else must approve')
voteComments[0].append(r'Patch Set [1-9]*: Works for me')
voteComments[0].append(r'Patch Set [1-9]*: Verified')
voteComments[0].append(r'Patch Set [1-9]*: Sanity review passed')

voteComments[1].append(r"Patch Set [1-9]*: I would prefer that you didn'*t submit this")
voteComments[1].append(r'Patch Set [1-9]*: Sanity problems found')


### Define Functions
# JudgeVoteScore(m)
# @m:message
######
# If Score is '+1' -> return 1
# If Score is '-1' -> return -1
# If Score isn't '+1' or '-1' -> return 0
######
def JudgeVoteScore(m): # (Regular expression)
    # Score +1
	for comment in voteComments[0]:
		if re.compile(comment).match(m):
			return 1

    # Score -1
	for comment in voteComments[1]:
		if re.compile(comment).match(m):
			return -1

	# No Score
	return 0



cnct = MySQLdb.connect(db="qt",user="root", passwd="password")
csr = cnct.cursor()
time_csr = cnct.cursor()

sql = "select ReviewId, AuthorId, Message "\
	  "from Comment "\
	  "where ReviewId < '100' "\
	  "and AuthorId != '-1' "\
	  "and AuthorId != '1000049';"


csr.execute(sql)
lines = csr.fetchall()
tagger = treetaggerwrapper.TreeTagger(TAGLANG='en',TAGDIR='../treetagger')
fv = {}

for line in lines:
	authorId = line[0]
	reviewId = line[1]
	message = line[2]

	if JudgeVoteScore(message) == 0:
		continue

	message = re.sub(r'\n','',message)
	# delete vote coments
	for comments in voteComments:
		for comment in comments:
			message = re.sub(comment,'',message)
			message = message.replace(comment, '')

	comment = r'\([1-9]* inline comment(s)*\)'
	message = re.sub(comment,'',message)

	if message == '':
		continue

	#set message tag
	tagText = tagger.tag_text(message.decode('utf-8'))
	tags = treetaggerwrapper.make_tags(tagText, exclude_nottags=True)

	#print words
	for tag in tags:
		print(tag.lemma)

        if fv.has_key(tag):
            fv[tag]+=1
        else:
            fv[tag]=1

	print ""
