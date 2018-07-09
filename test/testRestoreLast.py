import json

with open('../config/saveLastStation.json', 'r') as f:
    restore = json.load(f)

#load the data
freq = restore['freq']
idx  = restore['index']

print "freq="+freq
print "index="+idx


