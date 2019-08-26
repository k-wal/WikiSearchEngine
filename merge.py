from heapq import heappush, heappop
import os



def main_merge(total_articles,index_path):

	# max number of files open at a time
	max_files = 1000
	max_lines = 50000
	last_file_name = ""

	# number of files currently open
	open_files = 0

	# total number of files
	heap = []

	iteration_number = 1

	# total number of index files in the folder
	num_files = total_articles

	while(num_files>1):
		# current number of files to create in this iteration
		cur_number = 1
		open_files = 0
		
		# going through all files 
		for file_number in range(1,num_files+1):
			file_name = index_path + "/" + str(iteration_number) + "_" + str(file_number) + ".txt"
			
			# if max_files are open, then merge, empty heap, reset open_files 
			if open_files == max_files:
				last_file_name = merge_lower(open_files,heap,iteration_number,cur_number,index_path)

				heap = []
				open_files = 0
				cur_number += 1

			try:	
				f = open(file_name,"r")
			except:
				print("FILE NOT OPENED")
				print(file_name)
				continue

			line = f.readline()
			if line.rstrip() == "":
				line =  f.readline()
				if line.rstrip() =="":
					continue
			
			open_files+=1
		
			# splitting to get word and rest
			word,rest = line.split(":")
			# getting docID from the rest (before forst comma)
			docID = int(rest.split(",")[0])
			# first sort by word, then by docID
			heappush(heap,(word,docID,line,f))
	
		# merge last of files, when the number is not bigger than max_files
		last_file_name = merge_lower(open_files,heap,iteration_number,cur_number,index_path)
		heap = []
		open_files = 0
			
		# remove files of last iteration
		for file_number in range(1,num_files+1):
			file_name = index_path + "/" + str(iteration_number) + "_" + str(file_number) + ".txt"
			os.remove(file_name)
		iteration_number += 1
		# new number of files to merge = number of files created in this iteration
		num_files = cur_number


	last_letters = "00"

#	file_name = index_path + "/" + last_file_name
	f = open(last_file_name,"r")
	line = f.readline()
	file_name = index_path + "/" + str(last_letters) + ".txt"
	cur_f = open(file_name,"w")
	while line!="":
		word,rest = line.split(":")
		#if len(word) < 2 or not((word[0]>='a' and word[0]<='z') or (word[0]>='0' and word[0]<='9')) or not((word[1]>='a' and word[1]<='z') or (word[1]>='0' and word[1]<='9')):
		if len(word) < 2 or not(word[0]>='a' and word[0]<='z') or not(word[1]>='a' and word[1]<='z'):
			line = f.readline()
			continue
		if last_letters!=word[:2]:
			cur_f.close()
			last_letters = word[:2]
			file_name = index_path + "/" + str(last_letters) + ".txt"
			cur_f = open(file_name,"w")
		cur_f.write(line)
		line = f.readline()
	
	f.close()
	cur_f.close()
	os.remove(last_file_name)
			



def merge_lower(open_f,heap,iteration_number,cur_number,index_path):
	file_name_new = index_path + "/" + str(iteration_number+1) + "_" + str(cur_number) + ".txt"
	f_new = open(file_name_new,"w")
	last_file_name = file_name_new
	last_line = ""
	last_word = ""
	last_rest = ""

	cur_entry=0
	while open_f>0:
		cur_entry+=1
		
		try:
			w, docID , line , f = heappop(heap)
		except:
			print(heap)
			
		# extracting word and rest of sentence
		word,rest = line.split(":")	
		
		#removing newline at the end
		rest= rest.rstrip()
		
		# if current word matches with new word, append
		if word==last_word:
			to_write = "|" + rest

		else:
			if cur_entry==1:
				to_write = line.rstrip()		
			else:
				to_write = "\n" + line.rstrip()
		
		f_new.write(to_write)
		last_word,last_rest = word,rest
		new_line = f.readline()
		if new_line != "":
			w = new_line.split(":")[0]
			heappush(heap,(w,docID,new_line,f))
		else:
			f.close()
			#print("closing file #########################")
			open_f -= 1;

	f_new.close()
	open_files = 0
	heap = []

	return file_name_new

#main_merge()