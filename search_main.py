import sys
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import SnowballStemmer
import re
from search_words import search_query, field_search_query

snowball = SnowballStemmer('english')
stopwords = set(stopwords.words('english'))


index_path = sys.argv[1]
query_path = sys.argv[2]
output_path = sys.argv[3]


def field_query(query,index_path,output_file):
	field_words = [i for i in re.split(' ',query) if i]
	field_word_dict = {}
	for fw in field_words:
		field,word = re.split(':',fw)
		field_word_dict[field[0]] = word

	field_search_query(field_word_dict,index_path,output_file)


output_file = open(output_path,"w")

f = open(query_path,"r")

query = f.readline()


while(query!=""):
	words = []

	if len(re.split(':',query)) > 1:
		field_query(query,index_path,output_file)
		query = f.readline()
		continue

	# finding words in the query
	words=re.findall("[\w]+",query)

	# case folding
	for word in words:
		word = word.lower()


	# stemming
	stemmed = []
	stemmed = [snowball.stem(w) for w in words if not w in stopwords]


	words = stemmed

	search_query(words,index_path,output_file)

	query = f.readline()

f.close()


