from bs4 import BeautifulSoup
import requests
import pandas as pd
import unidecode


url = 'https://en.wikipedia.org/wiki/List_of_registered_museums_in_Poland'
response = requests.get(url)
content = BeautifulSoup(response.text, 'html.parser')

wikitable = content.find(class_='wikitable')
tr_tags = wikitable.find_all('tr')[1:]

td_tags = []

for tag in tr_tags:
    td_tags.append(tag.find_all('td'))

# leave only second and third element of every table row (Polish Name and Location)
for tag in td_tags:
    del tag[0]
    del tag[-1]

# get contents of tags
for tag in td_tags:
    tag[0] = tag[0].contents[0]
    tag[1] = tag[1].find('a').contents[0]

for tag in td_tags:
    tag[0] = str(tag[0])
    tag[1] = str(tag[1])

museum_decode = [unidecode.unidecode(tag[0]) for tag in td_tags]
city_decode = [unidecode.unidecode(tag[1]) for tag in td_tags]

# convert to pandas DataFrame
museums = pd.DataFrame(list(zip(museum_decode, city_decode)), columns=['museum','city'])

# export data to CSV
museums.to_csv('museums.csv', index=False)
