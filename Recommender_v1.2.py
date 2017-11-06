import os
import re
import numpy as np
from numpy import linalg as LA
import math
from tkinter import *
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.cluster import KMeans

master = Tk()
def quit():
    master.destroy()

def sse(listVect,mean):
    sum = 0 
    for i in range(len(listVect)):
        sum = sum + (LA.norm(np.array(listVect[i]) - np.array(mean)))**2
    return sum / len(listVect)
    
input_path="title_abstract_data"
expr = re.compile("[a-zA-Z]+")
tokenize = lambda doc: expr.findall(doc)
def recommend():
    expert_path = e1.get()
    candidate_path = e2.get()
    output_path = e3.get()
    files = next(os.walk(expert_path))[2]
    reviwerDic = {}
    for i in range(len(files)):
        f = open("title_abstract_data/" + files[i],"r",encoding = "utf8",errors = "ignore")
        Abs = []
        noAbs = ""
        for line in f:
            s = line.split("|")
            if(s[1][:-1].strip() == ""):
                noAbs=noAbs + s[0]
                continue
            Abs.append((s[0] + s[1])[:-1])
        if(noAbs != ""):
            Abs.append(noAbs)
           
        sklearn_tfidf = TfidfVectorizer(norm = 'l2',min_df = 0, use_idf = True, smooth_idf = True, sublinear_tf = False, tokenizer = tokenize)
        sklearn_representation = sklearn_tfidf.fit_transform(Abs)
        matrix=np.array(sklearn_representation.todense())
        sseSum=math.inf
        finalLabel=[]
        numClusters=0
        for k in range(len(Abs)):
            kmeans = KMeans(n_clusters=k+1, random_state=0).fit(matrix)
            labels=(kmeans.labels_).tolist()
            labelDic={}
            for j in range(k+1):
                labelDic[j+1]=[]
            for j in range(len(labels)):
                labelDic[labels[j]+1]=labelDic[labels[j]+1]+(matrix[j].tolist())
            sseTemp=0
            count=0
            for key in labelDic:
                sseTemp=sseTemp+sse(labelDic[key],(np.mean(np.array(labelDic[key]),axis=0)).tolist())
                count=count+1
            sseTemp=sseTemp/count
            if(sseTemp<sseSum):
                sseSum=sseTemp
                finalLabel=labels
                numClusters=k+1
                continue
            else:
                break
        personalDic={}
        for k1 in range(numClusters):
            personalDic[k1+1]=[]
        for k2 in range(len(finalLabel)):
            personalDic[finalLabel[k2]+1]=personalDic[finalLabel[k2]+1]+[Abs[k2]]
        clusterStrDic={}
        for Key in personalDic:
            sklearn_representation = sklearn_tfidf.fit_transform(personalDic[Key])
            vect = np.max(sklearn_representation.todense(), axis=0).tolist()
            reviwer_Score_dic={}
            for k in sklearn_tfidf.vocabulary_:
                reviwer_Score_dic[k] = vect[0][sklearn_tfidf.vocabulary_[k]]
            reviwer_Score_dic = sorted(reviwer_Score_dic.items(), key=lambda x: x[1])
            g = []
            n = int(len(reviwer_Score_dic) * 0.5)
            for f in range(n):
                item = reviwer_Score_dic.pop()
                k3,value = item
                g.append(k3)
            clusterStrDic[Key]= g
        reviwerDic[files[i][:-4]]=clusterStrDic
        #print(len(reviwerDic))


    # For documents submitted for reviewing
    input_title = open("Expert_Finding_Data/titles.txt","r", encoding='utf8',  errors='ignore')
    input_abstract = open("Expert_Finding_Data/abstracts.txt","r", encoding='utf8',  errors='ignore')

    l = []
    m = []
    v = 1       # for indexing in input_dic
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
        for reviewer in reviwerDic:
            if(len(name.intersection(set(reviewer))) > 0):
                continue;
            else:
                tempDic=reviwerDic[reviewer]
                maxScore=0
                for key in tempDic:
                    tempScore = jaccard_similarity(input_dic[index],tempDic[key])
                    if(tempScore>maxScore):
                        maxScore=tempScore
                jaccard_dic[reviewer]=maxScore
                
        jaccard_dic = sorted(jaccard_dic.items(), key=lambda x: x[1])
        g = []
        n = 10          # number of reviewers to be assigned
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
