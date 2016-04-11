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
from reppy.cache import RobotsCache

class BaseScraper(object):
	"""docstring for BaseScraper"""
	# init function
	# hostname: Hostname of the site you'll be crawling.
	# Required to read robots.txt and set proper permissions
	# for Crawl-delay and Allowed URLs
	def __init__(self, hostname):
		self.hostname = hostname
		self.visited = set()
		self.queue = []
		self.headers = {
			"User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:40.0) Gecko/20100101 Firefox/40.1"
		}
		self.crawl_rules = RobotsCache().fetch(hostname)
		self.delay = self.crawl_rules.delay('*')
		if self.delay is None:
			self.delay = 0.0
		self.last_fetch_time = 0

	# close function. Like a destructor
	# Any cleanup such as deleting temporary files goes here
	def _close(self):
		pass

	# fetch(url) -> page
	# Fetches a url and returns the corresponding BeautifulSoup object
	# url: URL of the age you'd like to fetch
	# page: BeautifulSoup object of the requested page
	def fetch(self, url):
		time_to_sleep = max(0, self.last_fetch_time + self.delay - time.time())
		time.sleep(time_to_sleep)
		if self.crawl_rules.allowed(url, '*'):
			r = requests.get(url, headers = self.headers)
		else:
			raise "FetchError"
		self.last_fetch_time = time.time()
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
		self._close()

	# next() -> url
	# url: URL of the next page containing the list of products
	def next(self):
		return False

	# products(page) -> productList
	# Extract all product urls from a product catalogue page
	# page: BeautifulSoup object of the page containing all product urls
	# productList: A list of all valid product urls you wish to visit
	def products(self, page):
		return []

	# process(page) -> status
	# Process a prodcut page
	# url: URL of the requested product page
	# page: BeautifulSoup object of the corresponding product page
	def process(self, url, page):
		return True
