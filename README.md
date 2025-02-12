# Google news scraper (Assignment-1)

- Roll No : MA24M023
- Name : Satheesh D M

This assignment is written entirely in python. A Shell script is used at last for logging. Postgres DB is used to store scraped data.
## requirements
- python3
- argparse
- configparser
- pandas
- selenium
- psycopg2
- requests
- datetime
## To your notice

- Script summary is given in the beginning of all the ".py" and ".sh" files.  
- Function summary, arguments & return type are explained in detail in all the function.

## Which is where ?

1. Refer ***"scrap_fns.py"*** for solutions to module 1, 2 & 3.
1. Refer ***"postgressdb_fns.py"*** for solutions to module 4 & 5.
1. Refer ***"main.py"*** & ***"gnews_scraper_cron.sh"*** for solution to module 6.

## The approach for scrapping
- G-News page had a repeating hierachy in the html for displaying the news article.
- The ***"extract_image_and_metadata"*** function takes advantage of this structure.
- Though there are different layout blocks like "trendings section, for you section, etc". The hierarchy is still maintained.
- This function first collects all the articles in a layout block using the article class name. Then stores these elements in a python list.
- Then iterates through this list and extracts the image data
    1. image url
    1. uses requests library to get the image data from the extracted url.
- Then collects all the meta data mentioned in the Question.
- Then the extracted info are appended to a python dictionary.




## Overview of the "main.py" (orchestration script)

- First it opens the "https://news.google.com" by default (from config.ini file). in headless mode (through selenium)
- Scraps the home page of Google news.
- Then collects the url for trendings page (through url id)
- Then it scraps that page too.
- All scraped data are made into a pandas df.
- Then this pandas df is stored into the postgres Database.

## gnews_scraper_cron.sh
- This is the file that calls main.py and creates logfile.
- And this is supposed to be ***scheduled as the cron job***. 


## "config.ini" file
- contains the base url link. ("https://news.google.com")
- also contains the database connection information. (Give your postgres DB connection details here).

## To run 
- execute only the "gnews_scraper_cron.sh" file. (it will redirect stdout & stderr to log file.)

