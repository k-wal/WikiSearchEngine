from heapq import heappush, heappop
import os


def main_merge():

	# max number of files open at a time
	max_files = 1000
	# number of files currently open
	open_files = 0

	# total number of files
	heap = []

	iteration_number = 1

	while(len(os.listdir("files"))>1):
		cur_number = 1
		open_files = 0
		num_files = len(os.listdir("files"))
		for file_number in range(1,num_files+1):
			file_name = "files/"+str(iteration_number)+"_" + str(file_number) + ".txt"
			
			if open_files == max_files:
				merge_lower(open_files,heap,iteration_number,cur_number)

				heap = []
				open_files = 0
				cur_number += 1

			f = open(file_name,"r")
			open_files+=1
			line = f.readline()
			if line.rstrip() == "":
				continue
			
			word,rest = line.split(":")
			docID = int(rest.split(",")[0])
			# first sort by word, then by docID
			heappush(heap,(word,docID,line,f))
	
		merge_lower(open_files,heap,iteration_number,cur_number)
		heap = []
		open_files = 0
		cur_number += 1
			
		for file_number in range(1,num_files+1):
			file_name = "files/"+str(iteration_number)+"_" + str(file_number) + ".txt"
			os.remove(file_name)
		iteration_number += 1


def merge_lower(open_f,heap,iteration_number,cur_number):
	file_name_new = "files/" + str(iteration_number+1) + "_" + str(cur_number) + ".txt"
	f_new = open(file_name_new,"w")
	last_line = ""
	last_word = ""
	last_rest = ""

	cur_entry=0
	while open_f>0:
		cur_entry+=1
		
		w, docID , line , f = heappop(heap)
		
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

#main_merge()