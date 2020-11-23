import scrapper
from helium import *
import time


class AlzaWebAdapter(scrapper.WebAdapter):

	def __init__(self, start_url):
		self.start_url = start_url

	def init(self):
		start_firefox(self.start_url)
		get_driver().maximize_window()

	def in_list(self):
		return S('div.mainContent div.browsingitemcontainer div.browsingitem .c2').exists()

	def get_rows(self):
		return find_all(S('#boxes > div.browsingitem'))

	def get_data(self, row):
		el = row.web_element

		try:
			rating = el.find_element_by_css_selector('.star-rating-wrapper').get_attribute('title')
		except:
			rating = ''

		return {
			'name': el.find_element_by_css_selector('a.name').text,
			'code': el.find_element_by_css_selector('.codec .code').get_attribute('textContent'),
			'short_desc': el.find_element_by_css_selector('.Description').text.strip(),
			'rating': rating,
			'price': el.find_element_by_css_selector('.c2').text
				.strip(',-')
				.replace(' ', ''),
			'stock': el.find_element_by_css_selector('.avlVal').text.split('\n')[0],

			'detail': el.find_element_by_css_selector('a.name').get_attribute('href')
		}

	###### PAGINATION ######

	def next_page(self):
		last_page = self.get_page_id()

		self.scroll_to(S('#pagerbottom a.fa-chevron-right'), 64)
		click(S('#pagerbottom a.fa-chevron-right'))

		self.close_popups(last_page)
		wait_until(self.in_list, timeout_secs=30)

	def has_next_page(self):
		return S('#pagerbottom a.fa-chevron-right').exists()

	def get_page_id(self):
		id = S('#pagerbottom a.pgn.sel').web_element.text.strip()

		return id

	###### DETAIL ######

	def in_detail(self):
		return S('#popisx').exists()

	def get_detail_data(self):
		cont = S('#detailItem')
		return {
			'rating_count': cont.web_element.find_element_by_css_selector('.ratingCount').text.strip('x'),
			'phone': cont.web_element.find_element_by_css_selector('div:nth-child(4)').text,
		}

	def exit_detail(self):
		click(u'Všechny objednávky')
		wait_until(
			lambda:
				not S('div.v-select__selection.v-select__selection--comma.v-select__selection--disabled').exists(),
			timeout_secs=30
		)

	###### INTERNAL ######

	def close_popups(self, last_page):
		# last page content is still visible after clicking to next page button
		wait_until(lambda: self.get_page_id() != last_page, 30)
		wait_until(S('#categoryAnotationBlock h1').exists, 30)

		try:
			wait_until(S('.popUpDialog .close').exists, 3)
			click(S('.popUpDialog .close'))
		except:
			pass

