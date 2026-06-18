from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.service import Service
import time


def search_myntra(query):

    service = Service(ChromeDriverManager().install())

    driver = webdriver.Chrome(service=service)

    driver.get("https://www.myntra.com")


    search_box = driver.find_element(
        By.CLASS_NAME,
        "desktop-searchBar"
    )

    search_box.send_keys(query)

    search_box.send_keys(Keys.ENTER)

    print("Myntra search opened successfully")

    return driver