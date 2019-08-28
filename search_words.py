import re

# searching for one query
def search_query(words,index_path,output_file):
	all_docs = {}
	for word in words:
		file_name = index_path + "/" + word[0] + word[1] + ".txt"
		f = open(file_name,"r")
		line = f.readline()

		while line != "":
			line_word,rest = re.split(':',line)
			
			if line_word == word:
				docs_index = re.split('\|',rest)
				docs = []
				for d in docs_index:
					docID,rest = re.split(',',d)
					docID = int(docID)
					
					all_freq = [int(i) for i in re.split("[a-z]",rest)[1:] ]
					all_fields = [i for i in re.split("[0-9]+",rest) if i]
					
					freq = int(re.split("[a-z]",rest)[0])
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
		print_title(index,index_path,output_file)
		count+=1
		if count==10:
			break
	output_file.write("\n")

# writing title to output file
def print_title(docID,index_path,output_file):
	file_name = index_path + "/title" + str(int(docID/1000)) + ".txt"
	f = open(file_name,"r")
	line = f.readline()
	while line != "":
		#print(line)
		fID = re.split(':',line)[0]
		l_id = len(fID) + 1
		l_line = len(line)
		title = line[l_id:l_line]
		if int(fID) == docID:
			output_file.write(title)
			break
		line = f.readline()
