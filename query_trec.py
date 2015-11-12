import json
import codecs
q = codecs.open("yqa.queries","r",encoding='utf-8')
data = {
    "requested": 1000,
"queries" : []
}
for line in q:
    line_data = line.split("\t")
    data['queries'].append({'number':line_data[0],
                            'text':line_data[1].strip('?\n')})
with open('query-file', 'w') as outfile:
    json.dump(data, outfile)

