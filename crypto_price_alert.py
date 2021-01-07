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


class PriceAlarm:
    target = 10000000
    alarm = 1
    should_check = True
    should_beep = True
    alarm_list = {1: 'coin', 2: 'robot_error', 3: 'error',
                  4: 'ping', 5: 'ready', 6: 'success', 7: 'wilhelm'}

    def choose_alarm(self):
        try:
            print("Choose an alarm sound!\nOptions:")
            for index in self.alarm_list:
                print("\t{}: {}".format(index, self.alarm_list[index]))
            sound = input()
            if 1 <= int(sound) <= 7:
                self.alarm = int(sound)
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

    def handle_user_input(self):
        target = input("Set the target price please!\n")
        try:
            if target == "!p" or target == "!price":
                print("Current price is: {}".format(self.get_price()))

            elif target == "!a" or target == "!alarm":
                self.should_beep = not self.should_beep
                if self.should_beep:
                    print("alarm sound is on! ({})".format(
                        self.alarm_list[self.alarm]))
                else:
                    print("alarm sound is off!")

            elif target == "!s" or target == "!sound":
                self.choose_alarm()

            elif target == "!h" or target == "!help":
                print("To check the current price, type !p or !price")
                print("To turn on/off the alarm, type !a or !alarm")
                print("To change the alarm sound, type !s or !sound")
                print("To close the program, type !e or !exit")

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


pa = PriceAlarm()
func = threading.Thread(target=pa.check_loop)
func.start()

while pa.should_check:
    pa.handle_user_input()
