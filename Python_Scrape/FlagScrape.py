import requests
from bs4 import BeautifulSoup
import pandas as pd

def flag_scrape():

    response = requests.get(url="https://flagpedia.net/emoji")
    data = BeautifulSoup(response.content, 'html.parser')

    table = data.find("table", class_="color")

    countries = []
    for i in table.find_all("td", class_="td-country"):
        countries.append((i.text.strip()))

    flags = []
    for i in table.find_all("td", class_="td-flag"):
        flags.append((i.text.strip()))

    flags_countries = pd.DataFrame(zip(countries, flags),
                                 columns=["Country", "Flag"])

    print(flags_countries)


    # data = []
    # for rows in row[1:]:
    #     cols = row.find_all('td')
    #     print(cols)

if __name__ == "__main__":
    flag_scrape()