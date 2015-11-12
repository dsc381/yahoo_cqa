import json

f = open('desc_full.json')
obj = json.load(f)
for i in obj:
    print i['question']
