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
			'code': el.find_element_by_css_selector('.codec .code').get_attribute('textContent'),
			'name': el.find_element_by_css_selector('a.name').text,
			'short_desc': el.find_element_by_css_selector('.Description').text.strip(),
			'rating': rating,
			'price': el.find_element_by_css_selector('.c2').text
				.strip(',-')
				.replace(' ', ''),
			'stock': el.find_element_by_css_selector('.avlVal').text.split('\n')[0],

			# 'detail': lambda row_data: (
			# 	# fix for inability to click on first link?
			# 	get_driver().execute_script("window.scrollTo(0, 0)"),
			# 	click(row_data['id'])
			# ),
		}

	###### PAGINATION ######

	def next_page(self):
		next_page_url = S('#pagerbottom a.fa-chevron-right').web_element.get_attribute('href')
		get_driver().get(next_page_url)
		wait_until(self.in_list, timeout_secs=30)
		self.close_popups()

	def has_next_page(self):
		return S('#pagerbottom a.fa-chevron-right').exists()

	def get_page_id(self):
		id = S('#pagerbottom a.pgn.sel').web_element.text.strip()

		return id

	###### DETAIL ######

	def in_detail(self):
		return S('main .v-card.custom-card .row .col-sm-4:nth-child(1) div').exists()

	def get_detail_data(self):
		cont = S('main .v-card.custom-card .row .col-sm-4:nth-child(1) div')
		return {
			'email': cont.web_element.find_element_by_css_selector('div:nth-child(3)').text,
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

	def close_popups(self):
		try:
			wait_until(S('.popUpDialog .close').exists, 2)
			click(S('.popUpDialog .close'))
		except:
			pass
