from extract import Scraper

host = 'localhost'
port = 5432
database = 'data_engineer_project'
user = 'postgres'
password = input("Enter password: ")
web_scrap = Scraper(host=host,
                    port = port,
                    database= database,
                    user = user,
                    password = password)

web_scrap.main()