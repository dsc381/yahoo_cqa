import json
import codecs

f = open("desc_full.json","r")
json_object = json.load(f)
q = codecs.open("yqa.queries","w", encoding='utf-8')
a = codecs.open("answers.dat","w", encoding='utf-8')
q_true = open("yqa.judge","w")

k = 0
for i in json_object:
    q.write(i["q_uid"]+"\t"+i["question"]+"\n")
    q_true.write(i["q_uid"] +"\t" + str(k)+"\n")
    a.write("<docno>"+str(k)+"</docno>\n")
    a.write("<text>\n")
    a.write(i["answer"]+"\n")
    a.write("</text>\n")
    k += 1
    repeat = 0
    for ans in i['nbestanswers']:
        #TODO fix bug and then remove thise
        if repeat == 0:
            repeat += 1
            continue
        a.write("<docno>"+str(k)+"</docno>\n")
        k += 1
        a.write("<text>\n")
        a.write(ans+"\n")
        a.write("</text>\n")


