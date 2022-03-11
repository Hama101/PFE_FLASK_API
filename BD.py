from selenium import webdriver
import random
import json
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
import os

PATH = r'driver\chromedriver.exe'
chrome_options = webdriver.ChromeOptions()
# for deployment
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-java")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")


class Recipe:
    def __init__(self, url):
        # self.driver = webdriver.Chrome(PATH, chrome_options=chrome_options)
        self.driver = webdriver.Chrome(executable_path=os.environ.get(
            "CHROMEDRIVER_PATH"), chrome_options=chrome_options)
        self.url = url
        self.driver.get(url)

    def get_name(self):
        return self.driver.find_element_by_class_name('headline').get_attribute('innerHTML')

    def get_rating(self):
        return self.driver.find_element_by_class_name('ugc-ratings-item').get_attribute('innerHTML')

    def get_images(self):
        images = self.driver.find_elements_by_class_name('image-loaded')
        urls = [url.get_attribute('data-src') for url in images]
        # remove all the images ending with .png from the urls
        urls = [url for url in urls if not url.endswith('.png')]
        # remove all duplicate urls
        return list(set(urls))

    def get_ingredients(self):
        list_of_ingredients = [x.get_attribute(
            'innerHTML') for x in self.driver.find_elements_by_class_name('ingredients-item-name')]
        final = [item.replace('\u00bd', '1/2') for item in list_of_ingredients]
        return final

    def get_instructions(self):
        return [x.find_element_by_tag_name('p').get_attribute('innerHTML') for x in self.driver.find_elements_by_class_name('paragraph')]

    def get_time(self):
        return self.driver.find_element_by_class_name('recipe-meta-item-body').get_attribute('innerHTML')

    def get_data(self):
        data = {
            'name': self.get_name(),
            'rating': self.get_rating(),
            'images': self.get_images(),
            'ingredients': self.get_ingredients(),
            'instructions': self.get_instructions(),
            'time': self.get_time(),
            'vedios': []
        }
        # save the data to a json file using the json module
        # name = data['name']
        # with open(f'BD/{name}.json', 'w') as outfile:
        #     json.dump(data, outfile , indent=4)

        return data


class Card:
    def __init__(self, driver, element):
        self.driver = driver
        self.element = element
        actions = ActionChains(self.driver)
        actions.move_to_element(self.element).perform()

    def get_url(self):
        return self.element.find_elements_by_tag_name('a')[0].get_attribute('href')

    def get_thumbnail(self):
        return self.element.find_elements_by_tag_name('img')[0].get_attribute('src')

    def get_title(self):
        return self.element.find_elements_by_tag_name('img')[0].get_attribute('title')

    def get_ratings(self):
        return self.element.find_element_by_class_name('ratings-count').get_attribute('innerHTML')

    def get_data(self):
        return {
            'url': self.get_url(),
            'thumbnail': self.get_thumbnail(),
            'title': self.get_title(),
            'rating': f"{self.get_ratings()}".replace(' ', '')
        }


# this will show the first 6 repices for a given topic
def get_list_by_topic(topic="Pizza"):
    #driver = webdriver.Chrome(PATH, chrome_options=chrome_options)
    driver = webdriver.Chrome(executable_path=os.environ.get(
        "CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    # maximize the window
    driver.maximize_window()
    class_name = "card"
    driver.get(f'https://www.allrecipes.com/search/results/?search={topic}')

    element = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((By.CLASS_NAME, class_name))
    )
    # scrolling down the page
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    cards = driver.find_elements_by_class_name(class_name)[0:10]
    list_of_cards = [Card(driver, card) for card in cards]
    data = [card.get_data() for card in list_of_cards]
    # remove all the card with no title
    data = [x for x in data if x['title'] != '']
    driver.close()
    return data


# this function will return a random image for a given topic
def get_image(driver, topic):
    class_name = "card"
    driver.get(f'https://www.allrecipes.com/search/results/?search={topic}')

    element = WebDriverWait(driver, 30).until(
        EC.presence_of_element_located((By.CLASS_NAME, class_name))
    )
    cards = driver.find_elements_by_class_name(class_name)[0:6]
    # select a random card
    random_card = random.choice(cards)
    card = Card(driver, random_card)
    driver.close()
    return card.get_thumbnail()


if __name__ == '__main__':
    get_list_by_topic()
    driver.quit()
