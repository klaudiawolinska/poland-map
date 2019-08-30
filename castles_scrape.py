from bs4 import BeautifulSoup
import requests
import pandas as pd

url = 'https://zamki.net.pl/gps.php'
response = requests.get(url)
content = BeautifulSoup(response.text, 'html.parser')

# get a list of all URLs which have to be opened
all_urls = list(content.find_all('a'))

castles_urls = [link for link in all_urls if 'gps-info.php' in str(link)]

urls_clean = [str(link).split('"')[1] for link in castles_urls]

urls_clean = [link.replace('amp;', '').replace(' ', '%') for link in urls_clean]

urls_clean = ['https://zamki.net.pl/' + link for link in urls_clean]

# empty lists to which website data will be written
castle_name_all = []
longitude_all = []
latitude_all = []

# iterate through all URLs to retrieve data
for url in urls_clean:
    response = requests.get(url)
    content = BeautifulSoup(response.text, 'html.parser')

    castle_name = str(content.find(class_='nagl')).split('<')[-2].split('>')[-1]
    castle_name_all.append(castle_name)

    longitude = str(content.find_all('div', id='licznik')[-1]).split(' ')[-1].split('<')[0]
    longitude_all.append(longitude)

    latitude = str(content.find_all('div', id='licznik')[-1]).split(' ')[-2].split('<')[0]
    latitude_all.append(latitude)

# remove Polish characters
castle_name_temp = [castle.encode('unicode_escape') for castle in castle_name_all]

castle_name_temp = [str(castle).replace("b'", "").replace("'", "").replace("\\\\xc3\\\\xb3", "o") for castle in
                    castle_name_temp]

castle_name_temp = [castle.replace("\\\\xc5\\\\x82", "l") for castle in castle_name_temp]
castle_name_temp = [castle.replace("\\\\xc4\\\\x85", "a") for castle in castle_name_temp]
castle_name_temp = [castle.replace("\\\\xc5\\\\xbc", "z") for castle in castle_name_temp]
castle_name_temp = [castle.replace("\\\\xc4\\\\x99", "e") for castle in castle_name_temp]
castle_name_temp = [castle.replace("\\\\xc5\\\\x9b", "s") for castle in castle_name_temp]
castle_name_temp = [castle.replace("\\\\xc5\\\\x84", "n") for castle in castle_name_temp]
castle_name_temp = [castle.replace("\\\\xc5\\\\xba", "z") for castle in castle_name_temp]
castle_name_temp = [castle.replace("\\\\xc5\\\\x81", "L") for castle in castle_name_temp]
castle_name_temp = [castle.replace("\\\\xc5\\\\x9a", "S") for castle in castle_name_temp]
castle_name_temp = [castle.replace("\\\\xc5\\\\xbb", "Z") for castle in castle_name_temp]

castle_name_clean = castle_name_temp.copy()

# zip lists into pandas DataFrame
castles_poland = pd.DataFrame(list(zip(castle_name_clean, latitude_all, longitude_all)),
                              columns=['castle', 'lat', 'long'])

# export data to CSV
castles_poland.to_csv('castles.csv', index=False)
