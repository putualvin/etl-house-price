# ETL HOUSE PRICE
A beginner data engineer project. A simple project to condact ETL and practicing what I learnt from the bootcamp. Extracted house price data from web scrap using python, transform, and loading to database.

## Requirements
- PostgreSQL Database
- Python
- SQL
- VSCode

## How To Run
- ```webscraper.py ``` contains all the script needed to run the program. It is python class that can be used to extract, transform, and load data into database.
  - ```connection_config``` is used to read json for credentials of the database
  - ```psql_conn``` to create a connection to the database
  - ```Scraper()``` is a class that contains the necessary script to connect to the database. Inside the scraper there are extract, transform, and load.
    - ```main()``` to run all extract, transform, load all together
    - ```extract()``` to extract all the necessary information from rumah123.com . It is in a form of a loop, but if you want to extract only one you can use the scrpt starting after the for loop.
    - ```transform()``` after it is extracted the format is not cleaned. The transform is used to clean the data so it can be uploaded and used for analysis
    - ```load()``` the final step of the script. To upload the file to database
- ```run_etl.py``` to run the script from the webscrapper.py

