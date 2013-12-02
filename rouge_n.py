from sklearn.feature_extraction.text import CountVectorizer
from nltk.corpus import stopwords
import sys

print "rouge score for files " + sys.argv[1] + " and " + sys.argv[2]

stopWords = stopwords.words('english')

file1 = []
with open(sys.argv[1]) as data:
  for tweet in data.readlines():
    if len(tweet) > 1:
      file1.append(tweet)

file2 = []
with open(sys.argv[2]) as data:
  for tweet in data.readlines():
    if len(tweet)>1:
      file2.append(tweet)

for x in range(0, min(len(file1), len(file2))):
  vectorizer = CountVectorizer(ngram_range=(1, 5), stop_words = stopWords)
  vectorizer.fit(file1)

  vectorizer2 = CountVectorizer(ngram_range=(1, 5), stop_words = stopWords)
  vectorizer2.fit(file2)
  intersect = set(vectorizer.get_feature_names()) & set(vectorizer2.get_feature_names())
  print float(len(intersect))/len(vectorizer2.get_feature_names())
  print min(len(file1), len(file2))
  file1.pop()
  file2.pop()
