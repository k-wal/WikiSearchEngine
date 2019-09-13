import xml.sax
import sys

dump_path = sys.argv[1]
total_articles = 0

class WikiHandler(xml.sax.ContentHandler):

	def __init__(self):
		self.count = 0

	# Call when element starts
	def startElement(self,tag,attributes):
		global total_articles

		if tag=="page":
			self.count += 1
			total_articles += 1

	# Call when element ends
	def endElement(self,tag):
		global total_articles

		if tag=="page" and total_articles % 1000 == 0:
			print(total_articles)


	def characters(self,content):
		pass




#regex for category:
#    ^\[\[Category\:.*\]\]$
#    ^{{Infobox.*}}$


parser = xml.sax.make_parser()

parser.setFeature(xml.sax.handler.feature_namespaces, 0)

Handler = WikiHandler()
parser.setContentHandler(Handler)

parser.parse(dump_path)
