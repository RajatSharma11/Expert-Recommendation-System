import os
import re
import numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
def mean(a):
    return sum(a) / len(a)
input_path = "title_abstract_data"
expr = re.compile("[a-zA-Z]+")
tokenize = lambda doc: expr.findall(doc)
files = next(os.walk(input_path))[2]
reviwer_title_dic = {}
reviwer_abstract_dic = {}
reviwer_keyword_dic = {}
for i in range(len(files)):
	l = []
	m = []
	f = open("title_abstract_data/" + files[i],"r", encoding='utf8',  errors='ignore')
	for line in f:
		s = line.split("|")
		l.append(s[0])
		if(len(s[1]) > 1):
			m.append(s[1])
	reviwer_title_dic[files[i][:-4]] = l
	reviwer_abstract_dic[files[i][:-4]] = m
	while("" in m):
		m.remove("")
	if len(m) > 0:
		sklearn_tfidf = TfidfVectorizer(norm='l2',min_df=0, use_idf=True, smooth_idf=True, sublinear_tf=False, tokenizer=tokenize)
		sklearn_representation = sklearn_tfidf.fit_transform(m)
	reviwer_Score_dic = {}
	vect = np.mean(sklearn_representation.todense(), axis=0).tolist()
	for key in sklearn_tfidf.vocabulary_:
		reviwer_Score_dic[key] = vect[0][sklearn_tfidf.vocabulary_[key]]
	reviwer_Score_dic = sorted(reviwer_Score_dic.items(), key=lambda x: x[1],reverse = True)	
	g = []
	n = int(len(reviwer_Score_dic) * 0.2)
	for f in range(n):
		item = reviwer_Score_dic.pop()
		key,value = item
		g.append(key)
	reviwer_keyword_dic[files[i][:-4]] = g 

input_title = open("Expert_Finding_Data/titles.txt","r", encoding='utf8',  errors='ignore')
input_abstract = open("Expert_Finding_Data/abstracts.txt","r", encoding='utf8',  errors='ignore')

l = []
m = []
v = 1		# for indexing in input_dic
writers_name = []
writers_name_list = []
input_dic = {}
for line in input_title:
	s = line.split("/")
	l.append(s[0])
	writers_name = "".join(s[1]).split("and")
	for i in range(len(writers_name)):
		if("\n" in writers_name[i]):
			writers_name[i] = writers_name[i][:-1]
		writers_name[i] = writers_name[i].strip(" ")
	while("" in writers_name):
		writers_name.remove("")
	writers_name_list.append(set(writers_name))
	print(writers_name_list)

for line in input_abstract:
	s = l[v - 1] + line 
	input_dic[v] = tokenize(s) 
	v += 1

def jaccard_similarity(query, document):
    intersection = set(query).intersection(set(document))
    union = set(query).union(set(document))
    return len(intersection)/len(union)


index = 1
final_dic = {}
for name in writers_name_list:
	jaccard_dic = {}
	for reviewer in reviwer_keyword_dic:
		if(len(name.intersection(set(reviewer))) > 0):
			continue;
		else:
			#print(type(input_dic[index]))
			#print(type(reviwer_keyword_dic[reviewer]))
			jaccard_dic[reviewer] = jaccard_similarity(input_dic[index],reviwer_keyword_dic[reviewer])
	#print(jaccard_dic)
	jaccard_dic = sorted(jaccard_dic.items(), key=lambda x: x[1],reverse = True)
	#print(jaccard_dic)
	g = []
	n = 10
	for f in range(n):
		item = jaccard_dic.pop()
		key,value = item
		g.append(key)
	final_dic[index] = g
	index += 1
print(final_dic)



	


