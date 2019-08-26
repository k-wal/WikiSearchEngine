import xml.sax
import process_text as pt


num = input("Enter doc id: ")

class WikiHandler(xml.sax.ContentHandler):

	def __init__(self):
		self.count = 0
		self.cur_tag = ""
		self.cur_content = ""
		self.cur_doc = ""

	# Call when element starts
	def startElement(self,tag,attributes):
		self.cur_tag = tag
		self.cur_content = ""
		if tag=="page":
			self.count += 1
			self.cur_doc = ""

	# Call when element ends
	def endElement(self,tag):
		
		if tag=="title" and self.count==int(num):
			print(self.cur_content)
			#exit()

		if tag=="page" and self.count==int(num):
			print(self.count)
			print(self.cur_doc)
			exit()
			
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
