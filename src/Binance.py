from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common import exceptions 
from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
import os
import sys

class Binance:
    src = "https://www.binance.com/en/trade/BTC_USDT"
    lastPrice = 0

    def scrapeBinance(self, file):
        PATH = os.path.abspath(file)

        # Set browser
        browser = webdriver.Chrome(PATH)

        # Load the page
        browser.get(self.src)
        browser.implicitly_wait(5)

        while True:
            try:
                # Wait until the element appear on the src page.
                main = WebDriverWait(browser, 5).until(
                    EC.presence_of_element_located((By.CLASS_NAME, "list-auto-sizer"))
                )
                
                values = main.find_elements_by_class_name("List_list-item-container__oHFzZ")
                for value in values:
                    prices = value.find_elements_by_class_name("List_list-item-entity__1f-x_")
                    for price in prices:
                        priceItem = price.find_element_by_class_name("price")
                        indicator = "-" if float(self.lastPrice) > float(priceItem.text.replace(",", "")) else "+"
                        self.lastPrice = float(priceItem.text.replace(",", ""))

                        print(indicator, "$" + self.lastPrice)

            except:
                print("Oops!", sys.exc_info()[0], "occurred.")
