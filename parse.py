import os
import sys
import re
from lxml import etree
import nltk.data

def fast_iter(context, func,model, *args, **kwargs):
    for event, elem in context:
        if elem.tag == 'subject':
            elem_q = elem
        if elem.tag == 'bestanswer':
            elem_a = elem
            func(elem_q,elem_a,model,*args,**kwargs)
            elem.clear
            for ancestor in elem.xpath('ancestor-or-self::*'):
                while ancestor.getprevious() is not None:
                    del ancestor.getparent()[0]
    del context

def process_element(elem1,elem2,model):
    question = elem1.text
    answer = elem2.text
    answer = answer.replace('<br />','')
    question = answer.replace('<br />','')
    answer = re.sub('. *\n','. ',answer)
    if(len(model.tokenize(answer.strip())) < 5 and 5==5):
        print "hi"
    
    print '\n'
    #.xpath('description/text( )')


sent_detector = nltk.data.load('tokenizers/punkt/english.pickle')
infile = os.path.expanduser('~/Data/Webscope_L6/small_sample.xml')
context = etree.iterparse(infile)
fast_iter(context, process_element,sent_detector)


