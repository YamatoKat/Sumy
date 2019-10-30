import os




# 読み込み
DIR = r"../sumy/data"
posts = [open(os.path.join(DIR, f)).read() for f in os.listdir(DIR)]
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


print(len(corpus))
print(len(originals))


import MeCab
import sys

# t = MeCab.Tagger('-Ochasen')
# print(t.parse(text))



noun = []
tagger = MeCab.Tagger( "-Ochasen" )
node = tagger.parseToNode( text)
while node:
    if node.feature.split(",")[0] == "名詞":
        replace_node = re.sub( re.compile( "[!-/:-@[-`{-~]" ), "", node.surface )
        if replace_node != "" and replace_node != " ":
            noun.append( replace_node )
    node = node.next


return noun




# TF-IDF
import re
from xml.dom.minidom import parse
from math import log

def getNoun(words):
   noun = []
   tagger = MeCab.Tagger( "-Ochasen" )
   node = tagger.parseToNode( words.encode( "utf-8" ) )
   while node:
      if node.feature.split(",")[0] == "名詞":
         replace_node = re.sub( re.compile( "[!-/:-@[-`{-~]" ), "", node.surface )
         if replace_node != "" and replace_node != " ":
            noun.append( replace_node )
      node = node.next
   return noun

def getTopKeywords(TF,n):
   list = sorted( TF.items(), key=lambda x:x[1], reverse=True )
   return list[0:n]

def calcTFIDF( N,TF, DF ):
   tfidf = TF * log( N / DF )
   return tfidf

# 文書数
N = 5 
tf = {}
df = {}
df_list = []
max=len(noun)

for word in noun:
    try:
        tf[word] = tf[word] + 1
    except KeyError:
        tf[word] = 1

for word in noun:
    try:
        if word in df_list: 
            continue
        df[word] = df[word] + 1
    except KeyError:
        df[word] = 1

tfidf = {}
for k,v in getTopKeywords( tf, max ):
    tfidf[k] = calcTFIDF(N,tf[k],df[k])
for k,v in getTopKeywords( tfidf, max ):
    print (k,v)




#要約文を抽出
# Sumy
# 連結したcorpusを再度tinysegmenterでトークナイズさせる
parser = PlaintextParser.from_string(''.join(corpus), Tokenizer('japanese'))

# スペースも1単語として認識されるため、ストップワードにすることで除外する
summarizer = LexRankSummarizer()
summarizer.stop_words = [' ']  
summarizer.stop_words = ['＊']  

# sentencres_countに要約後の文の数を指定します。
summary = summarizer(document=parser.document, sentences_count=1)

# 元の文を表示
for sentence in summary:
    print(originals[corpus.index(sentence.__str__())])


