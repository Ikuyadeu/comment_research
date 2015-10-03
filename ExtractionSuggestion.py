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

fv_tf = []					  # ある文書中の単語の出現回数を格納するための配列
fv_df = {}					  # 単語の出現文書数を格納するためのディクショナリ
word_count = []				 # 単語の総出現回数を格納するための配列

fv_tf_idf = []				  # ある文書中の単語の特徴量を格納するための配列

count_flag = {}				 # fv_dfを計算する上で必要なフラグを格納するためのディクショナリ

sql = "select ReviewId, AuthorId, Message "\
	  "from Comment "\
	  "where ReviewId < '100' "\
	  "and AuthorId != '-1' "\
	  "and AuthorId != '1000049';"


csr.execute(sql)
lines = csr.fetchall()
tagger = treetaggerwrapper.TreeTagger(TAGLANG='en',TAGDIR='../treetagger')

txt_num = len(lines)

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
	fv = {}					 # Count of word
	words = 0				   # total count of ward in line

	for word in list(fv_df.keys()):
		count_flag[word] = False

	for tag in tags:
		words += 1
		word = tag.lemma

		if fv.has_key(word):
			fv[word]+=1
		else:
			fv[word]=1

		if word in fv_df.keys(): # fv_dfにキー値がwordの要素があれば
			if count_flag[word] == False: # フラグを確認し，Falseであれば
				fv_df[word] += 1 # 出現文書数を1増やす
				count_flag[word] = True # フラグをTrueにする
		else:				 # fv_dfにキー値がwordの要素がなければ
			fv_df[word] = 1 # 新たにキー値がwordの要素を作り，値として1を代入する
			count_flag[word] = True # フラグをTrueにする

	fv_tf.append(fv)
	word_count.append(words)

for txt_id, fv in enumerate(fv_tf):
	tf = {}
	idf = {}
	tf_idf = {}
	for key in list(fv.keys()):
		tf[key] = float(fv[key]) / word_count[txt_id] # tfの計算
		idf[key] = math.log(float(txt_num) / fv_df[key]) # idfの計算
		tf_idf[key] = (tf[key] * idf[key], tf[key], idf[key], fv[key], fv_df[key]) # tf-idfその他の計算
	tf_idf = sorted(list(tf_idf.items()), key=lambda x:x[1][0], reverse=True) # 得られたディクショナリtf-idfを、tf[key]*idf[key](tf-idf値)で降順ソート(処理後にはtf-idfはリストオブジェクトになっている)
	fv_tf_idf.append(tf_idf)

# 出力
for txt_id, fv in enumerate(fv_tf_idf):
	print ('This is the tf-idf of text', txt_id)
	print ('total words:', word_count[txt_id])
	print

	for word, tf_idf in fv:
		print ('%s\ttf-idf:%lf\ttf:%lf\tidf:%lf\tterm_count:%d\tdocument_count:%d' % (word, tf_idf[0], tf_idf[1], tf_idf[2], tf_idf[3], tf_idf[4])) # 左から順に、単語、tf-idf値、tf値、idf値、その文書中の単語の出現回数、その単語の出現文書数(これは単語ごとに同じ値をとる)
	print
