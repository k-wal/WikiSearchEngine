import re
import xml.sax
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


class WikiHandler(xml.sax.ContentHandler):

	def __init__(self):
		self.count = 0
		self.cur_tag = ""
		self.cur_content = ""
		self.cur_doc = ""
		self.title = ""
		self.body = ""
		self.info_box = ""
		self.category = ""
		self.external_links = ""
		self.references = ""
		self.title_f = ""
		self.is_title_open = False
		self.title_file_number = ""

	# Call when element starts
	def startElement(self,tag,attributes):
		global total_articles

		self.cur_tag = tag
		self.cur_content = ""
		if tag=="page":
			self.count += 1
			total_articles += 1
			self.cur_doc = ""
			self.title = ""
			self.body = ""
			self.info_box = ""
			self.category = ""
			self.external_links = ""
			self.references = ""

	# Call when element ends
	def endElement(self,tag):
		global file_pointers
		global total_articles
		global merge_block_size
		global last_merge_end
		global index_path
		global last_merge_number
		# save title
		if tag == "title":
			self.title = self.cur_content
			self.write_title()

		# save text
		if tag=="text":
			self.body = self.cur_content

		# add different fields to the queue
		if tag=="page":
			#self.category = re.findall("^\[\[Category\:.*\]\]$",self.body)
			#self.info_box = re.findall("^{{Infobox.*}}$",self.body)
			arg = [self.title,self.body,self.info_box,self.category,self.external_links,self.references] 
			file_pointers[str(self.count)] = pt.tokenize(self.count,arg,index_path)
			#print(q.get())
			#pt.tokenize(self.cur_doc)
			#print(self.count)
		if tag=="page" and total_articles % merge_block_size == 0 and total_articles != 0:
			merge.range_merge(last_merge_end + 1,total_articles,last_merge_number+1,file_pointers,index_path)
			last_merge_number += 1
			file_pointers = {}
			last_merge_end = total_articles



	def characters(self,content):
		content = content.replace("_"," ")
		self.cur_content += content + " "
		self.cur_doc += content + " "

	def write_title(self):
		to_write = str(self.count) + ":" + self.title + "\n"
		
		if not self.is_title_open:
			file_name = index_path + "/title" + str(int(self.count/1000)) + ".txt"
			self.title_f = open(file_name,"a",encoding="utf-8")
		else:
			if self.title_file_number != int(self.count/1000):
				self.title_f.close()
				file_name = index_path + "/title" + str(int(self.count/1000)) + ".txt"
				self.title_f = open(file_name,"a",encoding="utf-8")

		self.title_f.write(to_write)



#regex for category:
#    ^\[\[Category\:.*\]\]$
#    ^{{Infobox.*}}$


parser = xml.sax.make_parser()

parser.setFeature(xml.sax.handler.feature_namespaces, 0)

Handler = WikiHandler()
parser.setContentHandler(Handler)

parser.parse(dump_path)

merge.range_merge(last_merge_end + 1,total_articles,last_merge_number+1,file_pointers,index_path)
del file_pointers
merge.main_merge(last_merge_number+1,index_path)