#!/usr/bin/env python3
from helium import *
from selenium.webdriver.common.keys import Keys
import time
import math
import csv

"""
Web scrapper

Created by Michal Mikolas
	https://www.linkedin.com/in/michal-mikolas
	nanuqcz@gmail.com
"""


###############################################################################
# CONFIG
###############################################################################
timeout = 60

def init():
	start_chrome('https://new-partners.mallgroup.com/login')

	write('', into='Email')
	write('', into='Heslo')
	click(u'Přihlásit')

	wait_until(
		S('div.v-data-table tbody tr td:nth-child(12)').exists,
		timeout_secs=timeout
	)

def get_rows():
	return find_all(S('div.v-data-table tbody tr'))

def get_data(row):
	return {
		'id': row.web_element.find_element_by_css_selector('td:nth-child(3)').text,
		'mall_id': row.web_element.find_element_by_css_selector('td:nth-child(4)').text,
		'name': row.web_element.find_element_by_css_selector('td:nth-child(5)').text,
		'price': row.web_element.find_element_by_css_selector('td:nth-child(6)').text.replace(' ', '').replace(u'Kč', ''),
		'payment': row.web_element.find_element_by_css_selector('td:nth-child(7)').text,
		'delivery': row.web_element.find_element_by_css_selector('td:nth-child(8)').text,
		'package_id': row.web_element.find_element_by_css_selector('td:nth-child(9)').text,
		'opened_date': row.web_element.find_element_by_css_selector('td:nth-child(10)').text,
		'delivery_date': row.web_element.find_element_by_css_selector('td:nth-child(11)').text,
		'delivered_date': row.web_element.find_element_by_css_selector('td:nth-child(12)').text,
		'status': row.web_element.find_element_by_css_selector('td:nth-child(13)').text,
		'detail': lambda row_data: click(row_data['id']),
	}

def next_page():
	click(S('div.v-data-footer__icons-after button'))
	wait_until(lambda:
		not S('div.v-select__selection.v-select__selection--comma.v-select__selection--disabled').exists(),
		timeout_secs=timeout
	)

def has_next_page():
	return not S('div.v-data-footer__icons-after button[disabled]').exists()

def wait_for_detail():
	wait_until(S('main .v-card.custom-card .row .col-sm-4:nth-child(1) div').exists)

def get_detail_data():
	cont = S('main .v-card.custom-card .row .col-sm-4:nth-child(1) div')
	return {
		'email': cont.web_element.find_element_by_css_selector('div:nth-child(3)').text,
		'phone': cont.web_element.find_element_by_css_selector('div:nth-child(4)').text,
	}

def exit_detail():
	click(u'Všechny objednávky')
	wait_until(lambda:
		not S('div.v-select__selection.v-select__selection--comma.v-select__selection--disabled').exists(),
		timeout_secs=timeout
	)

def save_data(data):
	with open(file='output.csv', mode='a+', encoding='utf-8', newline='') as file:
		writer = csv.writer(file)
		for row_data in data:
			writer.writerow(row_data.values())


###############################################################################
# Log
###############################################################################
class Log():
	def add_url(self, url):
		with open('log.txt', mode='a+', encoding='utf-8') as log_file:
			log_file.write(url + '\n')

	def get_urls(self):
		with open('log.txt', mode='r', encoding='utf-8') as log_file:
			return log_file.readlines()

	def has_url(self, url):
		urls = self.get_urls()
		return url in urls


###############################################################################
# Statistics
###############################################################################
class Stats():
	start_time = time.time()
	counter = 0

	def add(self, count):
		self.counter += count

	def print(self):
		now = time.time()

		running = now - self.start_time
		hours = math.floor(running / 60 / 60)
		minutes = math.floor(running / 60) - (hours * 60)
		seconds = running - (minutes * 60) - (hours * 60 * 60)

		print('')
		print('############################################################')
		print('# Running:  %02d:%02d:%02d'    % (hours, minutes, seconds))
		print('# Scrapped: %s items'          % format(self.counter, ',').replace(',', ' '))
		print('# Speed:    %d items / minute' % (self.counter / running * 60))
		print('############################################################')
		print('')


###############################################################################
# Scrapper
###############################################################################
stats = Stats()
log = Log()
init()
while True:
	# Get rows data
	data = []
	rows = get_rows()
	for row in rows:
		row_data = get_data(row)
		data.append(row_data)

	# Rows detail?
	for row_data in data:
		if 'detail' in row_data:
			if isinstance(row_data['detail'], str):
				# TODO handling detail URL
				pass

			if hasattr(row_data['detail'], '__call__'):
				try:
					row_data['detail'](row_data)
					wait_for_detail()

					row_data.update(get_detail_data())

					exit_detail()
				except:
					print('\n! Scrapping detail of this item failed:', row_data, '\n')

	# Save rows data
	save_data(data)
	log.add_url(get_driver().current_url)

	# Statistics
	stats.add(len(rows))
	stats.print()

	# Handle pagination
	if not has_next_page():
		break
	next_page()

input('Done.')
