import sys
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import SnowballStemmer
import re
from search_words import search_word

snowball = SnowballStemmer('english')
stopwords = set(stopwords.words('english'))


query_path = sys.argv[1]
index_path = sys.argv[2]
f = open(query_path,"r")

query = f.readline()

while(query!=""):
	words = []

	# finding words in the query
	words=re.findall("[\w]+",query)

	# case folding
	for word in words:
		word = word.lower()

	# stemming
	stemmed = []
	stemmed.append([snowball.stem(w) for w in words if not w in stopwords])

	words = stemmed
	print(words)
	search_word(words,index_path)

	query = f.readline()

f.close()