import requests
from bs4 import BeautifulSoup


def wiki_scrape():

	global df
	### Scraping Wikipedia: https://www.freecodecamp.org/news/scraping-wikipedia-articles-with-python/
	response = requests.get(url="https://en.wikipedia.org/wiki/National_dish#By_country")
	data = BeautifulSoup(response.content, 'html.parser')

	# finding parent <ul> tag
	parent = data.find("body").find("ul")

	# finding all <li> tags
	text = list(parent.descendants)

	scraped_page = []
	for li in data.find_all("li"):
		scraped_page.append(li.text)

	# Delete everything but the list
	del scraped_page[:(scraped_page.index("Afghanistan: Kabuli palaw[6]"))]
	del scraped_page[(scraped_page.index("Zimbabwe: Sadza[325]"))+1:]


	# Remove brackets and digits from items
	import re
	scraped_page = [re.sub('[0123456789]', '', _) for _ in scraped_page]
	scraped_page = [re.sub('[\n]', "', '", _) for _ in scraped_page]


	new_list = []
	for i in scraped_page:
		new_list.append(i.replace("[]", ""))

	newer_list = []
	for i in new_list:
		newer_list.append(i.split(':'))


	import pandas as pd
	df = pd.DataFrame(newer_list)

	new_df = df[[0, 1]].copy()
	new_df.columns=["Country", "Dish"]

	new_df['Dish'] = new_df['Dish'].str.split("',").str[0]
	df = pd.DataFrame(new_df)

	from pandas import Series
	dishes = new_df['Dish'].str.split(',').apply(Series, 1).stack()
	dishes.index = dishes.index.droplevel(-1)
	dishes.name = 'Dishes'
	del df['Dish']
	df = df.join(dishes)

	# Removing countries with no national dishes
	df = df.set_index("Country")
	df = df.drop(['United States', 'India'])
	df = df.reset_index()


	# df.to_csv(r'/Users/marrionmac/PycharmProjects/wiki_food.csv', index = False)

	## Create google search links for the recipes
	import unicodedata as u
	dishes = df['Dishes']

	normalized = []
	for i in dishes:
		normalized.append(u.normalize('NFKD', i).encode('ascii', 'ignore').decode())

	df['Dish_Normalized'] = normalized

	links = []
	for i in df['Dish_Normalized']:
		search_dish = i
		out_link = "https://www.google.com/search?q=" + '+'.join(search_dish.split(' '))
		links.append(out_link)

	df['Links'] = links

	df['Links'] = df['Links'].str.cat(df['Country'], sep="+")

	# df.to_csv(r'/Users/marrionmac/PycharmProjects/wiki_food.csv', index = False)


def flag_scrape():
	import requests
	from bs4 import BeautifulSoup
	import pandas as pd

	global flags_countries

	response = requests.get(url="https://flagpedia.net/emoji")
	data = BeautifulSoup(response.content, 'html.parser')

	table = data.find("table", class_="color")

	countries = []
	for i in table.find_all("td", class_="td-country"):
		countries.append((i.text.strip()))

	flags = []
	for i in table.find_all("td", class_="td-flag"):
		flags.append((i.text.strip()))

	flags_countries = pd.DataFrame(zip(countries, flags), columns=["Country", "Flag"])


def concat_df():
	import pandas as pd

	wiki_scrape()
	flag_scrape()

	df_wiki = pd.merge(df, flags_countries, on="Country")
	print(df_wiki)
	print(df_wiki.head)
	df_wiki.to_csv(r'/Users/marrionmac/PycharmProjects/wiki_food2.csv', index = False)


if __name__ == "__main__":
	concat_df()



