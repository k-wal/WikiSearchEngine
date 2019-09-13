#import xml.etree.ElementTree as etree
from lxml import etree
import re
import process_text as pt
import merge
import sys

dump_path = sys.argv[1]
index_path = sys.argv[2]
total_articles = 0
merge_block_size = 1000
last_merge_end = 0
last_merge_number = 0
file_pointers = {}


# function to write title
def write_title(count,title,is_title_open,title_file_number,title_f):
	to_write = str(count) + ":" + title + "\n"
	
	if not is_title_open:
		file_name = index_path + "/title" + str(int(count/1000)) + ".txt"
		title_f = open(file_name,"a")
	else:
		if title_file_number != int(count/1000):
			title_f.close()
			file_name = index_path + "/title" + str(int(count/1000)) + ".txt"
			title_f = open(file_name,"a")

	title_f.write(to_write)
	return title_f


# functiont to get tagname
def strip_tag_name(tag):
	tag = elem.tag
	idx = k = tag.rfind("}")
	if idx != -1:
		tag = tag[idx + 1:]
	return tag


count = 0
cur_tag = ""
cur_content = ""
cur_doc = ""
title = ""
body = ""
info_box = ""
category = ""
external_links = ""
references = ""
title_f = ""
is_title_open = False
title_file_number = ""


for event, elem in etree.iterparse(dump_path, events = ('start' , 'end'), encoding='utf-8'):
	tag = strip_tag_name(elem.tag)
	#print(tag)
	#print(elem.text)


	
	# if its start of element
	if event == 'start':
		cur_tag = tag
		cur_content = ""
	
		if tag=="page":
			count += 1
			total_articles += 1
			cur_doc = ""
			title = ""
			body = ""
			info_box = ""
			category = ""
			external_links = ""
			references = ""
		
	

	# end of element
	else:

		if elem.text:
			content = elem.text.replace("_"," ")
			cur_content += content + " "
			cur_doc += content + " "

		# save title
		if tag == "title":
			title = cur_content
			title_f = write_title(count,title,is_title_open,title_file_number,title_f)

		# save text
		if tag=="text":
			body = cur_content

		# add different fields to the queue
		if tag=="page":
			#category = re.findall("^\[\[Category\:.*\]\]$",body)
			#info_box = re.findall("^{{Infobox.*}}$",body)
			arg = [title,body,info_box,category,external_links,references] 
			file_pointers[str(count)] = pt.tokenize(count,arg,index_path)
			#print(q.get())
			#pt.tokenize(cur_doc)
			#print(count)
		if tag=="page" and total_articles % merge_block_size == 0 and total_articles != 0:
			merge.range_merge(last_merge_end + 1,total_articles,last_merge_number+1,file_pointers,index_path)
			last_merge_number += 1
			file_pointers = {}
			last_merge_end = total_articles

		elem.clear()


merge.range_merge(last_merge_end + 1,total_articles,last_merge_number+1,file_pointers,index_path)
del file_pointers
merge.main_merge(last_merge_number+1,index_path)





