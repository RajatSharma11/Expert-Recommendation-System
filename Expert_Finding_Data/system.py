import re
file_reviewer = open("reviewers.txt","r")
reviewer_list = []
dic = {}
r = re.compile("[a-z \-\'A-z]+")
for line in file_reviewer:
	reviewer_list.append("".join(r.findall(line)))
	dic["".join(r.findall(line))] = []
#print(reviewer_list)

file_trainingSet = open("training.txt","r")
p = re.compile("\t[a-z ,:\-/;A-z]+.")
i = 0
'''
for line in file_trainingSet:
	name = r.findall(line)[0]
	if("Abstract" in "".join(p.findall(line))):
		q = "".join(p.findall(line)).find("Abstract")
		#print("".join(p.findall(line))[1:q])
		topic = "".join(p.findall(line))[1:q]
	elif("ABSTRACT" in "".join(p.findall(line))):
		q = "".join(p.findall(line)).find("ABSTRACT")
		#print("".join(p.findall(line))[1:q])
		topic = "".join(p.findall(line))[1:q]
	else:
		#print("".join(p.findall(line))[1:-1])
		topic = "".join(p.findall(line))[1:-1]
	dic[name].append(topic)
print(dic)
'''
for line in file_trainingSet:
	name = p.findall(line)
	print(name)
	
