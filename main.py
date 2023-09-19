import requests
from bs4 import BeautifulSoup
import json
import re
import os
import logging


PATTERN = r'-\s*([^,]+)'
URL = "https://helpforenglish.cz"


def create_dictionary_of_url_links(*args: str) -> dict:
    """Connects to the webpage, scrapes its content, 
    and returns a dictionary of URL links."""
    try:
        response = requests.get(url=f"{URL}/dictionary/")
        soup = BeautifulSoup(response.content, "html.parser")
        url_links = {
            searched_a.text: URL+searched_a["href"]
            for element in args
            for searched_div in soup.find_all("div", class_=element)
            for searched_a in searched_div.find_all("a")
        }
        return url_links
    except Exception as e:
        logging.error(f"Failed to create dictionary of URL links: {str(e)}")
        return {}


def save_as_json_file(input_data: dict, filename: str):
    """Saves input data as a JSON file."""
    try:
        json_object = json.dumps(input_data, indent=4)
        with open(filename, "w", encoding="utf-8") as file:
            file.write(json_object)
    except Exception as e:
        logging.error(f"Failed to save JSON file: {str(e)}")


def scrape_vocabulary(url) -> list:
    """Scrapes vocabulary from a given URL."""
    try:
        vocabulary = []
        response = requests.get(url)
        soup = BeautifulSoup(response.content, "html.parser")
        my_div = soup.find_all("div", class_="col col-9 span8 word-card-info")
        for element in my_div:
            eng_word = element.find("strong").text
            if element.find("span", class_="tooltiptext"):
                one_or_more_cz_words = element.find(
                    "span").next_sibling.strip()
                one_word = re.search(PATTERN, one_or_more_cz_words).group(1)
                vocabulary.append(
                    {"czech": one_word, "english": eng_word})
            else:
                one_or_more_cz_words = element.find(
                    "strong").next_sibling.strip()
                one_word = re.search(PATTERN, one_or_more_cz_words).group(1)
                vocabulary.append(
                    {"czech": one_word, "english": eng_word})
        return vocabulary
    except Exception as e:
        logging.error(f"Failed to scrape vocabulary from {url}: {str(e)}")
        return []


def make_directory(directory_name: str):
    """Creates new directory."""
    os.makedirs(directory_name, exist_ok=True)


def main():
    logging.basicConfig(filename="scraper.log",
                        level=logging.ERROR, filemode="w")
    dictionary_links = create_dictionary_of_url_links("sloupec", "cloupec")
    save_as_json_file(dictionary_links, "sections-url-links.json")
    make_directory("vocabulary")
    for key, value in dictionary_links.items():
        vocabulary = scrape_vocabulary(value)
        save_as_json_file(vocabulary, f"vocabulary/{key}.json")


if __name__ == "__main__":
    main()
