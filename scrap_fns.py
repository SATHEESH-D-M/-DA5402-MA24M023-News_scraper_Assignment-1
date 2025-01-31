"""
Summary:
    # This module contains only the helper functions to scrap the google news webpage for images and metadata.
    # The functions are used in the main module to scrap the google news webpage.

    # The functions are:
        - load_config                   (extra)
        - load_base_url                 (Part answer to Modules 1 & 2)
        - image_dimensions              (extra)
        - extract_image_and_metadata    (Part answer to Modules 1, 2 & 3)
        - get_url                       (Part answer to Module 2)
"""

import argparse
import configparser
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from datetime import datetime
import requests


def load_config(config_file: str) -> configparser.ConfigParser:
    """
    Loads configuration from an INI file and return the base URL.

    Args:
        config_file (str)      : Path to the configuration file.
        fallback_url (str)     : URL to use if no URL is found in the configuration file.

    Returns:
        configparser.ConfigParser: the configparser object.
    """

    config = configparser.ConfigParser()
    config.read(config_file)

    return config


def load_base_url(config_file_name: str) -> str:
    """
    Summary:
        # loads the webpage url from the config file or through the command line

    Args:
        config_file_name (str): The name of the config file.

    Returns:
        str: _description_
    """

    # Parse command-line arguments
    parser = argparse.ArgumentParser(
        description="Load the google news home webpage url."
    )
    parser.add_argument(
        "--url",
        type=str,
        help="The base_url to load. If not provided, the url is loaded from the config file.",
    )
    args, unknown = parser.parse_known_args()  # Ignore extra arguments from Jupyter

    # load the config file
    config = configparser.ConfigParser()
    config.read(config_file_name)

    # get the base_url
    url = args.url if args.url else config["DEFAULT"]["base_url"]

    return url


def image_dimensions(image_info: str) -> tuple:
    """
    Summary:
        # Gets the dimensions of an image.

    Args:
        image_data (str): The image data.

    Returns:
        tuple: The dimensions of the image.
    """
    height = int(image_info.split(":")[-2].strip(" px;height"))
    width = int(image_info.split(":")[-1].strip(" px;"))
    return height, width


def extract_image_and_metadata(
    driver: object,
    element_class_name: str,
    article_class_name: str,
    thumbnail_class_name: str,
    article_class_url: str,
    article_class_time: str,
    news_data: list,
) -> None:
    """
    Summary:
        # scraps the image_data and the associated metadata from the google news page html.
        # Appends the scrapped data to the news_data list.
        # metadata includes
            - headlines,
            - image_url,
            - image_height,
            - image_width,
            - article_url, (of the published article in the news)
            - scrap_timestamp,
            - published_time (relative to scrape_timestamp)

    Args:
        driver (object)             : The selenium webdriver object.
        element_class_name (str)    : The class name of the element containing all the info reqired.
        article_class_name (str)    : The class name of the element containing the articles.
        thumbnail_class_name (str)  : The class name of the element containing the thumbnail.
        article_class_url (str)     : The class name of the element containing the article url.
        article_class_time (str)    : The class name of the element containing the published time.
        news_data (list)            : The list to store the scrapped data.

    Returns: None
    """
    # extract relevant blocks of elements that contain image data and associated metadata from the html and make a list
    articles = WebDriverWait(driver, 30).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, element_class_name))
    )

    # iterate over the list of articles and extract the image_data and metadata
    for article in articles:
        try:
            # extract the image data
            image_url = article.find_element(
                By.CSS_SELECTOR, thumbnail_class_name
            ).get_attribute("src")

            image_data = requests.get(image_url).content

            # extraxt the metadata
            headline = article.find_element(By.CSS_SELECTOR, article_class_name).text

            image_info = article.find_element(
                By.CSS_SELECTOR, thumbnail_class_name
            ).get_attribute("style")

            height, width = image_dimensions(image_info)
            article_url = article.find_element(
                By.CSS_SELECTOR, article_class_url
            ).get_attribute("href")

            scrap_timestamp = datetime.now()

            published_time = article.find_element(
                By.CSS_SELECTOR, article_class_time
            ).text

            # Append the data to the list
            news_data.append(
                {
                    "image_data": image_data,
                    "headlines": headline,
                    "image_url": image_url,
                    "image_height": height,
                    "image_width": width,
                    "article_url": article_url,
                    "scrap_timestamp": scrap_timestamp,
                    "published_time": published_time,
                }
            )

        except Exception as e:
            print(
                f"Error (Skipping this article instance): {str(e).split('Stacktrace:')[0].strip()}"
            )

    return None


def get_url(driver: object, url_ID: str) -> str:
    """
    Summary:
        # gets any url from the google news webpage html.

    Args:
        driver (object) : The selenium webdriver object.
        url_ID (str)    : The unique id to locate url from webpage html.

    Returns:
        str: The required url.
    """
    required_url = driver.find_element(By.ID, url_ID).get_attribute("href")

    return required_url
