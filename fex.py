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
    #yahoo data addition
    corp = []
    q = open("q_id.txt","r")
    i = 0
    for l in q:
        if i%2 == 0:
            corp.append(l)
    q.close()
    vectorizer = CountVectorizer(min_df=1,binary=True,stop_words=None)
    X = vectorizer.fit_transform(corpus + corp)
    return X,labels



# vectorizer = CountVectorizer(min_df=1)
# Y = vectorizer.fit_transform(labels)
# bi_vectorizer = CountVectorizer(ngram_range=(1,2),
#                                 token_pattern=r'\b\w+\b', min_df=1)


# X = vectorizer.fit_transform(corpus)
# X_2 = bi_vectorizer.fit_transform(corpus)





if __name__ == '__main__':
    f = codecs.open(os.path.expanduser("~/Data/cqa/uiuc/train_5500.utf8.txt"),encoding='utf-8',errors='ignore')
    X,Y = extract(f)
    f.close()
    # pct_train = .8
    # num_train = int(X.shape[0]*pct_train)
    train_set,test_set = X[:len(labels)], X[len(label):]
    # train_l, test_l = Y[:num_train], Y[num_train:]
    clf = svm.SVC()
    clf.fit(train_set,Y)
    results =  clf.predict(test_set)
    desc_q = []
    i = 0
    for i in results:
        if i == 1:
            desc_q.append(i)
        i += 1
    dec_uid = open('desc_uid',"w")
    print >> desc_uid, desc_q
    # print accuracy_score(results,test_l)
    # print precision_score(results,test_l)
    # print list(results).count(1)
    # clz = svm.SVC(C=1)
    # results =  clz.predict(X)
    # print precision_score(results,Y)


