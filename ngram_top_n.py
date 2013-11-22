from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords
import numpy as np

stopWords = stopwords.words('english')

print "reading topics from 11/19"
with open('topic_list-11-21.txt') as f:
  content = f.readlines()
  for topic in content:
    print "\n"
    print topic.rstrip()
    train_set = []
    with open('data/'+topic.rstrip()+'.txt') as data:
    #with open('data/Catching Fire.txt') as data:
      for tweet in data.readlines():
        train_set.append(tweet)
    vectorizer = TfidfVectorizer(stop_words = stopWords)
    vectorizer.fit(train_set)
    words = ' '.join(vectorizer.get_feature_names())
    idf_vals = vectorizer.transform([words]).toarray()
    words = words.split(' ')
    sorted_indices = np.argsort(idf_vals[0])
    print "first"
    print sorted_indices[0]
    print words[sorted_indices[0]]
    print "second"
    print sorted_indices[1]
    print words[sorted_indices[1]]
    print "third"
    print sorted_indices[2]
    print words[sorted_indices[2]]

