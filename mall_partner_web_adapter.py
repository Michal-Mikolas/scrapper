import scrapper
from helium import *
import re


class MallPartnerWebAdapter(scrapper.WebAdapter):

	def __init__(self, email, password):
		super().__init__()

		self.email = email
		self.password = password

	def init(self):
		start_chrome('https://new-partners.mallgroup.com/login')
		get_driver().maximize_window()

		write(self.email, into='Email')
		write(self.password, into='Heslo')
		click(u'Přihlásit')

	def in_list(self):
		return S('div.v-data-table tbody tr td:nth-child(12)').exists()

	def get_rows(self):
		return find_all(S('div.v-data-table tbody tr'))

	def get_data(self, row):
		return {
			'id': row.web_element.find_element_by_css_selector('td:nth-child(3)').text,
			'mall_id': row.web_element.find_element_by_css_selector('td:nth-child(4)').text,
			'name': row.web_element.find_element_by_css_selector('td:nth-child(5)').text,
			'price': row.web_element.find_element_by_css_selector('td:nth-child(6)').text
				.replace(' ', '')
				.replace(u'Kč', ''),
			'payment': row.web_element.find_element_by_css_selector('td:nth-child(7)').text,
			'delivery': row.web_element.find_element_by_css_selector('td:nth-child(8)').text,
			'package_id': row.web_element.find_element_by_css_selector('td:nth-child(9)').text,
			'opened_date': row.web_element.find_element_by_css_selector('td:nth-child(10)').text
				.replace('\n', ' '),
			'delivery_date': row.web_element.find_element_by_css_selector('td:nth-child(11)').text,
			'delivered_date': row.web_element.find_element_by_css_selector('td:nth-child(12)').text,
			'status': row.web_element.find_element_by_css_selector('td:nth-child(13)').text,
			'detail': lambda row_data: (
				# fix for inability to click on first link?
				get_driver().execute_script("window.scrollTo(0, 0)"),
				click(row_data['id'])
			),
		}

	def next_page(self):
		click(S('div.v-data-footer__icons-after button'))
		wait_until(lambda:
                    not S(
                    	'div.v-select__selection.v-select__selection--comma.v-select__selection--disabled').exists(),
                    timeout_secs=30
             )

	def has_next_page(self):
		return not S('div.v-data-footer__icons-after button[disabled]').exists()

	###### RESTORE PAGINATION ######

	def get_page_id(self):
		id = S('div.v-data-footer__pagination').web_element.text
		id = re.sub(' z .*', '', id)

		return id.strip()

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
