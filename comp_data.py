import os
import json
import operator
import pprint

current_dir = os.getcwd()
fp_cho_freq = open(current_dir+"/compare/cho_freq.json", mode="r", encoding="utf-8")
fp_joong_freq = open(current_dir+"/compare/joong_freq.json", mode="r", encoding="utf-8")

cho_freq = json.loads(fp_cho_freq.read())
joong_freq = json.loads(fp_joong_freq.read())

#pprint(cho_freq)

joong = dict()
cho = dict()
all = dict()

for key, value in joong_freq.items():
    if key in cho_freq:
        all[key] = value
    elif key not in cho_freq:
        joong[key] = value

for key, value in cho_freq.items():
    if key in joong_freq:
        all[key] += value
    elif key not in joong_freq:
        cho[key] = value

sorted_all_list = sorted(all.items(), key=operator.itemgetter(1), reverse=True)
sorted_cho_list = sorted(cho.items(), key=operator.itemgetter(1), reverse=True)
sorted_joong_list = sorted(joong.items(), key=operator.itemgetter(1), reverse=True)


for item in sorted_all_list:
    print(item)

#print(sorted_all_list)
#print(sorted_cho_list)
#print(sorted_joong_list)



#print(key +" : "+str(value))

