import requests
from bs4 import BeautifulSoup
from beepy import beep
import math
import threading


class PriceAlarm:
    target = 10000000
    alarm = 1
    currency = "bitcoin"
    should_check = True
    should_beep = True
    alarm_list = {1: 'coin', 2: 'robot_error', 3: 'error',
                  4: 'ping', 5: 'ready', 6: 'success', 7: 'wilhelm'}

    def choose_alarm(self):
        try:
            print("Choose an alarm sound!\nOptions:")
            for index in self.alarm_list:
                print(f"\t{index}: {self.alarm_list[index]}")
            sound = input()
            if 1 <= int(sound) <= 7:
                self.alarm = int(sound)
            else:
                raise Exception()
        except:
            print("Give me a number from 1 to 7 you dumb ass!")

    def get_price(self):
        try:
            URL = "https://coinmarketcap.com/currencies/" + self.currency.lower() + "/"
            page = requests.get(URL)
            soup = BeautifulSoup(page.content, 'html.parser')

            result = soup.find(id='__next')
            price = result.find(class_="priceValue___11gHJ")
            price = price.text.strip()
            price = self.format_prices(price)
            return price
        except:
            self.currency = "bitcoin"
            print("This is not a valid currency!")
            return -1
        
    def print_currency(self):
        print("The currency you are watching is: " + str(self.currency))

    def play_sound(self):
        if self.should_beep:
            beep(sound=self.alarm)

    def format_prices(self, price):
        price = price.replace('$', '')
        price = price.replace(',','')
        return float(price)

    def handle_user_input(self):
        target = input("Set the target price please!\n")
        try:
            if target == "!p" or target == "!price":
                print(f"Current price of {self.currency.capitalize()} is: {self.get_price()}")

            elif target == "!a" or target == "!alarm":
                self.should_beep = not self.should_beep
                if self.should_beep:
                    print(f"alarm sound is on! ({self.alarm_list[self.alarm]})")
                else:
                    print("alarm sound is off!")

            elif target == "!s" or target == "!sound":
                self.choose_alarm()

            elif "!c" in target or "!currency" in target:
                target = target.replace('!currency ', '')
                target = target.replace('!c ', '')
                self.currency = target


            elif target == "!h" or target == "!help":
                print("\tTo check the current price, type !p or !price")
                print("\tTo change the currency, type !c or !currency, then type the currency's name")
                print("\tTo turn on/off the alarm, type !a or !alarm")
                print("\tTo change the alarm sound, type !s or !sound")
                print("\tTo close the program, type !e or !exit\n")

            elif target == "!e" or target == "!exit":
                self.should_check = False
                print("Exiting...")

            elif (type(target) == str and type(self.format_prices(target)) == float) or type(target) == float and self.should_check == True:
                self.target = self.format_prices(target)
            else:
                print(type(target))
        except:
            print("Give me a normal target you dumb ass!")

    def check_price(self):
        if float(self.get_price()) >= float(self.target):
            self.play_sound()

    def check_loop(self):
        while self.should_check:
            self.check_price()


pa = PriceAlarm()
func = threading.Thread(target=pa.check_loop)
func.start()

while pa.should_check:
    pa.handle_user_input()
