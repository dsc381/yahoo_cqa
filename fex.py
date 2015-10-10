import os
import codecs
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.metrics import accuracy_score, precision_score

labels = []

def s_extract(f):
    dict = {}
    corpus = []

def extract(f):
    def sample(f):
        hits = []
        misses = []
        for l in f:
            if "DESC" in l:
                hits.append(l)
            else:
                misses.append(l)
        f = []
        i = 0
        for ex in hits:
            f.append(ex)
            f.append(misses[i])
            i += 1
        return f

    corpus = []
    category = []
    labels = []
    f = sample(f)
    for l in f:
        temp = l.split(' ',1)
        corpus.append(temp[1:][0])
        category.append(temp[0])

    for line in category:
        if "DESC" in line:
            labels.append(1)
        else:
            labels.append(0)
    vectorizer = CountVectorizer(min_df=1,binary=True,stop_words=None)
    X = vectorizer.fit_transform(corpus)
    return X,labels

f = codecs.open(os.path.expanduser("~/Data/cqa/uiuc/train_5500.utf8.txt"),encoding='utf-8',errors='ignore')
X,Y = extract(f)
f.close()
pct_train = .8
num_train = int(X.shape[0]*pct_train)
train_set,test_set = X[:num_train], X[num_train:]
train_l, test_l = Y[:num_train], Y[num_train:]


# vectorizer = CountVectorizer(min_df=1)
# Y = vectorizer.fit_transform(labels)
# bi_vectorizer = CountVectorizer(ngram_range=(1,2),
#                                 token_pattern=r'\b\w+\b', min_df=1)


# X = vectorizer.fit_transform(corpus)
# X_2 = bi_vectorizer.fit_transform(corpus)


clf = svm.SVC()
clf.fit(train_set,train_l)
results =  clf.predict(test_set)
print accuracy_score(results,test_l)
print precision_score(results,test_l)
print len(results)
clz = svm.SVC(C=1)
clz.fit(X,Y)
results =  clz.predict(X)
print precision_score(results,Y)

