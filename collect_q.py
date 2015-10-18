import ast
import json
import langid

def eval_language(l):
    if type(l) is list:
        temp =  map(langid.classify,l)
        return [t[0] for t in temp]
    else:
        return langid.classify(l)[0]
def convert(s):
    output = []
    for l in s:
        output.append(l.rstrip('\n'))
    return output
svm = open("desc_d","r")
q = open("q-a_pair.json","r")

questions = json.load(q)
labels = convert(svm)
svm.close()
q.close()
web = ['http','.com','.edu','org','www.']

output = []
i = 0
for label,entry in zip( labels,questions):
    if i%100000 == 0:
        print i
    i += 1
    if label == "1":
        answer = entry['answer']
        nanswers = entry['nbestanswers']
        question = entry['question']
        nanswers = [n for n in nanswers if n not in web]
        nanswers = [n for n,lang in zip(nanswers,eval_language(nanswers)) if lang == 'en']
        if eval_language(question) == 'en' and eval_language(answer) == 'en' and (not any([w in question for w in web]) and not any([w in answer for w in web])) and entry['main_cat'] != 'Family':
            entry['nbestanswers'] = nanswers
            output.append(entry)

with open("desc_full.json", 'w') as f:
  json.dump(output,f)

