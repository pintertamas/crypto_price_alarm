import requests
from bs4 import BeautifulSoup
from beepy import beep
import simpleaudio
import os
import sys
from re import sub
from decimal import Decimal
import math
import threading
import platform


class PriceAlert:
    target = 10000000
    alarm = 1
    should_check = True
    should_beep = True

    def choose_alarm(self):
        try:
            sound = input("Choose an alarm sound!\n\tOptions:\n\t1 : 'coin'\n\t2 : 'robot_error'\n\t3 : 'error'\n\t4 : 'ping'\n\t5 : 'ready'\n\t6 : 'success'\n\t7 : 'wilhelm'\n\n")
            if 1 <= int(sound) <= 7:
                self.alarm = sound
            else:
                raise Exception()
        except:
            print("Give me a number from 1 to 7 you dumb ass!")

    def get_price(self):
        URL = "https://coinmarketcap.com/currencies/ethereum/"
        page = requests.get(URL)
        soup = BeautifulSoup(page.content, 'html.parser')

        result = soup.find(id='__next')
        price = result.find(class_="priceValue___11gHJ")
        price = price.text.strip()
        price = self.format_prices(price)
        return price

    def play_sound(self):
        if self.should_beep:
            beep(sound=self.alarm)

    def format_prices(self, price):
        price = Decimal(sub(r'[^\d.]', '', price))
        price = math.trunc(price)
        return price

    def set_target(self):
        target = input("Set the target price please!\n")
        try:
            if target == "!p" or target == "!price":
                print("Current price is: {}".format(self.get_price()))
            elif target == "!b" or target == "!beep":
                self.should_beep = not self.should_beep
                if self.should_beep:
                    print("Alert sound is on!")
                else:
                    print("Alert sound is off!")
            elif target == "!a" or target == "!alarm":
                self.choose_alarm()
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
pa.choose_alarm()
func = threading.Thread(target=pa.check_loop)
func.start()

while pa.should_check:
    pa.set_target()
