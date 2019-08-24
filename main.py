import re
from threading import Thread
import xml.sax
import process_text as pt
from queue import Queue

q = Queue(maxsize=0)
		


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

	# Call when element starts
	def startElement(self,tag,attributes):
		self.cur_tag = tag
		self.cur_content = ""
		if tag=="page":
			self.count += 1
			self.cur_doc = ""
			self.title = ""
			self.body = ""
			self.info_box = ""
			self.category = ""
			self.external_links = ""
			self.references = ""


	# Call when element ends
	def endElement(self,tag):
		
		# save title
		if tag == "title":
			self.title = self.cur_content

		# save text
		if tag=="text":
			self.body = self.cur_content

		# add different fields to the queue
		if tag=="page":
			#self.category = re.findall("^\[\[Category\:.*\]\]$",self.body)
			#self.info_box = re.findall("^{{Infobox.*}}$",self.body)
			arg = [self.title,self.body,self.info_box,self.category,self.external_links,self.references] 
			pt.tokenize(arg)
			#print(q.get())
			#pt.tokenize(self.cur_doc)
			print(self.count)

	def characters(self,content):
		self.cur_content += content + " "
		self.cur_doc += content + " "

	


#regex for category:
#    ^\[\[Category\:.*\]\]$
#    ^{{Infobox.*}}$


parser = xml.sax.make_parser()

parser.setFeature(xml.sax.handler.feature_namespaces, 0)

Handler = WikiHandler()
parser.setContentHandler(Handler)

parser.parse("data.xml")
'''
# assign tasks
def call_process_text(qu,):
		while not qu.empty():
			#print("qqqqqqqq")
			article = qu.get()
			#print(doc)
			pt.tokenize(article)
			
			qu.task_done()

num_threads = 1
for i in range(num_threads):
	thread = Thread(target=call_process_text,args=(q,))
	thread.setDaemon(True)
	thread.start()
q.join()
'''