#!/usr/bin/env python3
from helium import *
from selenium.webdriver.common.keys import Keys
import time
import math
import csv
import re

"""
Web scrapper

Created by Michal Mikolas
	https://www.linkedin.com/in/michal-mikolas
	nanuqcz@gmail.com
"""


###############################################################################
# CONFIG
###############################################################################
timeout = 30
attempts = 3

def init():
	start_chrome('https://new-partners.mallgroup.com/login')

	write('info@davigon.cz', into='Email')
	write('Korona3184', into='Heslo')
	click(u'Přihlásit')

	wait_until(in_list, timeout)
	time.sleep(1)
	click(S('div.v-data-footer div.v-input__icon i.v-icon'))
	time.sleep(1)
	click('20')
	time.sleep(3)

def in_list():
	return S('div.v-data-table tbody tr td:nth-child(12)').exists()

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

###### DETAIL ######

detail_strategy = 'natural'  # natural|page|finish

def in_detail():
	return S('main .v-card.custom-card .row .col-sm-4:nth-child(1) div').exists()

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

###### RESTORE PAGINATION ######

def get_page_id():
	id = S('div.v-data-footer__pagination').web_element.text
	id = re.sub(' z .*', '', id)

	return id.strip()

def store_page():
	with open('lastpage.txt', 'w') as file:
		file.write(get_page_id())

def restore_page():
	with open('lastpage.txt', 'r') as file:
		last_id = file.read().strip()

	if last_id:
		while get_page_id() != last_id:
			next_page()

###### STORAGE ######

def save_data(data):
	with open(file='output.csv', mode='a+', encoding='utf-8', newline='') as file:
		writer = csv.writer(file)
		for row_data in data:
			writer.writerow(row_data.values())


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
# Struggles
###############################################################################
def struggle(func, attempts = 3, fail_func = None):
	fails = 0
	while fails < attempts:
		try:
			return func()
		except:
			fails += 1
			print("! Something went wrong, didn't work for %d. time." % fails)

	fail_func()
	heal()

def heal():
	print('\n! Weird stuff happened. Re-initialising...')
	get_driver().quit()

	init()
	wait_until(in_list, timeout_secs=timeout)

	raise Healed

class Healed(Exception):
	pass

def open_detail(row_data):
	if isinstance(row_data['detail'], str):
		get_driver().get(row_data['detail'])

	if hasattr(row_data['detail'], '__call__'):
		row_data['detail'](row_data)

	wait_until(in_detail, timeout_secs=timeout)


###############################################################################
# Scrapper
###############################################################################
stats = Stats()

init()
wait_until(in_list, timeout_secs=timeout)
struggle(restore_page, attempts, lambda: print('! Pagination restore failed.'))

while True:
	try:
		# Get rows data
		data = []
		rows = get_rows()
		for row in rows:
			row_data = get_data(row)
			data.append(row_data)

		# Rows detail?
		for row_data in data:
			if 'detail' in row_data:
				struggle(
					lambda: open_detail(row_data),
					attempts,
					lambda: print('! Scrapping detail of this item failed:', row_data)
				)

				row_data.update(get_detail_data())

				struggle(
					exit_detail,
					attempts,
					lambda: print('! Scrapping detail of this item failed:', row_data)
				)

		# Save rows data
		save_data(data)
		store_page()

		# Statistics
		stats.add(len(rows))
		stats.print()

		# Handle pagination
		if not has_next_page():
			break
		struggle(next_page, attempts, lambda: print('! Next page failed to load.'))

	except Healed:
		struggle(restore_page, attempts, lambda: print('! Pagination restore failed.'))


###############################################################################
# Cleaner
###############################################################################

# lines_seen = set()  # holds lines already seen
# with open("output-cleaned.csv", "w") as output_file:
# 	for line in open("output.csv", "r"):
# 		if line not in lines_seen:  # check if line is not duplicate
# 			output_file.write(line)
# 			lines_seen.add(line)

input('Done.')
