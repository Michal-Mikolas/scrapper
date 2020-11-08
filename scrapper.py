#!/usr/bin/env python3
from helium import *
import time
import math

"""
Web scrapper

Created by Michal Mikolas
	https://www.linkedin.com/in/michal-mikolas
	nanuqcz@gmail.com
"""


###############################################################################
# CONFIG
###############################################################################
def init():
	start_chrome('https://aukro.cz/notebooky-netbooky?endingTime=9&endingTime_enabled=1&offerTypeAuction=2&order=d&price_enabled=1&price_to=1059&a_enum%5B9844%5D%5B20%5D=20&a_enum%5B9844%5D%5B30%5D=30&a_enum%5B9844%5D%5B40%5D=40&a_enum%5B9844%5D%5B50%5D=50')
	wait_until(S('products-list list-view list-card').exists)

def get_rows():
	return find_all(S('products-list list-view list-card'))

def get_data(row):
	return {
		# 'name': S('h2', below=row).web_element.text,
		# 'price': S('.buy-price', below=row).web_element.text
		'name': row.web_element.find_element_by_css_selector('h2').text,
		'price': row.web_element.find_element_by_css_selector('.buy-price').text
	}

def next_page():
	click('chevron_right')
	wait_until(lambda: not S('products-list.searching').exists())

def has_next_page():
	a = S('a.page-number.next')
	b = S('a.page-number.next').exists()
	return S('a.page-number.next').exists()

def save_data(data):
	print('TODO')


###############################################################################
# Statistics
###############################################################################
class stats():
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
		print('# Running:  ' + str(hours), ':' + str(minutes), ':' + str(round(seconds)))
		print('# Scrapped: ' + str(self.counter) + ' items')
		print('# Speed:    ' + str(round(self.counter / running * 60)) + ' items / minute')
		print('############################################################')
		print('')


###############################################################################
# Scrapper
###############################################################################
stats = stats()
init()
while True:
	# Get rows data
	data = []
	rows = get_rows()
	for row in rows:
		row_data = get_data(row)
		# print('found ', row_data['name'])
		data.append(row_data)

	stats.add(len(rows))
	stats.print()

	# Rows detail?

	# Save rows data
	save_data(data)

	# Handle pagination
	if not has_next_page():
		break
	next_page()

input('Done.')
