import re
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import SnowballStemmer


porter = SnowballStemmer('english')
stopwords = set(stopwords.words('english'))


def tokenize(article):
	words = []
	for field in article:
		words.append(re.findall("[\w']+",field))
	case_folding(words)
	#print(words)

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
		

	[ print(key , " :: " , value) for (key, value) in sorted(count.items()) if count[key][0]>0 ]
	print("\n")