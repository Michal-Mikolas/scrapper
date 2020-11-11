import classes


class MallPartnersWebAdapter(classes.WebAdapter):
	pass


######  ######

scrapper = classes.Scrapper(
	MallPartnersWebAdapter(),
	classes.CsvStorage()
)
scrapper.scrap_data()

######  ######

init()
wait_until(in_list, timeout_secs=timeout)
struggle(restore_page, attempts, lambda: print('! Pagination restore failed.'))

while True:
	try:
		pages_scrapped = False
		while not pages_scrapped:
			try:
				# Get rows data
				data = []
				rows = get_rows()
				for row in rows:
					row_data = struggle(
						lambda: get_data(row),
						attempts,
						lambda: print('! Scrapping list failed.')
					)
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

				pages_scrapped = True

			except HealedToLastPage:
				pass

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

	except HealedToInit:
		# Restore last visited page
		page_restored = False
		while not page_restored:
			try:
				struggle(restore_page, attempts, lambda: print(
					'! Pagination restore failed.'))
				page_restored = True
			except:
				pass


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
