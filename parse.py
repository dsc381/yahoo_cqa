import os
import sys
import re
from lxml import etree
import nltk.data
import langid

def fast_iter(context, func,model, *args, **kwargs):
    for event, elem in context:
        if elem.tag == 'uid':
            elem_uid = elem
        if elem.tag == 'subject':
            elem_q = elem
        if elem.tag == 'bestanswer':
            elem_a = elem
        if elem.tag == 'nbestanswers':
            elem_na = elem
            func(elem_q,elem_a,elem_uid,elem_na,model,*args,**kwargs)
            elem.clear
            for ancestor in elem.xpath('ancestor-or-self::*'):
                while ancestor.getprevious() is not None:
                    del ancestor.getparent()[0]
    del context

def process_element(elem1,elem2,elem3,elem4,model):
    q_uid = elem4.text
    question = elem1.text
    answer = elem2.text
    nanswers = elem3.text
    answer = answer.replace('<br />','')
    question = answer.replace('<br />','')
    nanswers = [i.replace('<br />','') for i in nanswers]
    answer = re.sub('. *\n','. ',answer)
    nanswer = [re.sub('. *\n','. ', i) for i in nanswers]
    web = ['http','.com','.edu','org','www.']
    nanswer = [n for n in nanswer if n not in web]
    q_length = model.tokenize(question.strip())

    if(len(model.tokenize(answer.strip())) < 5 and len(model.tokenize(answer.strip())) >= 1 and len(model.tokenize(question.strip())) < 2):
        x = 5
    #.xpath('description/text( )')


sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
infile = os.path.expanduser('~/Data/Webscope_L6/small_sample.xml')
context = etree.iterparse(infile)
fast_iter(context, process_element,sent_detector)


