import json

f = open('iri_data.json')
  

data = json.load(f)

new_data = {}

for i in data:
    if i['Team Number'] in new_data.keys():
        new_data[i['Team Number']].append(i)
    else:
        new_data[i['Team Number']] = [i]



json_object = json.dumps(new_data, indent=4)
 
# Writing to sample.json
with open("iri_data.json", "w") as outfile:
    outfile.write(json_object)