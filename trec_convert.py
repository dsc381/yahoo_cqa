import json
import codecs
import os
import string

f = open("desc_full.json","r")
json_object = json.load(f)
q = codecs.open("yqa.queries","w", encoding='utf-8')
a = codecs.open("answers.dat","w", encoding='utf-8')
q_true = open("yqa.judge","w")

k = 0
f = open(os.path.expanduser("~/IR/katz/cython/stemmer/stops.txt"))
stop_list = f.read().split("\n") + ['ha']
remove_punctuation_map = dict((ord(char), None) for char in string.punctuation)
for i in json_object:
    if len([t  for t in i["answer"].translate(remove_punctuation_map).split(' ') if t.lower() not in stop_list]) < 11:
        continue
    q.write(i["q_uid"]+"\t"+i["question"].replace('\n',' ')+"\n")
    q_true.write(i["q_uid"] +"\t" + str(k)+"\n")
    a.write("<DOC>\n")
    a.write("<DOCNO> "+str(k)+" </DOCNO>\n")
    a.write("<TEXT>\n")
    a.write(i["answer"]+"\n")
    a.write("</TEXT>\n")
    a.write("</DOC>\n")
    repeat = 0
    for ans in i['nbestanswers']:
        #TODO fix bug and then remove thise
        if repeat == 0:
            repeat = 1
            continue
        if len([t  for t in ans.translate(remove_punctuation_map).split(' ') if t.lower() not in stop_list]) < 11:
            continue
        a.write("<DOC>\n")
        a.write("<DOCNO> "+str(k)+" </DOCNO>\n")
        a.write("<TEXT>\n")
        a.write(ans+"\n")
        a.write("</TEXT>\n")
        a.write("</DOC>\n")


