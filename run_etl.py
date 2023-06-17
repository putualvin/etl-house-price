from web_scrapper import Scraper
import pandas as pd
import os

web_scrap = Scraper()

df = pd.read_csv('House Price/Scrap Output.csv')
web_scrap.transform(df)
web_scrap.load(df, 'public')