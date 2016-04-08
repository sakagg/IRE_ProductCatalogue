# It is advised not to touch this file.
# You may read the comments though.
# To use the package, look at the example "infibeam_scraper.py"

import requests
from time import sleep
import time
from bs4 import BeautifulSoup
import codecs
import sys
import urllib

class BaseScraper(object):
	"""docstring for BaseScraper"""
	# init function, nothing to explain here
	def __init__(self):
		self.visited = set()
		self.queue = []

	# fetch(url) -> page
	# Fetches a url and returns the corresponding BeautifulSoup object
	# url: URL of the age you'd like to fetch
	# page: BeautifulSoup object of the requested page
	def fetch(self, url):
		r = requests.get(url)
		return BeautifulSoup(r.content)

	# run() -> None
	# The core logic of the class
	# First, get all the page urls and extract all product urls
	# Eliminate any duplicates
	# Process all product URLs
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

	# next() -> url
	# url: URL of the next page containing the list of products
	def next(self):
		return False

	# products(page) -> productList
	# Extract all product urls from a product catalogue page
	# page: BeautifulSoup object of the page containing all product urls
	# productList: A list of all valid product urls you wish to visit
	def products(self, page):
		links = page.find_all("div", "product-img")
		for link in links:
			curr_link = link.contents[1].get("href")
			if curr_link.startswith("/Mobile_Accessories") or curr_link.startswith("/mobile_accessories"):
				continue
			else:
				yield self.hostname + curr_link

	# process(page) -> status
	# Process a prodcut page
	# url: URL of the requested product page
	# page: BeautifulSoup object of the corresponding product page
	def process(self, url, page):
		print url
