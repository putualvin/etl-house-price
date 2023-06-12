import requests
from bs4 import BeautifulSoup
from selenium import webdriver
import pandas as pd
import itertools
import re
import psycopg2
from sqlalchemy import create_engine


        
class Scraper():
    def __init__(self,
                 host,
                 port,
                 database,
                 user,
                 password):
        self.header = {"user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36"}
        self.host = host
        self.port = port
        self.database = database
        self.user = user
        self.password = password
        
    def connect_database(
    self,
    host,
    port,
    database,
    user,
    password):
        conn = psycopg2.connect(
            host = host,
            port = port,
            database = database,
            user = user,
            password = password
        )
        conn.set_session(autocommit=True)
        cur = conn.cursor()
        
        return conn, cur
    
    def main(self):
        df = self.extract()
        merged_df = df.transform()

    def extract(self):
        #Define header
        merged_df = pd.DataFrame()
        r = requests.get(url,headers=self.header)
        c = r.content
        page = BeautifulSoup(c, 'html.parser')
        all_tempat = page.find_all('div',class_='ui-organism-intersection__element intersection-card-container')
        place_name = []
        address = []
        lb = []
        kt = []
        price = []
        mortage = []
        date_posted = []
        tayang = []
        #Preparing list of files
        page_list = [*range(1,101)]
        city_list = ['dki-jakarta','bekasi','tangerang','bogor','depok']
        place_category = ['apartemen', 'rumah']
        place_ownership = ['jual', 'sewa']
        df = pd.DataFrame()
        for ownership, city, category, page in itertools.product(place_ownership,city_list, place_category, page_list):
            url = f'https://www.rumah123.com/{ownership}/{str(city)}/{category}/?page={str(page)}#qid~42eeef39-13df-4144-afa7-f1229e9827be'
            r = requests.get(url,headers=header)
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
                    address = i.find('div', class_='card-featured__middle-section').find('span',text = re.compile(",")).text
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
                    mortage = i.find('div', class_='card-featured__middle-section__price').find('em').text.replace("Cicilan:", "").strip()
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
                # df.to_csv(os.path.join(path_output, f'{page}_{ownership}_{city}.csv'), index=False, sep = ';')
                
                merged_df = merged_df.append(df)
                print(f"Current city {city} page {page}")
                
                return merged_df
            
     def transform(self, df):
         #Drop null values
        df = df.dropna()
        #Drop duplicated values
        df = df.drop_duplicates(subset='place_name')
        
        #Assigning kecamatan and city
        df[['kecamatan','city']] = df.address.str.split("," ,expand = True)
        df = df.drop(columns=['address'])
        df.head()
        #Cleaning price column
        df[['rp','new_price','number']] = df['price'].str.split(" ", expand = True)
        #Function to determine new price
        def new_price(a):
            if 'Miliar' in a:
                return 1000000000
            else:
                return 1000000
        df['amount'] = df.price.apply(lambda x: new_price(x))
        df['price'] = df.price.str.replace("Rp","").str.replace("Miliar", "").str.replace("Juta","").str.replace(",",".").str.strip().astype('float')
        df['final_price'] = df['price'] * df['amount']
        df = df.drop(columns = ['price', 'new_price', 'rp', 'amount'])
        
        #Cleaning Area
        df['area'] = df.area.str.replace("m²","").str.strip().astype('float')
        
        #Cleaning Date Posted
        df[['Nama','Date Posted']] = df['date_posted'].str.split("sejak", expand=True)
        df[['day','month','year']] = df['Date Posted'].str.split(" ", expand=True)
        list_month = ['06', '05', '12', '02', '04', '03',
       '01']
        df['month'] = df['month'].replace(df['month'].unique(), list_month)
        df['date'] = df['day'] + '/' +df['month']+'/'+df['year']
        df = df.drop(columns=['Unnamed: 0','Date Posted', 'day', 'month', 'year','date_posted','Nama'])
        
        return df
        
    def create_engine(self):
        engine = create_engine(f'postgresql+psycopg2://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}')
        print("Engine Created")
        return engine
            
            
    def load(self, df, conn, cur, engine,schema):
        cur.execute('''
                        drop table if exists house_price
                    ''')
        df.to_sql(
            'house_price',
            engine,
            schema,
            if_exists = 'replace',
            index = False
        )
        
            
        
            