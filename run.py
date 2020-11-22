import scrapper
from mall_partner_web_adapter import MallPartnerWebAdapter


scrapper = scrapper.Scrapper(
	MallPartnerWebAdapter(),
	scrapper.CsvUniqueStorage('mall_partner.csv', 'mall_partner.unique.csv')
)
scrapper.run(scrapper.MODE_NATURAL)


input('Done.')
