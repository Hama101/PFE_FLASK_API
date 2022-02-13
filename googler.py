from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import os

PATH = r'driver\chromedriver.exe'
chrome_options = webdriver.ChromeOptions()
#for deployment
chrome_options.binary_location = os.environ.get("GOOGLE_CHROME_BIN")
chrome_options.add_argument("--incognito")
chrome_options.add_argument("--headless")
chrome_options.add_argument("--disable-extensions")
chrome_options.add_argument("--disable-java")
chrome_options.add_argument("--disable-dev-shm-usage")
chrome_options.add_argument("--no-sandbox")



def predict_image(img_path):
    #driver = webdriver.Chrome(PATH , chrome_options=chrome_options)
    driver = webdriver.Chrome(executable_path=os.environ.get("CHROMEDRIVER_PATH"), chrome_options=chrome_options)
    driver.get('https://storage.googleapis.com/tfhub-visualizers/visualizers/vision/index.html?modelMetadataUrl=https%3A%2F%2Fstorage.googleapis.com%2Ftfhub-visualizers%2Fgoogle%2Faiy%2Fvision%2Fclassifier%2Ffood_V1%2F1%2Fmetadata.json')
    img = os.getcwd()+f"/{img_path}"
    file = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.ID, "file"))
    )
    file.send_keys(img)
    l = WebDriverWait(driver, 60).until(
        EC.presence_of_element_located((By.CLASS_NAME, "tfhubVisualizerTemplatesClassifierResultDisplayName"))
    )
    labels = [item.get_attribute("innerHTML") for item in driver.find_elements_by_class_name('tfhubVisualizerTemplatesClassifierResultDisplayName')]
    percentage = [item.get_attribute("innerHTML") for item in driver.find_elements_by_class_name('tfhubVisualizerTemplatesClassifierResultScorePercent')]
    driver.quit()
    return labels[0:5], percentage[0:5]


if __name__ == "__main__":
    res = predict_image('000.jpg')
    print(res)