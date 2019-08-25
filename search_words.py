


def search_word(words,index_path):
	f = open(index_path,"r")
	all_docs = {}
	line = f.readline()
	while line != "":
		line_word,rest = line.split(':')

		for word in words:

			if line_word == words:
				docs_index = rest.split('|')
				docs = []
				for d in docs_index:
					docID = d.split(',')[0]
					if str(docID) not in all_docs.keys():
						all_docs[str(docID)] = 1
					else:
						all_docs[str(docID)] += 1

	print(sorted(all_docs))
