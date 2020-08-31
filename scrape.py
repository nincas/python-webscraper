from src.Binance import Binance
import time
import os
from sys import exit

PATH = "src/bin/chromedriver"
if os.name == 'nt':
    PATH = "src/bin/chromedriver.exe"

# Binance - Pattern
binance = Binance()
binance.scrapeBinance(PATH)