import os
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
    for event, elem in context:
        if elem.tag == 'uri':
            elem_uid = elem
        if elem.tag == 'subject':
            elem_q = elem
        if elem.tag == 'bestanswer':
            elem_a = elem
        if elem.tag == 'nbestanswers':
            elem_na = elem
            func(elem_q,elem_a,elem_uid,elem_na,model,result)
            elem.clear
            for ancestor in elem.xpath('ancestor-or-self::*'):
                while ancestor.getprevious() is not None:
                    del ancestor.getparent()[0]
    del context
    return result

def process_element(elem1,elem2,elem3,elem4,model,result):
    q_uid = elem3.text
    question = elem1.text
    answer = elem2.text
    nanswers = [e.text for e in elem4]

    answer = answer.replace('<br />','')
    question = question.replace('<br />','')
    nanswers = [i.replace('<br />','') for i in nanswers]
    answer = re.sub('\n','. ',answer)
    nanswers = [re.sub('\n','. ', i) for i in nanswers]
    web = ['http','.com','.edu','org','www.']
    nanswers = [n for n in nanswers if n not in web]
    nanswers = [n for n,lang in zip(nanswers,eval_language(nanswers)) if lang == 'en']

    q_length = len(model.tokenize(question.strip()))
    a_length = len(model.tokenize(answer.strip()))
    print question
    print q_length == 1

    if (q_length == 1) and (a_length > 1) and (a_length < 5) and eval_language(question) == 'en' and eval_language(answer) == 'en':
        if sys.argv[1] == "svm":
            result.append(q_uid)
            result.append(question)
        else:
            print "hi"
            result.append(q_uid)
            result.append(question)
            result.append(answer)
            result.append(str(nanswers))


    #.xpath('description/text( )')


sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
infile = os.path.expanduser('~/Data/Webscope_L6/small_sample.xml')
context = etree.iterparse(infile)
result = fast_iter(context, process_element,sent_detector)
outfile = open("test.txt",'w')
print >>  outfile, '\n'.join(result)




