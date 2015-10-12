# -*- coding: utf-8 -*-
import MeCab

t = MeCab.Tagger("-d /var/lib/mecab/dic/ipadic-utf8")
t.parse('')
n = t.parseToNode("これはテストです。")

while n is not None:
    print(n.surface + '\t' + n.feature)
    n = n.next
