import requests
from time import sleep
import time
from bs4 import BeautifulSoup
import codecs
import sys
import urllib

class BaseScraper(object):
	"""docstring for BaseScraper"""
	def __init__(self):
		self.visited = set()
		self.queue = []

	def fetch(self, url):
		r = requests.get(url)
		return BeautifulSoup(r.content)

	def run(self):
		page = self.next()
		while page:
			content = self.fetch(page)
			for product_url in self.products(content):
				if product_url not in self.visited:
					content = self.fetch(product_url)
					status = self.process(product_url, content)
					if not status is False:
						self.visited.add(product_url)
						self.queue.append(product_url)
			page = self.next()
		for i in self.queue:
			self.process(i, self.fetch(i))

	def next(self):
		return False

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
