from helium import *
import time
import math
import csv
import re


   #
  # #   #####    ##   #####  ##### ###### #####
 #   #  #    #  #  #  #    #   #   #      #    #
#     # #    # #    # #    #   #   #####  #    #
####### #    # ###### #####    #   #      #####
#     # #    # #    # #        #   #      #   #
#     # #####  #    # #        #   ###### #    #
class WebAdapter():

	def init(self):
		pass

	def in_list(self):
		pass

	def get_rows(self):
		pass

	def get_data(self, row):
		pass

	def next_page(self):
		pass

	def has_next_page(self):
		pass

	###### RESTORE PAGINATION ######

	def get_page_id(self):
		pass

	def store_page(self):
		pass

	def restore_page(self):
		pass

	###### DETAIL ######

	def in_detail(self):
		pass

	def get_detail_data(self):
		pass

	def exit_detail(self):
		pass


 #####
#     #  ####  #####    ##   #####  #####  ###### #####
#       #    # #    #  #  #  #    # #    # #      #    #
 #####  #      #    # #    # #    # #    # #####  #    #
      # #      #####  ###### #####  #####  #      #####
#     # #    # #   #  #    # #      #      #      #   #
 #####   ####  #    # #    # #      #      ###### #    #
class Scrapper():

	###### PUBLIC API ######

	def __init__(self, web_adapter, storage, timeout=30, fail_attempts=3):
		pass

	def scrap_data(self, mode='natural'):
		pass

	def scrap_finish_mode(self):
		pass

	###### SOLUTINON FOR NON-STABLE WEB PAGES ######

	def struggle(self, func, attempts=3, fail_func=None, try_to_heal=True):
		pass

	def heal(self):
		pass


 #####
#     # #####  ####  #####    ##    ####  ######
#         #   #    # #    #  #  #  #    # #
 #####    #   #    # #    # #    # #      #####
      #   #   #    # #####  ###### #  ### #
#     #   #   #    # #   #  #    # #    # #
 #####    #    ####  #    # #    #  ####  ######
class Storage():
	def __init__(self):
		pass

	def save(self, data):
		pass

	def finish(self):
		pass


class CsvStorage():
	def __init__(self, filename='output.csv'):
		pass

	def save(self, data):
		pass

	def finish(self):
		pass


class CsvUniqueStorage(CsvStorage):
	def finish(self):
		pass


 #####
#     # #####   ##   #####  ####
#         #    #  #    #   #
 #####    #   #    #   #    ####
      #   #   ######   #        #
#     #   #   #    #   #   #    #
 #####    #   #    #   #    ####
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
		print('# Running:  %02d:%02d:%02d' % (hours, minutes, seconds))
		print('# Scrapped: %s items' % format(self.counter, ',').replace(',', ' '))
		print('# Speed:    %d items / minute' % (self.counter / running * 60))
		print('############################################################')
		print('')
