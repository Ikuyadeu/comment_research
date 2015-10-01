# -*- coding: utf-8 -*-
#This is test for TreeTagger
import treetaggerwrapper
tagger = treetaggerwrapper.TreeTagger(TAGLANG='en',TAGDIR='../treetagger')
tagText = tagger.tag_text(u"This is a very short text to tag.")

tags = treetaggerwrapper.make_tags(tagText, exclude_nottags=False)

for tag in tags:
    print(tag.word)
