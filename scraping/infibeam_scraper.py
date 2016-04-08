from base_scraper import BaseScraper

class InfibeamScraper(BaseScraper):
	"""docstring for InfibeamScraper"""
	def __init__(self):
		BaseScraper.__init__(self)
		self.hostname = "http://infibeam.com"
		self.page_no = 1

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
		print url
		return True

scraper = InfibeamScraper()
scraper.run()
