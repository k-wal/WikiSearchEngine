


def search_word(words,index_path):
	all_docs = {}
	for word in words:
		file_name = index_path + "/" + word[0] + word[1] + ".txt"
		f = open(file_name,"r")
		line = f.readline()

		while line != "":
			line_word,rest = line.split(':')
			
			if line_word == word:
				docs_index = rest.split('|')
				docs = []
				for d in docs_index:
					docID = d.split(',')[0]
					freq = int(d.split(',')[1])
					'''
					if str(docID) not in all_docs.keys():
						if freq <= 1:
							all_docs[str(docID)] = 1
						else:
							all_docs[str(docID)] = freq
					else:
						if freq<=1:
							all_docs[str(docID)] += 1
						else:
							all_docs[str(docID)] *= freq
					'''
					if str(docID) not in all_docs.keys():
						all_docs[str(docID)] = freq
					else:
						all_docs[str(docID)] *= freq
					
				break
			line = f.readline()

	count=0
	for key,value in sorted(all_docs.items(), key = lambda item: item[1], reverse=True):
		index = int(key)
		print_title(index,index_path)
		count+=1
		if count==10:
			break
	print("-------------------------")

def print_title(docID,index_path):
	file_name = index_path + "/title" + str(int(docID/1000)) + ".txt"
	f = open(file_name,"r")
	line = f.readline()
	while line != "":
		#print(line)
		fID = line.split(':')[0]
		l_id = len(fID) + 1
		l_line = len(line)
		title = line[l_id:l_line]
		if int(fID) == docID:
			print(title)
			break
		line = f.readline()
