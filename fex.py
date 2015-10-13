import os
import numpy
import codecs
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn import svm
from sklearn.metrics import accuracy_score, precision_score


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
        fi = []
        i = 0
        for ex in hits:
            fi.append(ex)
            fi.append(misses[i])
            i+=1
            fi.append(misses[i])
            i += 1
        return fi

    def get_labels(f):
        '''assumes file is LABEL: text'''
        labels = [[] for i in xrange(5)]
        category = []
        corpus = []
        for l in f:
            temp = l.split(' ',1)
            corpus.append(temp[1:][0])
            category.append(temp[0])
        i = 0
        for line in category:
            if "HUM" in line:
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

    def desc_lables(fi):
        '''As DESC is so low in represented, we use random sampling to build SVM'''
        corpus = []
        category = []
        labels =[]
        for l in fi:
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
    corpus,Y = get_labels(f)
    f.seek(0)
    fi = sample(f)
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
    vectorizer = CountVectorizer(min_df=1,stop_words=None)
    X = vectorizer.fit_transform(corpus+corp)
    miniX = vectorizer.fit_transform(d_corpus+corp)
    return X,miniX,Y




if __name__ == '__main__':
    stop_w = ['a',
    'about','above','after','again','against',
    'all','am','an','and','any','are','aren\'t',
    'as','at','be','because','been','before','being',
    'below','between','both','but','by','can\'t','cannot',
    'could','couldn\'t','did','didn\'t','do','does','doesn\'t',
    'doing','don\'t','down','during','each','few','for',
    'from','further','had','hadn\'t','has','hasn\'t','have',
    'haven\'t','having','he','he\'d','he\'ll','he\'s','her',
    'here','here\'s','hers','herself','him','himself','his',
    'i','i\'d','i\'ll','i\'m','i\'ve','if','in',
    'into','is','isn\'t','it','it\'s','its','itself',
    'let\'s','me','more','most','mustn\'t','my','myself',
    'no','nor','not','of','off','on','once',
    'only','or','other','ought','our','ours','ourselves',
    'out','over','own','same','shan\'t','she','she\'d',
    'she\'ll','she\'s','should','shouldn\'t','so','some','such',
    'than','that','that\'s','the','their','theirs','them',
    'themselves','then','there','there\'s','these','they','they\'d',
    'they\'ll','they\'re','they\'ve','this','those','through','to',
    'too','under','until','up','very','was','wasn\'t',
    'we','we\'d','we\'ll','we\'re','we\'ve','were','weren\'t',
    'while','with','won\'t','would','wouldn\'t','you','you\'d',
    'you\'ll','you\'re','you\'ve','your','yours','yourself','yourselves']


    f = codecs.open(os.path.expanduser("~/Data/cqa/uiuc/train_5500.utf8.txt"),encoding='utf-8',errors='ignore')
    X,miniX,Y = extract(f)
    f.close()
    train_set,d_train_set = X[:len(Y[0])], miniX[:len(Y[5])]
    test_set,d_test_set = X[len(Y[0]):], miniX[len(Y[5]):]
    svms = []
    for i in xrange(6):
        svms.append(svm.LinearSVC())
    print "training"
    for sv,i in zip(svms,xrange(6)):
        print str(i)+" /5"
        if i == 5:
            sv.fit(d_train_set,Y[i])
        else:
            sv.fit(train_set,Y[i])
        #     sv.fit(d_train_set,Y[i])
        # else:
        #     sv.fit(train_set,Y[i])
    results = []
    print "evaulating"
    for sv,i in zip(svms,xrange(6)):
        print str(i)+" /5"
        if i ==5:
            results.append(sv.predict(d_test_set))
            print d_test_set.shape[0]
            print results[5].shape
        else:
            results.append(sv.predict(test_set))
    current = numpy.zeros(len(results[1]))
    numpy.savetxt("desc_d",results[5].T, fmt= "%d")
    for res in zip(results[:-1]):
        current = numpy.logical_or(res,current)
    current = numpy.logical_or(results[5].resize(len(current)),numpy.invert(current))

    # desc_q = []
    # i = 0
    # for i in results:
    #     if i == 1:
    #         desc_q.append(i)
    #     i += 1
    numpy.savetxt("desc_uid",current.T, fmt= "%d")
    # print list(results).count(1)
    # clz = svm.SVC(C=1)
    # results =  clz.predict(X)
    # print precision_score(results,Y)


