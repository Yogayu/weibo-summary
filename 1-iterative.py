from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from nltk.corpus import stopwords
import numpy as np

stopWords = stopwords.words('english')
vectorizer = CountVectorizer(stop_words = stopWords)
transformer = TfidfTransformer()

print "reading topics from 11/21"
with open('topic_list-11-21.txt') as f:
  content = f.readlines()
  for topic in content:
    print "\n"
    print topic.rstrip()
    train_set = []
    with open('data/'+topic.rstrip()+'.txt') as data:
      for tweet in data.readlines():
        train_set.append(tweet)
    trainVectorizerArray = vectorizer.fit_transform(train_set).toarray()
    transformer.fit(trainVectorizerArray)
    sums = transformer.transform(trainVectorizerArray).toarray().sum(1)
    sorted_indices = np.argsort(sums)
    print "first"
    print train_set[sorted_indices[-1]]
    
    # recalculate 1
    seenWords = stopWords + train_set[sorted_indices[-1]].split(' ')
    vectorizer2 = CountVectorizer(stop_words = seenWords)
    trainVectorizerArray = vectorizer2.fit_transform(train_set).toarray()
    transformer2 = TfidfTransformer()
    transformer2.fit(trainVectorizerArray)
    sums = transformer2.transform(trainVectorizerArray).toarray().sum(1)
    sorted_indices = np.argsort(sums)
    print "second"
    print train_set[sorted_indices[-1]]

 
    # recalculate 2
    seenWords2 = seenWords + train_set[sorted_indices[-1]].split(' ')
    vectorizer3 = CountVectorizer(stop_words = seenWords2)
    trainVectorizerArray = vectorizer3.fit_transform(train_set).toarray()
    transformer3 = TfidfTransformer()
    transformer3.fit(trainVectorizerArray)
    sums = transformer3.transform(trainVectorizerArray).toarray().sum(1)
    sorted_indices = np.argsort(sums)
    print "third"
    print train_set[sorted_indices[-1]]

 

