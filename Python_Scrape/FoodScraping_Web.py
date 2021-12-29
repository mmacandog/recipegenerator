import requests
from bs4 import BeautifulSoup
import pandas as pd
#
# nyt_dishes = None
# se_dishes = None
# ba_dishes = None
# food52_dishes = None
# epicurious_dishes = None


def nyt_scrape():
    global nyt_dishes

    # Scraping NYT Cooking Most Popular Dishes 2021

    response = requests.get(url="https://cooking.nytimes.com/68861692-nyt-cooking/37282773-our-50-most-popular-recipes-of-2021")
    data = BeautifulSoup(response.content, 'html.parser')

    # # finding parent <ul> tag
    # results = data.find("div", class_="recipes track-card-params").find_all("h3", class_="name")
    #
    # results = []

    dishes = []
    for i in data.find_all("a", class_="card-recipe-info card-link"):
        dishes.append((i.find("h3", class_="name").text.strip()))

    links = []
    for i in data.find_all("a", class_="card-recipe-info card-link"):
        links.append("https://cooking.nytimes.com/"+format(i.get("href")))

    images = []
    for i in data.find_all("img"):
        images.append(format(i["src"]))
        # print(i["src"])

    nyt_dishes = pd.DataFrame(zip(dishes, links, images), columns=["Dishes", "Links", "Image"])
    print(nyt_dishes)

    nyt_dishes.to_csv(r'/Users/marrionmac/PycharmProjects/PersonalProjects/nytbest50_2021.csv', index = False)

def se_scrape():
    global se_dishes

    # Scraping Serious Eats Most Popular Dishes 2021
    response = requests.get(url="https://www.seriouseats.com/favorite-recipes-2021-5213870")
    data = BeautifulSoup(response.content, 'html.parser')

    # finding parent <ul> tag
    results = data.find_all("a", class_="mntl-sc-block-heading__link")

    dishes = []
    for i in results:
        dishes.append(i.text.strip())

    links = []
    images = []
    for i in data.find_all("a", class_="mntl-sc-block-heading__link"):
        links.append(format(i.get("href")))
        images.append(format(i["src"]))

    print(images)

    # se_dishes = pd.DataFrame(zip(dishes, links), columns=["Dishes", "Links"])
    # se_dishes.to_csv(r'/Users/marrionmac/PycharmProjects/PersonalProjects/seriouseats_2021.csv',index=False)
    # print(se_dishes)


def ba_scrape():
    global ba_dishes
    # Scraping Bon Appetite Most Popular Dishes 2021
    response = requests.get(url="https://www.bonappetit.com/gallery/most-popular-recipes-2021")
    data = BeautifulSoup(response.content, 'html.parser')

    dishes = []
    for i in data.find_all(class_="BaseWrap-sc-TURhJ GallerySlideCaptionHedText-cZHlsU eTiIvU"):
        dishes.append(i.text.strip())

    links = []
    for i in data.find_all("a", class_="BaseButton-aWfgy ButtonWrapper-dOcxiw bxdYtG kBzOGK button button--utility GallerySlideCaptionButton-hNHUKu hTfhDO"):
        links.append(i.get("href"))


    # remove digits
    import re
    dishes = [re.sub('[.0123456789]', '', _) for _ in dishes]

    ba_dishes = pd.DataFrame(zip(dishes, links), columns=["Dishes", "Links"])
    ba_dishes.to_csv(r'/Users/marrionmac/PycharmProjects/PersonalProjects/ba_2021.csv',index=False)


def food52_scrape():

    global food52_dishes
    # Scraping Food52.com Most Popular Dishes 2021
    response = requests.get(url="https://food52.com/blog/26920-top-10-genius-recipes-of-2021")
    data = BeautifulSoup(response.content, 'html.parser')

    # finding objects using class
    results = data.find_all("a", class_="card__link")

    dishes = []
    for link in data.find_all("a", class_="card__link"):
        dishes.append(link.text.strip())

    links = []
    for i in data.find_all("a", class_="card__link"):
        links.append("https://food52.com"+format(i.get("href")))


    food52_dishes = pd.DataFrame(zip(dishes, links), columns=["Dishes", "Links"])
    food52_dishes.to_csv(r'/Users/marrionmac/PycharmProjects/PersonalProjects/food52_2021.csv',index=False)


def epicurious_scrape():
    global epicurious_dishes
    # Scraping Food52.com Most Popular Dishes 2021
    response = requests.get(url="https://www.epicurious.com/recipes-menus/the-most-popular-recipes-2021-gallery")
    data = BeautifulSoup(response.content, 'html.parser')

    # finding objects using class
    results = data.find_all("h2", class_="BaseWrap-sc-TURhJ BaseText-fFzBQt GallerySlideCaptionHed-lgowel eTiIvU iSweUE kDNKaZ")

    dishes = []
    for i in results:
        dishes.append(i.text.strip())

    links = []
    for i in data.find_all("a", class_="BaseButton-aWfgy ButtonWrapper-dOcxiw irSbmz kkOEhI button button--utility GallerySlideCaptionButton-hNHUKu hTfhDO"):
        links.append(format(i.get("href")))

    epicurious_dishes = pd.DataFrame(zip(dishes, links), columns=["Dishes", "Links"])
    epicurious_dishes.to_csv(r'/Users/marrionmac/PycharmProjects/PersonalProjects/epicurious_2021.csv',index=False)


def combine_df():
    nyt_scrape()
    se_scrape()
    epicurious_scrape()
    ba_scrape()
    food52_scrape()

    # Combine all df

    combined = pd.concat([nyt_dishes, se_dishes, ba_dishes, epicurious_dishes, food52_dishes])
    # combined.to_csv(r'/Users/marrionmac/PycharmProjects/PersonalProjects/combined_2021.csv',index=False)
    print(combined)


if __name__ == "__main__":
    se_scrape()