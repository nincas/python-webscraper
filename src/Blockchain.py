from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common import exceptions 
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from .components.RedisClient import RedisClient
import os
import sys
import json

class Blockchain:
    src = ""
    lastPrice = 0.0

    def __init__(self, srcUrl):
        self.src = srcUrl

    def scrape(self, file):
        PATH = os.path.abspath(file)

        # Set browser
        chrome_options = Options()
        chrome_options.add_argument('--headless')
        chrome_options.add_argument('--no-sandbox')
        browser = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)

        # Load the page
        browser.get(self.src)
        browser.implicitly_wait(10)
        r = RedisClient()

        while True:
            try:
                # Wait until the element appear on the src page.
                price = WebDriverWait(browser, 10).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "kpvYqK"))
                )
                
                # price = main.find_element_by_class_name("kpvYqK")
                indicator = "-" if float(self.lastPrice) > float(price.text.replace(",", "")) else "+"
                self.lastPrice = price.text.replace(",", "")

                print(indicator, "$" + self.lastPrice)
                r.publishValue('btc-value-blockchain', json.dumps({
                    "source": self.src,
                    "indicator": indicator,
                    "value": float(self.lastPrice)
                }))

            except:
                print("Oops!", sys.exc_info()[0], "occurred.")
