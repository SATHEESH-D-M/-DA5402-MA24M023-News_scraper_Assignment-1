"""
Summary:
    # This is the main orchestration script (Answer to module 6).
    # Requirements:
        - scrap_fns.py
        - postgresdb_fns.py
commands:
    "python3 main.py --url https://news.google.co.uk" --> to run the script with the specified url.
    "python3 main.py" --> to run the script with the url from the config file.

"""

# import helper modules
from scrap_fns import *
from postgresdb_fns import *

# import libraries
import pandas as pd
from selenium import webdriver
import time

# Headless mode settings to run the website in background
from selenium.webdriver.chrome.options import Options

options = Options()
options.add_argument("--headless")  # Enable headless mode
options.add_argument("--disable-gpu")  # Optional: Fixes some headless issues

# get the base_url
url = load_base_url("config.ini")
print(url)

# load the webpage
driver = webdriver.Chrome(options=options)
driver.get(url)
time.sleep(3)

# Initialize an empty list to store the scrapped data
news_data = []


"""
    # Start scraping homepage for the image_data and metadata
        - The repeated calls of the function extract_image_and_metadata is to account for the different layout of the webpage.
        - Change the arguments of the function and call multiple times to match the layout of the webpage to scrap.
"""
extract_image_and_metadata(
    driver=driver,
    element_class_name=".IBr9hb",
    article_class_name=".gPFEn",
    thumbnail_class_name=".Quavad.vwBmvb",
    article_class_url=".WwrzSb",
    article_class_time=".hvbAAd",
    news_data=news_data,
)

extract_image_and_metadata(
    driver=driver,
    element_class_name=".IFHyqb",
    article_class_name=".JtKRv",
    thumbnail_class_name=".Quavad.vwBmvb",
    article_class_url=".WwrzSb",
    article_class_time=".hvbAAd",
    news_data=news_data,
)

# Get the top stories url
top_stories_url = get_url(
    driver=driver, url_ID="i11"
)  # Check if the argument "url_ID" is up-to-date

# Load the top stories page
driver.get(top_stories_url)
time.sleep(3)

"""
    # Start scraping top-stories page for the image_data and metadata
        - The repeated calls of the function extract_image_and_metadata is to account for the different layout of the webpage.
        - Change the arguments of the function and call multiple times to match the layout of the webpage to scrap.
"""
extract_image_and_metadata(
    driver=driver,
    element_class_name=".IBr9hb",
    article_class_name=".gPFEn",
    thumbnail_class_name=".Quavad.vwBmvb",
    article_class_url=".WwrzSb",
    article_class_time=".hvbAAd",
    news_data=news_data,
)


# close the driver
# input("Press Enter to close the browser...")
driver.quit()

# convert to pandas dataframe
df = pd.DataFrame(news_data)

# push the data to the database
config = load_config("config.ini")
insert_data_into_DB(config, df)
