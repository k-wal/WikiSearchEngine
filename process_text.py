import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import SnowballStemmer


porter = SnowballStemmer('english')
stopwords = set(stopwords.words('english'))


def tokenize(article):
	words = []
	for field in article:
		#print(field)
		words.append(re.findall("[\w']+",field))
	
	category = re.findall("\[\[Category\:.*\]\]",article[1])
	for c in category:
		sep_words = re.findall("[\w']+",c)
		for w in sep_words:
			words[3].append(w)		

	info_box = re.findall("^{{Infobox.*}}$",article[1])
	for i in info_box:
		sep_words = re.findall("[\w']+",c)
		for w in sep_words:
			words[2].append(w)		


	case_folding(words)
	
def case_folding(old_words):
	new_words = []
	for field in old_words:
		new_words.append([s.lower() for s in field])
	stem(new_words)

# to remove stop words and stem words
def stem(all_words):
	words = []
	for field in all_words:
		words.append([porter.stem(w) for w in field if not w in stopwords])
	count(words)

def count(words):
	count = {}
	
	for (i,field) in enumerate(words):
		for w in field:
			if w not in count.keys():
				count[w] = [0,0,0,0,0]
				count[w][i] = 1
			else:
				count[w][i] += 1
		

#	[ print(key , " :: " , value) for (key, value) in sorted(count.items())] #if count[key][3]>0 ]
#	print("\n")