# -*- coding: utf-8 -*-   
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd

corpus = [
    'This is the first document.',
    'This document is the second document.',
    'And this is the third one.',
    'Is this the first document?'
]


tfidf = TfidfVectorizer()
x = tfidf.fit_transform(corpus)


# pandas
df_tfidf = pd.DataFrame(x.toarray(), columns=tfidf.get_feature_names())
print(df_tfidf)