json_object = json.load("q-a_pair.json")
q = open("yqa.queries","w")
a = open("answers.dat","w")
q_true = open("yqa.judge","w")

k = 0
for i in json_object:
    q.write(i["q_uid"]+"\t"+i["question"]+"\n")
    a.write("<docno>"+str(k)+"</docno>\n")
    k += 1
    a.write("<text>\n")
    a.write(i["answer"]+"\n")
    a.write("</text>\n")
    for ans in i['nbestanswers']:
        a.write("<docno>"+str(k)+"</docno>\n")
        k += 1
        a.write("<text>\n")
        a.write(ans+"\n")
        a.write("</text>\n")


