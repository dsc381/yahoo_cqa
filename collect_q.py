import ast

def convert(s):
    output = []
    for l in s:
        output.append(l.rstrip('\n'))
    return output
q = open("desc_d","r")
f = open("q_id.txt")
q_ids = convert(f)
f.close()
labels = convert(q)
q.close()
correct = []
for l,d in zip( labels,xrange(0,len(labels)-1)):
    if l == "1":
        correct.append(q_ids[d])
        correct.append(q_ids[d+1])
outfile = open("correct_uid.txt","w")
print >>  outfile, '\n'.join(correct)

