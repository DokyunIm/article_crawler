import os
from gensim.models import Word2Vec

current_dir = os.getcwd()
fp_data = open(current_dir+"/test.csv", mode="r", encoding="utf-8")
data = list()
for line in fp_data:
    line = line.rstrip(",\n")
    words = list()
    for word in line.split(","):
        words.append(word)
    data.append(words)
#print(data)

embedding_model = Word2Vec(data, size=500, window = 4, min_count=10, workers=4, iter=100, sg=1)
result = embedding_model.most_similar(positive=["야채", "감자"], topn=100)

for item in result:
    print(str(item))

