import csv 

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://en.wikipedia.org"
URL = BASE_URL + "/wiki/Member_states_of_the_United_Nations"

response = requests.get(URL)

response.raise_for_status()

html_doc = BeautifulSoup(response.text, 'html.parser')
table = html_doc.find('table', class_='wikitable')

countries = []

rows = table.find_all('tr')
for row in rows:
    name_link = row.th.a
    if name_link is not None:
        name = name_link.string
        date = row.td.span.string
        country_dict = {
            'Name': name,
            'Date of Admission': date,
            'URL': name_link['href']
        }
        countries.append(country_dict)

info_to_save = []
for country in countries:
    new_url=BASE_URL+country['URL']
    new_response = requests.get(new_url)

    new_response.raise_for_status()

    new_html_doc = BeautifulSoup(new_response.text,'html.parser')

    
    latitude = new_html_doc.find('span', class_='latitude').string
    longitude = new_html_doc.find('span', class_='longitude').string
    coordinates = latitude+longitude
    info = {
        'Name': country['Name'],
        'Date of Admission': country['Date of Admission'],
        'Coordinates': coordinates,
        'Complete URL': new_url
             }
    info_to_save.append(info)

#salva de fato o arquivo
with open ('countries.csv', 'w') as file:
    writer = csv.DictWriter(file,fieldnames=['Name','Date of Admission','Coordinates','Complete URL'])
    writer.writeheader()
    writer.writerows(info_to_save)


