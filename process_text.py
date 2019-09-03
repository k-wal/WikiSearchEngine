import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import SnowballStemmer


porter = SnowballStemmer('english')
stopwords = set(stopwords.words('english'))


# create an array of separate words for all fields
def tokenize(docID,article,index_path):
	words = []
	title = article[0]
	for field in article:
		#print(field)
	#	words.append(re.findall("[a-zA-Z]+",field))
		words.append(re.findall("[a-zA-Z]+",field))



	# finding category from body
	category = re.findall("\[\[Category\:.*\]\]",article[1])
	for c in category:
		sep_words = re.findall("[a-zA-Z]+",c)
		for w in sep_words:
			words[3].append(w)		

	# finding info_box from body
	info_box = re.findall("{{Infobox.*}}",article[1])
	
	for i in info_box:
		sep_words = re.findall("[a-zA-Z]+",i)
		for w in sep_words:
			words[2].append(w)		

	#case_folding(docID,words,title,index_path)
	stem(docID,words,title,index_path)
	

'''
def case_folding(docID,old_words,title,index_path):
	new_words = []
	for field in old_words:
		new_words.append([s.lower() for s in field])
	stem(docID,new_words,title,index_path)
'''

# to remove stop words and stem words and case folding
def stem(docID,all_words,title,index_path):
	words = []
	for field in all_words:
		words.append([porter.stem(w.lower()) for w in field if not w.lower() in stopwords])


	new_words = [w for w in words if len(w)>1]
	count(docID,new_words,title,index_path)

# counting every single word count in all fields
def count(docID,words,title,index_path):
	count = {}
	
	# order of fields : all(total frequency),title, body, info_box, category, external_links, referances
	for (i,field) in enumerate(words):
		for w in field:
			if w not in count.keys():
				count[w] = [0,0,0,0,0,0]
				count[w][i] = 1
			else:
				count[w][i] += 1
	
	to_file(docID,count,index_path)

# write to file "docID.txt"
# format for a word (say key): key:docID,TOTAL,tTNUM,bBODY,iINFO,cCATEGORY,lLINKS,rREFERENCES
def to_file(docID,count,index_path):
	file_name = index_path + "/1_" + str(docID) + ".txt"
	f = open(file_name,"w")
	for w in sorted(count.keys()):
		to_write = w + ":" + str(docID)

		title,body,info_box,category,external_links,referances = count[w]
		body -= (info_box + category)
		
		if title==1:
			to_write += "T"
		elif title>0:
			to_write += "t" + str(title)

		if body==1:
			to_write += "B"
		elif body>0:
			to_write += "b" + str(body)
		
		if info_box==1:
			to_write += "I"
		elif info_box>0:
			to_write += "i" + str(info_box)

		if category==1:
			to_write += "C"
		elif category>0:
			to_write += "c" + str(category)

		if external_links==1:
			to_write += "E"
		elif external_links>0:
			to_write += "e" + str(links)

		if referances==1:
			to_write += "R"
		elif referances>0:
			to_write += "r" + str(referances)

		to_write += "\n"
		f.write(to_write)
	f.close()



#	[ print(key , " :: " , value) for (key, value) in sorted(count.items())] #if count[key][3]>0 ]
#	print("\n")