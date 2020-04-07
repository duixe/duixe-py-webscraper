import sqlite3
from bs4 import BeautifulSoup
import requests

conn = sqlite3.connect("crawl.db")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS crawlTB(book_name TEXT, price TEXT, links TEXT)")


class webCrawler:
	def __init__(self, begin_url, depth):
		self.begin_url = begin_url
		self.depth = depth
		self.books = []

	def crawl(self):
		self.info_from_link(self.begin_url)

	# @staticmethod
	def info_from_link(self, link):
		start_page = requests.get(link)
		soup = BeautifulSoup(start_page.text, 'html.parser')

		all_books = soup.find_all(class_='product_pod')

		# for books in all_books:
		# 	for book_name in books.select('h3'):
		# 		print(book_name.get_text())
		for all_book in all_books:
			links = all_book.find(class_='image_container').contents[1]['href']
			book_name = all_book.find('h3').get_text()
			price = all_book.find(class_='price_color').get_text().replace('Â', '')
			book_info = bookInfo(book_name, price, links)
			book_info.exec_sqlite()

		self.books.append(book_info)


class bookInfo:
	def __init__(self, book_name, price, links):
		self.book_name = book_name
		self.price = price
		self.links = links

	def exec_sqlite(self):
		cur.execute("INSERT INTO crawlTB (book_name, price, links) VALUES (?, ?, ?)",
					(self.book_name, self.price, self.links))
		conn.commit()


spider = webCrawler("http://books.toscrape.com/", 0)
spider.crawl()

for book in spider.books:
	print("scraped data added to your DB", end='')
