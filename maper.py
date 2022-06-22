from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import time
import asyncio
import random 
import os

PATH = r'driver\chromedriver.exe'
MAPS_URL = "https://www.google.com/maps/"
CLASS_STYLE = "hfpxzc"

chrome_options = webdriver.ChromeOptions()
# for deployment
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-java")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")


class Resturant:
    def __init__(self , driver = None , url = None):
        #set the driver
        self.url = url
        if not driver:
            # self.driver = webdriver.Chrome(PATH, chrome_options=chrome_options)
            self.driver = webdriver.Chrome(executable_path=os.environ.get(
                "CHROMEDRIVER_PATH"), chrome_options=chrome_options)
            #open the url
            self.driver.get(url)
            self.driver.maximize_window()
        else:
            self.driver = driver
            self.driver.get(url)
        #wait for the page to load
        wait = WebDriverWait(self.driver, 10)
        wait.until(EC.visibility_of_element_located((By.TAG_NAME, "canvas")))
        time.sleep(2)

    @property
    def name(self):
        return self.driver.find_elements_by_tag_name("h1")[0].get_attribute("innerText")


    @property
    def get_contact(self):
        contacts = self.driver.find_elements_by_class_name("Io6YTe")
        return {
            "address" : contacts[0].get_attribute("innerText"),
            "phone" : contacts[1].get_attribute("innerText"),
        }

    @property
    def position(self):
        url = self.driver.current_url
        # the link is under this form : https://blabla/bla/bla/@{lat},{lng},{zoom}/data=blabla
        # print("----->",url)
        url = url.split("@")[1]
        # print("------------------>" , url)
        lat , lng = url.split(",")[0:2]
        # print("aaaaaaaaaa")
        # print(lat , lng)
        return lat , lng

    @property
    def get_info(self):
        return {
            "name" : self.name or "",
            "contact" : self.get_contact or None,
            "position" : self.position or None,
        }


def get_resturants_by_query_and_city(qurey = "pizza" , city = "sidi bouzid") :
    driver = webdriver.Chrome(PATH, chrome_options=chrome_options)
    driver = webdriver.Chrome(executable_path=os.environ.get(
        "CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    # maximize the window
    driver.maximize_window()
    driver.get(MAPS_URL)
    # wait for the page to load
    wait = WebDriverWait(driver, 30)
    search_box = wait.until(EC.visibility_of_element_located((By.ID, "searchboxinput")))

    final_qurey = f"{qurey.replace(' ','+')}+{city.replace(' ','+')}" #setting the final url and changing all spaces with +

    search_box.send_keys(final_qurey)
    search_box.send_keys(Keys.ENTER)

    link_holders = wait.until(EC.visibility_of_all_elements_located((By.CLASS_NAME, CLASS_STYLE)))

    if not link_holders:
        # print("No results found")
        return None

    links = [link.get_attribute('href') for link in link_holders[0:4]]

    return links , driver


def get_resturant_info_by_link(link , driver=None):
    try : 
        if not link:
            return None
        resturant = Resturant(driver , link)
        return resturant.get_info
    except Exception as e:
        # print(e)
        return None



def get_api_response(qurey , city):
    start_time = time.time()
    links , driver = get_resturants_by_query_and_city(qurey , city)
    if not links:
        return None
    
    response = [get_resturant_info_by_link(link, driver) for link in links]
    #delete the none items
    response = [item for item in response if item]
    driver.quit()
    print(f"----{time.time() - start} s----")
    return response



if __name__ == "__main__":
    start = time.time()
    res = get_api_response("pizza" , "sidi bouzid")
    print(len(res) , [item["name"] for item in res])
    print(f"{time.time() - start} s")


