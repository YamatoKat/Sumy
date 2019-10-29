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

# textの入力
text = 'かつおぶしはどういうふうに選択し、どういうふうにして削るか。まず、かつおぶしの良否の簡単な選択法をご披露しよう。よいかつおぶしは、かつおぶしとかつおぶしとを叩き合わすと、カンカンといってまるで拍子木か、ある種の石を鳴らすみたいな音がするもの。'

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
summary = summarizer(document=parser.document, sentences_count=1)

# 元の文を表示
for sentence in summary:
    print(originals[corpus.index(sentence.__str__())])