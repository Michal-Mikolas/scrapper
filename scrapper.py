#!/usr/bin/env python3
from helium import *
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
def init():
	start_chrome('https://new-partners.mallgroup.com/login')

	write('', into='Email')
	write('', into='Heslo')
	click(u'Přihlásit')

	wait_until(S('div.v-data-table tbody tr td').exists, timeout_secs=30)

def get_rows():
	return find_all(S('div.v-data-table tbody tr'))

def get_data(row):
	return {
		'name': row.web_element.find_element_by_css_selector('td:nth-child(5)').text,
		'price': row.web_element.find_element_by_css_selector('td:nth-child(6)').text
	}

def next_page():
	click(S('div.v-data-footer__icons-after button'))
	wait_until(lambda:
		not S('div.v-select__selection.v-select__selection--comma.v-select__selection--disabled').exists(),
		timeout_secs=30
	)

def has_next_page():
	return not S('div.v-data-footer__icons-after button[disabled]').exists()

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
