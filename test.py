from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import numpy as np

documents = (
"The sky is blue",
"The sun is bright",
"The sun in the sky is bright",
"We can see the shining sun, the bright sun"
)

stopWords = stopwords.words('english')

vectorizer = TfidfVectorizer(ngram_range=(1,1), stop_words = stopWords)
vectorizer.fit(documents)
words =  vectorizer.get_feature_names()
test_set = []
for word in words:
  test_set.append(str(word))
print test_set
print vectorizer.transform(test_set).toarray().sum(1)
