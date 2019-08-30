from bs4 import BeautifulSoup
import requests
import pandas as pd
import re

letters = 'abcdefghijklmnoprstuwz'

# get urls for letters, like: 'https://latitudelongitude.org/pl/a', 'https://latitudelongitude.org/pl/b', etc.
main_urls = []
for letter in letters:
    main_urls.append("https://latitudelongitude.org/pl/" + letter)

# get urls of specific cities
cities_urls = []

for url in main_urls:
    response = requests.get(url)
    content = BeautifulSoup(response.text, 'html.parser')
    a_tags = content.find(class_="col-full").find_all('a')

    for tag in a_tags:
        cities_urls.append(str(tag))

cities = []

for url in cities_urls:
    cities.append(re.findall(r"[a-z\-]+\/", url))

# flatten list
cities = [val for sublist in cities for val in sublist]

complete_urls = [r"https://latitudelongitude.org/pl/" + city for city in cities]

# from urls of specific cities scrape their coordinates
final_data = []

for url in complete_urls:
    response = requests.get(url)
    content = BeautifulSoup(response.text, 'html.parser')

    final_data.append([url, content.find_all(class_="intro")[0].find('span').contents])

cities = pd.DataFrame(final_data, columns=["city", "coordinates"])

# export data to CSV
cities.to_csv('cities.csv', index=False)
