import os
import re
import numpy as np
from tkinter import *
from sklearn.feature_extraction.text import TfidfVectorizer

master = Tk()
def quit():
    master.destroy()

def mean(a):
    return sum(a) / len(a)
expr = re.compile("[a-zA-Z]+")
tokenize = lambda doc: expr.findall(doc)
reviwer_title_dic = {}
reviwer_abstract_dic = {}
reviwer_keyword_dic = {}
def recommend():
	expert_path = e1.get()
	candidate_path = e2.get()
	output_path = e3.get()
	files = next(os.walk(expert_path))[2]
	for i in range(len(files)):
		l = []
		m = []
		f = open(expert_path + "/" + files[i],"r", encoding='utf8',  errors='ignore')
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
		reviwer_Score_dic = sorted(reviwer_Score_dic.items(), key=lambda x: x[1])
		#print(reviwer_Score_dic)	
		g = []
		n = int(len(reviwer_Score_dic) * 0.5)
		for f in range(n):
			item = reviwer_Score_dic.pop()
			key,value = item
			g.append(key)
		reviwer_keyword_dic[files[i][:-4]] = g 
		#print(reviwer_keyword_dic)

	input_title = open(candidate_path + "/titles.txt","r", encoding='utf8',  errors='ignore')
	input_abstract = open(candidate_path + "/abstracts.txt","r", encoding='utf8',  errors='ignore')

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
		#print(writers_name_list)

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
	score_file = open("paper_reviewer_score.txt","w")
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
		jaccard_dic = sorted(jaccard_dic.items(), key=lambda x: x[1])
		#print(jaccard_dic)
		g = []
		n = 10
		for f in range(n):
			item = jaccard_dic.pop()
			key,value = item
			g.append(key)
			score_file.write(str(key) + ":" + str(value) + ",")
		final_dic[index] = g
		score_file.write("\n")
		index += 1
	output = open(output_path + "output.txt", "w")
	for key in final_dic:
		output.write(str(key) + " : ")
		output.write(str(final_dic[key]) + "\n")
	output.close()
	quit()

##########################################################################################
master.geometry("400x250")
master.title('Expert Recommender')
master.resizable(width=False, height=False)
master.configure(bg="#a1dbcd")
Label(master, text="Experts File Path",bg="#a1dbcd",height = 3,width = 30).grid(row=0)
Label(master, text="Candidates File Path",bg="#a1dbcd",height = 3,width = 30).grid(row=1)
Label(master, text="Output File Path",bg="#a1dbcd",height = 3,width = 30).grid(row=2)

e1 = Entry(master)
e2 = Entry(master)
e3 = Entry(master)
e1.grid(row=0, column=1)
e2.grid(row=1, column=1)
e3.grid(row=2, column=1)

Button(master, text='Recommend', command=recommend,fg="#a1dbcd",bg="#383a39", height=2, width=15).grid(row=4, column=1, sticky=W, pady=4)

mainloop( )
