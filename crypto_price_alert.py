import requests
from bs4 import BeautifulSoup
import os
import sys
from re import sub
from decimal import Decimal
import math
import threading
import platform
from beepy import beep
import simpleaudio


class PriceAlert:
    target = 10000000
    should_check = True

    def get_price(self):
        URL = "https://coinmarketcap.com/currencies/ethereum/"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')

        result = soup.find(id='__next')
        price = result.find(class_ = "priceValue___11gHJ")
        price = price.text.strip()
        price = self.format_prices(price)
        return price

    def play_sound(self):
        beep(sound=1)
        #alert_text = "Ethereum price is over {}".format(self.target)
        #if platform.system() == "Darwin" or platform.system() == "Linux":
        #    os.system('say {}'.format(alert_text))
        #elif platform.system() == "Windows":
        #    import winsound
        #    duration = 100
        #    freq = 5000
        #    winsound.Beep(freq, duration)

    def format_prices(self, price):
        price = Decimal(sub(r'[^\d.]', '', price))
        price = math.trunc(price)
        return price

    def set_target(self):
        target = input("Set the target price please!\n")
        try:
            if target == "!p" or target == "!price":
                print("Current price is: {}".format(self.get_price()))
            elif target == "!e" or target == "!exit":
                self.should_check = False
                print("Exiting...")
            elif (type(target) == str and type(self.format_prices(target)) == int) or type(target) == int and self.should_check == True:
                self.target = self.format_prices(target)
        except:
            print("Give me a normal target you dumb ass!")

    def check_price(self):
        if self.get_price() >= self.target:
            self.play_sound()

    def check_loop(self):
        while self.should_check:
            self.check_price()

pa = PriceAlert()
func = threading.Thread(target=pa.check_loop)
func.start()

while pa.should_check:
    pa.set_target()