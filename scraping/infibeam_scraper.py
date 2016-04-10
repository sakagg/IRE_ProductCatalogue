from base_scraper import BaseScraper
from sys import argv
import sys

class InfibeamScraper(BaseScraper):
	"""docstring for InfibeamScraper"""
	def __init__(self, filepath):
		BaseScraper.__init__(self)
		self.hostname = "http://www.infibeam.com"
		self.page_no = 1
		self.dump = open(filepath, "w")

	def _close(self):
		self.dump.close()
		BaseScraper._close(self)

	def next(self):
		if self.page_no > 22:
			return False
		url = self.hostname+"/Mobiles/search?sort=relevance&page="+str(self.page_no)
		self.page_no += 1
		return url

	def products(self, page):
		links = page.find_all("div", "product-img")
		for link in links:
			curr_link = link.contents[1].get("href")
			if curr_link.startswith("/Mobile_Accessories") or curr_link.startswith("/mobile_accessories"):
				continue
			else:
				yield self.hostname + curr_link

	def process(self, url, page):
		soup = page
		data = {}
		delimit = "#@#"

		# handling encoding issues
		reload(sys)
		sys.setdefaultencoding('utf8')

		# Getting dump specific data from DOM
		try:
			data["name"] = soup.find("h1",{"class":"product-title-big"}).contents[0]
		except AttributeError:
			data["name"] = "Error"

		if data["name"] == "Error":
			return False
		try:
			data["image"] = soup.find("img",{"class":"hidden"}).get("src")
		except AttributeError:
			data["image"] = "No image"
		try:
			data["price"] = str(soup.find("meta",{"itemprop":"price"}).get("content"))
		except AttributeError:
			data["price"] = "N/A"

		try:
			data["vendor"] = str(soup.find("span",{"class":"seller-detail name"}).contents[0])
		except AttributeError:
			data["vendor"] = "No vendor"
		try:
			data["description"] = str(soup.find("div", {"class":"description"}).contents[1])+""
		except AttributeError:
			data["description"] = "No description"
		try:
			tds = soup.find("div",{"id":"specs"}).find_all("td")
			specs = []
			for i in range(0,len(tds)-1,2):
				try:
					if( i+1 < len(tds) and len(tds[i].contents) >= 1 and len(tds[i+1].contents) >= 1):
						word1 = (tds[i].contents[0]).decode("utf8",errors="ignore")
						word2 = (tds[i+1].contents[0]).decode("utf8",errors="ignore")
						specs.append(word1+"*%*"+word2)
				except TypeError,IndexError:
					pass
			data["specs"] = u"#~#".join(specs)
		except AttributeError:
		  	data["specs"] = "No specs"

		data["name"] = data["name"].decode("utf8","ignore")
		data["price"] = data["price"].decode("utf8","ignore")
		data["vendor"] = data["vendor"].decode("utf8","ignore")
		data["description"] = data["description"].decode("utf8","ignore")
		data["specs"] = data["specs"].decode("utf8","ignore")

		# writing to dump
		self.dump.write(data["name"]+delimit+data["price"]+delimit+data["vendor"]+delimit+data["image"]+delimit+data["description"]+delimit+data["specs"]+"*@*")
		return True

if len(argv) == 2:
	scraper = InfibeamScraper(argv[1])
	scraper.run()
else:
	print "Error: filepath arg expected"
