# coding: utf-8
import spacy
from urllib import request
from bs4 import BeautifulSoup
import bs4
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from sumy.summarizers.lex_rank import LexRankSummarizer


# Spacy
nlp = spacy.load('ja_ginza')

#doc = nlp('これがライブラリの実験です')
#for sent in doc.sents:
#    for token in sent:
#        print(token.i, token.orth_, token.lemma_, token.pos_, token.tag_, token.dep_, token.head.i)
#   print('EOS')

# the target book url
url = 'https://www.aozora.gr.jp/cards/001403/files/49986_37674.html'
html = request.urlopen(url)
soup = BeautifulSoup(html, 'html.parser')
body = soup.select('.main_text')

text = ''
for b in body[0]:
    if type(b) == bs4.element.NavigableString:
        text += b
        continue
    # only kanji
    text += ''.join([e.text for e in b.find_all('rb')])

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


# Sumy
# 連結したcorpusを再度tinysegmenterでトークナイズさせる
parser = PlaintextParser.from_string(''.join(corpus), Tokenizer('japanese'))

# スペースも1単語として認識されるため、ストップワードにすることで除外する
summarizer = LexRankSummarizer()
summarizer.stop_words = [' ']  

# sentencres_countに要約後の文の数を指定します。
summary = summarizer(document=parser.document, sentences_count=3)

# 元の文を表示
for sentence in summary:
    print(originals[corpus.index(sentence.__str__())])