import requests
from bs4 import BeautifulSoup
from beepy import beep
import threading


def print_help():
    print("\tTo set a target price, just type it!")
    print("\tTo check the current price, type !p or !price")
    print("\tTo change the currency, type !c or !currency, then type the currency's name")
    print("\tTo turn on/off the alarm, type !a or !alarm")
    print("\tTo change the alarm sound, type !s or !sound")
    print("\tTo close the program, type !e or !exit")


def format_prices(price):
    price = price.replace('$', '')
    price = price.replace(',', '')
    return round(float(price), 2)


class PriceAlarm:
    target = -1
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
            price = format_prices(price)
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

    def print_price(self):
        print(
            f"Current price of {self.currency.capitalize()} is: {self.get_price()}. The target price is: {self.target}")

    def print_alarm(self):
        self.should_beep = not self.should_beep
        if self.should_beep:
            print(f"alarm sound is on! ({self.alarm_list[self.alarm]})")
        else:
            print("alarm sound is off!")

    def choose_currency(self, target):
        target = target.replace('!currency ', '')
        target = target.replace('!c ', '')
        self.currency = target

    def handle_user_input(self):
        target = input()
        try:
            if target == "!p" or target == "!price":
                self.print_price()

            elif target == "!a" or target == "!alarm":
                self.print_alarm()

            elif target == "!s" or target == "!sound":
                self.choose_alarm()

            elif "!c" in target or "!currency" in target:
                self.choose_currency(target)

            elif target == "!h" or target == "!help":
                print_help()

            elif target == "!e" or target == "!exit":
                self.should_check = False
                print("Exiting...")

            elif (type(target) is str and type(format_prices(target)) is float) or type(
                    target) is float and self.should_check is True:
                self.target = format_prices(target)
            else:
                print("There was an error. Try again!")
        except:
            print("Give me a valid input please!")

    def check_price(self):
        if float(self.get_price()) >= float(self.target):
            self.play_sound()

    def check_loop(self):
        while self.should_check:
            self.check_price()


pa = PriceAlarm()
pa.target = round(pa.get_price() * 1.1, 2)
print_help()
func = threading.Thread(target=pa.check_loop)
func.start()

while pa.should_check:
    pa.handle_user_input()
