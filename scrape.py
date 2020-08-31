from src.Binance import Binance
from src.Blockchain import Blockchain
import time
import os
from sys import exit, argv

validArgs = ['binance', 'blockchain']

if argv[1] not in validArgs:
    print(argv[1], " not a valid source.")
    exit(0)

PATH = "src/bin/chromedriver"
if os.name == 'nt':
    PATH = "src/bin/chromedriver.exe"

print("Starting getting", argv[1], "btc value.")

if argv[1] == 'binance':
    # Binance - Pattern
    binance = Binance("https://www.binance.com/en/trade/BTC_USDT")
    binance.scrape(PATH)

if argv[1] == 'blockchain':
    # Blockchain - Pattern
    blockChain = Blockchain("https://exchange.blockchain.com/trade")
    blockChain.scrape(PATH)
