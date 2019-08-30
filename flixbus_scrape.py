from bs4 import BeautifulSoup
import requests
import pandas as pd
import unidecode


url = 'https://www.flixbus.pl/autobusy/polska'
response = requests.get(url)
content = BeautifulSoup(response.text, 'html.parser')

hubpage_cities = content.find_all(class_='hubpage__cities')

hubpage_cities = [tag.find_all("a") for tag in hubpage_cities]

# flatten the list
hubpage_cities = [val for sublist in hubpage_cities for val in sublist]

flixbus_cities = [tag.contents for tag in hubpage_cities]

# flatten the list
flixbus_cities = [val for sublist in flixbus_cities for val in sublist]

flixbus_cities = [unidecode.unidecode(city) for city in flixbus_cities]

flixbus = pd.DataFrame(list(flixbus_cities), columns=['city'])

# export data to CSV
flixbus.to_csv('flixbus.csv', index=False)
