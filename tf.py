# -*- coding: utf-8 -*-

import os
import MeCab
import sys
import re
from xml.dom.minidom import parse
from math import log
import spacy

# Spacy
nlp = spacy.load('ja_ginza')

# ファイル読み込み
DIR = r"/Users/yamato/Desktop/data"
f = os.listdir(DIR)

N = 2 #何個めの文書
posts = [open(os.path.join(DIR, f[N])).read()]
text = ','.join(posts)

# レンマ化
corpus = []
originals = []
doc = nlp(text)
for s in doc.sents:
    originals.append(s)
    tokens = []
    for t in s:
        tokens.append(t.lemma_)
    corpus.append(' '.join(tokens))

# Mecab辞書を用いて名詞抽出
noun = []
tagger = MeCab.Tagger( "-Ochasen" )
node = tagger.parseToNode( text)
while node:
    if node.feature.split(",")[0] == "名詞":
        replace_node = re.sub( re.compile( "[!-/:-@[-`{-~]" ), "", node.surface )
        if replace_node != "" and replace_node != " ":
            noun.append( replace_node )
    node = node.next

# TF：文書中に出てくる頻度の多いワードを抽出
tf = {}
for word in noun:
    try:
        tf[word] = tf[word] + 1
    except KeyError:
        tf[word] = 1

temp = sorted( tf.items(), key=lambda x:x[1], reverse=True )
for k,v in temp:
    print (k,v)