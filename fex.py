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

    def get_labels(name,f):
        labels[[],[],[],[],[]]
        for l in f:
            temp = l.split(' ',1)
            corpus.append(temp[1:][0])
            category.append(temp[0])
        for line in category:
            if "HUM:" in line:
                labels[0].append(1)
            else:
                labels[0].append(0)
            if "ENTY:" in line:
                labels[1].append(1)
            else:
                labels[1].append(0)
            if "NUM:" in line:
                labels[2].append(1)
            else:
                labels[2].append(0)
            if "LOC" in line:
                labels[3].append(1)
            else:
                labels[3].append(0)
            if "ABB" in line:
                labels[4].append(1)
            else:
                labels[4].append(0)
        return corpus,labels

    def desc_lables(f):
        for l in f:
            temp = l.split(' ',1)
            corpus.append(temp[1:][0])
            category.append(temp[0])
        for line in category:
            if "DESC" in line:
                labels.append(1)
            else:
                labels.append(0)
        return corpus,labels

    corpus = []
    Y = []
    fi = sample(f)
    corpus,Y = get_labels(name,f)
    d_corpus,d_labels = desc_lables(fi)
    Y.append(d_labels)
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
    miniX = vectorizer.fit_transform(d_corpus+corp)
    return X,miniX,Y



# vectorizer = CountVectorizer(min_df=1)
# Y = vectorizer.fit_transform(labels)
# bi_vectorizer = CountVectorizer(ngram_range=(1,2),
#                                 token_pattern=r'\b\w+\b', min_df=1)


# X = vectorizer.fit_transform(corpus)
# X_2 = bi_vectorizer.fit_transform(corpus)





if __name__ == '__main__':
    f = codecs.open(os.path.expanduser("~/Data/cqa/uiuc/train_5500.utf8.txt"),encoding='utf-8',errors='ignore')
    X,miniX,Y = extract(f)
    f.close()
    train_set,d_train_set = X[:len(labels[0])], miniX[:len(labels[-1])]
    test_set,d_test_set = X[len(labels[0]):], miniX[len(labels[-1]):]
    # train_l, test_l = Y[:num_train], Y[num_train:]
    svms = []
    for i in xrange(6):
        svms.append(svm.SVC())
    for sv,i in zip(svms,xrange(6)):
        if i == 5:
            sv.fit(d_train_set,Y[i])
        sv.fit(train_set,Y[i])
    results = []
    for sv in svms:
        if i ==5:
            results.append(sv.predict(d_test_set))
        results.append(sv.predict(test_set))
    current = np.ones(len(results[1]))
    for res in results[:-1]:
        current = np.logical_and(res)
    current = np.logical_or(results[-1].resize(len(current)),np.invert(current))

    # desc_q = []
    # i = 0
    # for i in results:
    #     if i == 1:
    #         desc_q.append(i)
    #     i += 1
    numpy.savetxt("desc_uid",current, fmt= "%d")
    # print accuracy_score(results,test_l)
    # print precision_score(results,test_l)
    # print list(results).count(1)
    # clz = svm.SVC(C=1)
    # results =  clz.predict(X)
    # print precision_score(results,Y)


