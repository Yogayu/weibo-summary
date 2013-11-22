from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfTransformer
from nltk.corpus import stopwords
import numpy as np

stopWords = stopwords.words('english')
vectorizer = CountVectorizer(ngram_range=(1, 3), stop_words = stopWords)
transformer = TfidfTransformer()

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
    fitted = vectorizer.fit_transform(train_set)
    ngrams =  vectorizer.get_feature_names()
    ngrams_as_arrs = np.asarray(ngrams)
    trainVectorizerArray = fitted.toarray()
    transformer.fit(trainVectorizerArray)
    (h, w) = trainVectorizerArray.shape
    diag = np.diag(np.ones(w))
    idf_vals = transformer.transform(diag).toarray()
    sums = idf_vals.sum(1)
    sorted_indices = np.argsort(sums)
    print "first"
    print sums
    print ngrams_as_arrs[sorted_indices[-1]]
    
    # recalculate 1
    seenWords = stopWords + ngrams_as_arrs[sorted_indices[-1]].split(' ')
    vectorizer2 = CountVectorizer(ngram_range=(1,3), stop_words = seenWords)
    fitted = vectorizer2.fit_transform(train_set)
    ngrams =  vectorizer2.get_feature_names()
    ngrams_as_arrs = np.asarray(ngrams)
    trainVectorizerArray = fitted.toarray()
    transformer.fit(trainVectorizerArray)
    (h, w) = trainVectorizerArray.shape
    diag = np.diag(np.ones(w))
    idf_vals = transformer.transform(diag).toarray()
    sums = idf_vals.sum(1)
    sorted_indices = np.argsort(sums)
    print "second"
    print ngrams_as_arrs[sorted_indices[-1]]
    
    # recalculate 2
    seenWords = seenWords + ngrams_as_arrs[sorted_indices[-1]].split(' ')
    vectorizer3 = CountVectorizer(ngram_range=(1,3), stop_words = seenWords)
    fitted = vectorizer3.fit_transform(train_set)
    ngrams =  vectorizer3.get_feature_names()
    ngrams_as_arrs = np.asarray(ngrams)
    trainVectorizerArray = fitted.toarray()
    transformer.fit(trainVectorizerArray)
    (h, w) = trainVectorizerArray.shape
    diag = np.diag(np.ones(w))
    idf_vals = transformer.transform(diag).toarray()
    sums = idf_vals.sum(1)
    print sums
    sorted_indices = np.argsort(sums)
    print "third"
    print ngrams_as_arrs[sorted_indices[-1]]
    


