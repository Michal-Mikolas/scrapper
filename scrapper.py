from helium import *
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

	###### PAGINATION ######

	def next_page(self):
		pass

	def has_next_page(self):
		pass

	def get_page_id(self):
		return get_driver().current_url

	def store_page(self):
		page_id = self.get_page_id()
		with open(self.get_name() + '.lastpage', 'w') as file:
			file.write(page_id)

	def restore_page(self):
		with open(self.get_name() + '.lastpage', 'a+') as file:
			# a+ creates file if not exist and move the cursor to the file end
			file.seek(0)
			last_id = file.read().strip()

		if last_id:
			while self.get_page_id() != last_id:
				self.next_page()

	###### DETAIL ######

	def in_detail(self):
		pass

	def get_detail_data(self):
		pass

	def exit_detail(self):
		pass

	###### HELPERS ######

	def scroll_top(self):
		get_driver().execute_script(
			"window.scroll({top: 0, left: 0, behavior: 'smooth'})"
		)

	def scroll_bottom(self):
		get_driver().execute_script(
			"window.scroll({top: document.body.scrollHeight, left: document.body.scrollWidth, behavior: 'smooth'})"
		)

	def scroll_all(self):
		"""
		Used for web pages with lazy-loading elements which renders only when visible
		"""
		total_height = get_driver().execute_script("return document.body.scrollHeight")
		page_height = get_driver().execute_script("return window.innerHeight")

		scroll_y = 0
		while True:
			get_driver().execute_script("window.scroll({top: %d, left: 0})" % scroll_y)
			time.sleep(.3)

			scroll_y += page_height
			if (scroll_y >= total_height):
				break

	def scrool_to(self, element, offset_top=0):
		# TODO finish this method!!!

		# element = S('#pagerbottom a.fa-chevron-right').web_element
		coordinates = element.location_once_scrolled_into_view
		print(coordinates)
		get_driver().execute_script("arguments[0].scrollIntoView();", element)
		print(element.get_attribute('href'))
		time.sleep(3)

	###### INTERNAL ######

	def get_name(self):
		return self.__class__.__name__.replace('WebAdapter', '')


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

	def add_data(self, data):
		pass

	def finish(self):
		pass


class CsvStorage():

	def __init__(self, filename='output.csv'):
		self.filename = filename

	def add_data(self, data):
		with open(file=self.filename, mode='a+', encoding='utf-8', newline='') as file:
			writer = csv.writer(file)
			for row_data in data:
				writer.writerow(row_data.values())


class CsvUniqueStorage(CsvStorage):

	def __init__(self, filename='output.csv', unique_filename='output.unique.csv'):
		super().__init__(filename)
		self.unique_filename = unique_filename

	def finish(self):
		lines_seen = set()  # holds lines already seen
		with open(self.unique_filename, "w", encoding='utf-8', newline='') as output_file:
			for line in open(self.filename, "r", encoding='utf-8'):
				if line not in lines_seen:  # check if line is not duplicate
					output_file.write(line)
					lines_seen.add(line)


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

	def add(self, data):
		self.counter += len(data)

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


 #####
#     #  ####  #####    ##   #####  #####  ###### #####
#       #    # #    #  #  #  #    # #    # #      #    #
 #####  #      #    # #    # #    # #    # #####  #    #
      # #      #####  ###### #####  #####  #      #####
#     # #    # #   #  #    # #      #      #      #   #
 #####   ####  #    # #    # #      #      ###### #    #
class Scrapper():
	MODE_NATURAL = 'mode_natural'
	MODE_PAGE = 'mode_page'
	MODE_END = 'mode_end'


	###### PUBLIC API ######


	def __init__(self, web_adapter: WebAdapter, storage: Storage, verbosity=2, timeout=30, fail_attempts=3):
		self.web = web_adapter
		self.storage = storage
		self.verbosity = verbosity
		self.timeout = timeout
		self.fail_attempts = fail_attempts
		self.stats = Stats()


	def run(self, mode='mode_natural'):
		if mode == self.MODE_NATURAL:
			return self.scrap_mode_natural()


	def scrap_mode_natural(self):
		self.init()
		self.restore_page()

		while True:
			try:
				page_scrapped = False
				while not page_scrapped:
					try:
						# Get rows data
						data = []
						rows = self.web.get_rows()
						for row in rows:
							row_data = self.get_data(row)
							data.append(row_data)

						# Rows detail?
						for row_data in data:
							if 'detail' in row_data:
								self.open_detail(row_data)
								row_data.update(self.web.get_detail_data())
								self.exit_detail(row_data)

						page_scrapped = True

					except HealedToLastPage:
						pass

				# Save rows data
				self.add_data(data)
				self.store_page()

				# Statistics
				self.stats.add(data)
				if self.verbosity >= 1:
					self.stats.print()

				# Handle pagination
				if not self.web.has_next_page():
					break
				self.next_page()

			except HealedToInit:
				# Restore last visited page
				self.try_forever(self.restore_page)

		self.finish()


	###### INTERNAL ######


	def init(self):
		if self.verbosity >= 2:
			print('Scrapper: Initialising web page...')

		self.web.init()
		wait_until(self.web.in_list, timeout_secs=self.timeout)


	def restore_page(self):
		if self.verbosity >= 2:
			print('Scrapper: Restoring pagination...')

		self.struggle(
			self.web.restore_page,
			self.fail_attempts,
			lambda: print('! Pagination restore failed.')
		)


	def get_data(self, row):
		if self.verbosity >= 2:
			print('Scrapper: Fetching items from page...')

		return self.struggle(
			lambda: self.web.get_data(row),
			self.fail_attempts,
			lambda: print('! Scrapping list failed.')
		)


	def open_detail(self, row_data):
		if self.verbosity >= 2:
			print('Scrapper: Opening item detail...')

		self.struggle(
            lambda: self.open_detail_unsafe(row_data),
            self.fail_attempts,
            lambda: print('! Opening detail of this item failed:', row_data)
        )


	def open_detail_unsafe(self, row_data):
		if isinstance(row_data['detail'], str):
			get_driver().get(row_data['detail'])

		if hasattr(row_data['detail'], '__call__'):
			row_data['detail'](row_data)

		wait_until(self.web.in_detail, timeout_secs=self.timeout)


	def exit_detail(self, row_data):
		if self.verbosity >= 2:
			print('Scrapper: Exiting item detail...')

		self.struggle(
            self.web.exit_detail,
            self.fail_attempts,
            lambda: print('! Exiting detail of this item failed:', row_data)
        )


	def add_data(self, data):
		if self.verbosity >= 2:
			print('Scrapper: Adding data from current page to storage...')

		self.struggle(
            lambda: self.storage.add_data(data),
            self.fail_attempts,
            lambda: (print('! Adding data to storage failed'), self.heal_to_init())
        )


	def store_page(self):
		if self.verbosity >= 2:
			print('Scrapper: Storing current pagination position...')

		self.struggle(
            self.web.store_page,
            self.fail_attempts,
            lambda: (print('! Storing page ID failed'), self.heal_to_init())
        )


	def next_page(self):
		if self.verbosity >= 2:
			print('Scrapper: Going to next page...')

		self.struggle(
			self.web.next_page,
			self.fail_attempts,
			lambda: print('! Next page failed to load.')
		)


	def finish(self):
		if self.verbosity >= 2:
			print('Scrapper: Finishing...')

		self.storage.finish()


	###### SOLUTINON FOR NON-STABLE WEB PAGES ######


	def struggle(self, func, attempts=3, fail_func=None, try_to_heal=True):
		fails = 0
		while fails < attempts:  # TODO self.fail_attempts ?
			try:
				return func()
			except Exception as e:
				fails += 1
				print("! Something went wrong, didn't work for %d. time." % fails)
				print("- exception:", e.__class__.__name__ + ':', e)

		if fail_func:
			fail_func()

		if try_to_heal:
			self.heal()


	def heal(self):
		try:
			print('! Trying to heal to last page...')  # TODO heal max 3x for one page?
			if not self.web.in_list():
				self.struggle(
					self.web.exit_detail,
					self.fail_attempts,
					lambda: print('! Healing to the last page failed...'),
					try_to_heal=False
				)

			raise HealedToLastPage

		except HealedToLastPage:
			raise HealedToLastPage

		except:
			self.heal_to_init()


	def heal_to_init(self):
		print('\n! Weird stuff happened. Re-initialising...')
		get_driver().quit()

		self.struggle(self.web.init, self.fail_attempts, lambda: print('! Re-initialising failed. '))
		wait_until(self.web.in_list, timeout_secs=self.timeout)

		raise HealedToInit


	def try_forever(self, func):
		success = False
		while not success:
			try:
				func()
				success = True
			except:
				pass


class HealedToLastPage(Exception):
	pass


class HealedToInit(Exception):
	pass
