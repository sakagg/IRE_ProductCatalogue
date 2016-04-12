from base_scraper import BaseScraper
from sys import argv
import sys
import pymongo
import math, time
from bson.objectid import ObjectId

class InfibeamScraper(BaseScraper):
	"""docstring for InfibeamScraper"""
	def __init__(self):
		hostname = "http://www.infibeam.com"
		BaseScraper.__init__(self, hostname)
		self.page_no = 1
		self.mobiles = pymongo.MongoClient().iredb.mobiles

	def _close(self):
		BaseScraper._close(self)

	def update(self, id):
		url = self.mobiles.find_one({"_id": ObjectId(id)})["url"]
		self.process(url, self.fetch(url), "update")

	def next(self):
		if self.page_no > 21:
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
			elif self.mobiles.count({"url": self.hostname + curr_link}) > 0:
				continue
			else:
				yield self.hostname + curr_link

	def process(self, url, page, oper = "create"):
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
			data["image"] = soup.find("img",{"class":"inview"}).get("src")
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

		if oper == "create":
			# writing to dump
			print self.mobiles.insert({
				"url": url,
				"name": data["name"],
				"price": [data["price"]],
				"vendor": data["vendor"],
				"image": data["image"],
				"description": data["description"],
				"specs": data["specs"],
				"updated_on": [math.floor(time.time()*1000)]
			})
			print data["name"]
		elif oper == "update":
			mobile = self.mobiles.find_one({"url": url})
			mobile["price"].append(data["price"])
			mobile["updated_on"].append(math.floor(time.time()*1000))
			self.mobiles.update({"_id": mobile["_id"]}, {
				"url": url,
				"name": data["name"],
				"price": mobile["price"],
				"vendor": data["vendor"],
				"image": data["image"],
				"description": data["description"],
				"specs": data["specs"],
				"updated_on": mobile["updated_on"]
			})
		return True

if len(sys.argv) >= 2:
	scraper = InfibeamScraper()
	if sys.argv[1] == "create":
		scraper.run()
	elif sys.argv[1] == "update" and len(sys.argv) >= 3:
		scraper.update(sys.argv[2])
