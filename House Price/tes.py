import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import os
import glob
import itertools
import matplotlib.pyplot as plt
## Preparation for Web Scarpping
#Define header
header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"}
#Preparing list of files
page_list = [*range(1,101)]
city_list = ['dki-jakarta','bekasi','tangerang','bogor','depok']
place_category = ['apartemen', 'rumah']
place_ownership = ['jual', 'sewa']
for ownership, city, category, page in itertools.product(place_ownership,city_list, place_category, place_ownership):
    url = f'https://www.rumah123.com/{ownership}/{str(city)}/{category}/?page={str(page)}#qid~42eeef39-13df-4144-afa7-f1229e9827be'
    r = requests.get(url, headers = header)
    c = r.content
    page = BeautifulSoup(c, 'html.parser')
    all_city = page.find_all('div',class_='ui-organism-intersection__element intersection-card-container')
    place_name = []
    place_address = []
    building_area = []
    num_bedroom = []
    place_price = []
    place_mortage = []
    date_posted = []
for i in all_city:
    try:
        name = i.find('a').find('h2').text
    except:
        name = None
    try:
        address = i.find('p', class_='card-featured__middle-section__location').text
    except:
        address = None
    try:
        bedroom = i.find('span', class_='attribute-text').text
    except:
        bedroom = None
    try:
        area = i.find('div', class_='attribute-info').find('span').text
    except:
        area = None
    try:
        price = i.find('div', class_='card-featured__middle-section__price').find('strong').text
    except:
        price = None
    try:
        mortage = i.find('div', class_='ui-organisms-card-r123-featured__middle-section__price').find('em').text.replace("Cicilan:", "").strip()
    except:
        mortage = None
    try:
        jadwal = i.find('div', class_='ui-organisms-card-r123-basic__bottom-section__agent').text
    except:
        jadwal = None
    place_name.append(name)
    place_address.append(address)
    num_bedroom.append(bedroom)
    building_area.append(area)
    place_price.append(price)
    place_mortage.append(mortage)
    date_posted.append(jadwal)
    df = pd.DataFrame({'place_name':place_name, 'address':place_address, 'bedroom':num_bedroom, 'area':building_area,
                            'price':place_price, 'mortage':place_mortage, 'category': category, 'date_posted':date_posted})
    # path_output = r'Scrap Output'
    print(f"Currently Working at page: {page}, City: {city}, Ownership: {ownership}")
    # df.to_csv(os.path.join(path_output, f'{page}_{ownership}_{city}.csv'), index=False, sep = ';')
    df.to_csv(f'{page}_{ownership}_{city}.csv', index = False, sep = ';')

df.to_csv('tes1.csv')