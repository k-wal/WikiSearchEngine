import sys
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.stem import SnowballStemmer
import re
from search_words import search_query, field_search_query
import time

snowball = SnowballStemmer('english')
stopwords = set(stopwords.words('english'))


index_path = sys.argv[1]
start_time = time.time()


def field_query(query,index_path):
	field_words = [i for i in re.split(' ',query) if i]
	field_word_dict = {}
	for fw in field_words:
		field,word = re.split(':',fw)
		field_word_dict[field[0]] = word

	result_count = field_search_query(field_word_dict,index_path)




while True:
	words = []
	query = input("QUERY : ")
	start_time = time.time()
	print("\n")

	if len(re.split(':',query)) > 1:
		result_query = field_query(query,index_path)
		continue

	# finding words in the query
	words=re.findall("[a-zA-Z]+",query)

	# case folding
	for word in words:
		word = word.lower()


	# stemming
	stemmed = []
	stemmed = [snowball.stem(w) for w in words if not w in stopwords]


	words = stemmed

	result_count = search_query(words,index_path)
	print("---------------------", result_count, " results in ",time.time() - start_time," seconds ---------------")
	print("\n\n")


