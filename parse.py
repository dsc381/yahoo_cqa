import os
import io, json
from bisect import bisect_left
import codecs
import sys
import re
from lxml import etree
import nltk.data
import langid

def eval_language(l):
    if type(l) is list:
        temp =  map(langid.classify,l)
        return [t[0] for t in temp]
    else:
        return langid.classify(l)[0]

def fast_iter(context, func,model, *args, **kwargs):
    result = []
    if sys.argv[1] == "clean":
        uids = get_good_uid()

    i = 0
    for event, elem in context:
        if elem.tag == 'uri':
            elem_uid = elem
        if elem.tag == 'subject':
            elem_q = elem
        if elem.tag == 'bestanswer':
            elem_a = elem
        if elem.tag == 'nbestanswers':
            elem_na = elem
        if elem.tag == 'maincat':
            elem_mcat = elem

            if i%100000 == 0:
                print i
            i+=1
            if sys.argv[1] == 'clean':
                func(elem_q,elem_a,elem_uid,elem_na,result,uids)
            else:
                func(elem_q,elem_a,elem_uid,elem_na,elem_mcat,model,result)
            elem.clear
            for ancestor in elem.xpath('ancestor-or-self::*'):
                while ancestor.getprevious() is not None:
                    del ancestor.getparent()[0]
    del context
    return result

def clean_questions(elem1,elem2,elem3,result,uids):
    q_uid = elem3.text
    question = elem1.text
    answer = elem2.text
    nanswers = [e.text for e in elem4]
    if binary_search(uids,int(q_uid)) > -1:
        result.append({'q_uid':q_uid,
            'question':question,
            'answer':answer,
            'nbestanswers':nanswers})


def process_element(elem1,elem2,elem3,elem4,elem5,model,result):
    q_uid = elem3.text
    mcat = elem5.text
    question = elem1.text
    q_length = len(model.tokenize(question.strip()))
    question = question.replace('<br />','')
    answer = elem2.text
    nanswers = [e.text for e in elem4]
    answer = answer.replace('<br />','')
    nanswers = [i.replace('<br />','') for i in nanswers]
    answer = re.sub('\n','. ',answer)
    nanswers = [re.sub('\n','. ', i) for i in nanswers]

    a_length = len(model.tokenize(answer.strip()))

    if (q_length == 1) and (a_length > 1) and (a_length < 5):
        if sys.argv[1] == "svm":
            result.append({'q_uid':q_uid,'question':question})
        else:
            result.append({'q_uid':q_uid,
                           'main_cat':mcat,
             'question':question,
             'answer':answer,
             'nbestanswers':nanswers})


            #TODO fix
def remove(json_obj,pruned):
    for entry in json_obj:
        answer = entry['answer']
        nanswers = entry['nbestanswers']
        question = entry['question']
        web = ['http','.com','.edu','org','www.']
        nanswers = [n for n in nanswers if n not in web]
        nanswers = [n for n,lang in zip(nanswers,eval_language(nanswers)) if lang == 'en']
        if eval_language(question) == 'en' and eval_language(answer) == 'en' and (not any([w in question for w in web]) or not any([w in answer for w in web])):
            entry['nbestanswers'] = nanswers
            pruned.append(entry)
    #.xpath('description/text( )')


def binary_search(a, x, lo=0, hi=None):   # can't use a to specify default for hi
    hi = hi if hi is not None else len(a) # hi defaults to len(a)   
    pos = bisect_left(a,x,lo,hi)          # find insertion position
    return (pos if pos != hi and a[pos] == x else -1) # don't walk off the end

def get_good_uid():
    good_id = []
    q = open("correct_uid")
    for l in q:
        try:
            temp = int(l)
            good_id.append(temp)
        except:
            continue
    good_id = sorted(good_id)



if sys.argv[1] == "svm":
    fname = 'q_id.json'
    func = process_element
elif sys.argv[1] == "parse":
    fname = 'q-a_pair.json'
    func = process_element
elif sys.argv[1] == "clean":
    uids = get_good_uid()
    fname = 'cleaned_cqa.json'
    func = clean_questions

sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
infile = os.path.expanduser(sys.argv[2])
context = etree.iterparse(infile)
result = fast_iter(context,func ,sent_detector)

with open(fname, 'w') as f:
  json.dump(result,f)





