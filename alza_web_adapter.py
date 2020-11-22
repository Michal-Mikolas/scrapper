import scrapper
from helium import *


class AlzaWebAdapter(scrapper.WebAdapter):

	def __init__(self, start_url):
		self.start_url = start_url

	def init(self):
		start_chrome(self.start_url)
		get_driver().maximize_window()

	def in_list(self):
		return S('div.mainContent div.browsingitemcontainer div.browsingitem a.name').exists()

	def get_rows(self):
		self.scroll_bottom()
		return find_all(S('div.mainContent div.browsingitemcontainer div.browsingitem'))

	def get_data(self, row):
		el = row.web_element
		return {
			'code': el.find_element_by_css_selector('.codec .code').text,
			'name': el.find_element_by_css_selector('a.name').text,
			'short_desc': el.find_element_by_css_selector('.Description').text.strip(),
			'rating': el.find_element_by_css_selector('.star-rating-wrapper').get_attribute('title'),
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

	def next_page(self):
		click(S('#pagerbottom a.fa-chevron-right'))
		wait_until(self.in_list, timeout_secs=30)

	def has_next_page(self):
		return not S('#pagerbottom a.fa-chevron-right').exists()

	###### RESTORE PAGINATION ######

	# def get_page_id(self):
	# 	id = S('div.v-data-footer__pagination').web_element.text
	# 	id = re.sub(' z .*', '', id)

	# 	return id.strip()

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
