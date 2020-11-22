import scrapper


class AlzaWebAdapter(scrapper.WebAdapter):

	def __init__(self, start_url):
		self.start_url = start_url
