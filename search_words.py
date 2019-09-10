import re

# searching for one query
def search_query(words,index_path,output_file):
	all_docs = {}
	for word in words:
		file_name = index_path + "/" + word[0] + word[1] + word[2] + ".txt"
		f = open(file_name,"r")
		line = f.readline()

		while line != "":
			line_word,rest = re.split(':',line)
			
			# move on to next iteration if not word
			if line_word != word:
				line = f.readline()
				continue

			# substitute T for t1 and such for byte compressions
			rest = re.sub('T','t1',rest)
			rest = re.sub('B','b1',rest)
			rest = re.sub('I','i1',rest)
			rest = re.sub('E','e1',rest)
			rest = re.sub('R','r1',rest)
			rest = re.sub('C','c1',rest)

			docs_index = re.split('\|',rest)
			docs = []
			for d in docs_index:
				docID,rest = re.split(',',d)
				docID = int(docID)
				
				'''
				all_freq = [int(i) for i in re.split("[a-z]",d)[1:]]
				all_fields = [i for i in re.split("[0-9]+",d) if i]
				
				freq = 0
				for i,field in enumerate(all_fields):
					if field == 't':
						freq += all_freq[i]
					if field == 'b':
						freq += all_freq[i]
				'''
				freq = int(re.split("[a-z]",rest)[0])
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


# searching for field query
def field_search_query(field_word_dict,index_path,output_file):
	all_docs = {}

	# go through each field and update all_docs dictionary
	for field,word in field_word_dict.items():
		file_name = index_path + "/" + word[0] + word[1] + ".txt"
		f = open(file_name,"r")
		line = f.readline()

		# go through each line of file containing the word
		while line != "":
			line_word,rest = re.split(':',line)
			
			# move on to next iteration if not word
			if line_word != word:
				line = f.readline()
				continue

			docs_index = re.split('\|',rest)
			docs = []
			for d in docs_index:
				docID,rest = re.split(',',d)
				docID = int(docID)
					
				# getting fields and frequencies corresponding to them
				all_freq = [int(i) for i in re.split("[a-z]",rest)[1:] ]
				all_fields = [i for i in re.split("[0-9]+",rest) if i]
					
				# if this field does not have word for docID, move to next docID
				if field not in all_fields:
					continue

				index = all_fields.index(field)
				freq = all_freq[index]

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



# "==References==\n[{{.*}}\n]+\n"
