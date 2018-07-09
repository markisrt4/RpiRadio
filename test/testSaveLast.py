import json

save = {'freq': '97100000', 'index': '1'}

with open('../config/saveLastStation.json', 'w') as f:
    json.dump(save, f)
