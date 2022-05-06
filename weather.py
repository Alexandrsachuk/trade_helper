from colorama import init
init()
from colorama import Fore, Back, Style
import pyowm
from pyowm.owm import OWM
from pyowm.utils.config import get_default_config
config_dict = get_default_config()
config_dict['language'] = 'ru'
owm = OWM('53c6f9985a6bdd981fd13f433a212a41', config_dict)
mgr = owm.weather_manager()

print(Fore.BLACK)
print(Back.GREEN)

place = input("Где вы сейчас? ")
observation = mgr.weather_at_place(place)
w = observation.weather
temp = w.temperature("celsius")["temp"]

print("В городе: " + place + " сейчас " + w.detailed_status + " и температура " + str(temp) + "C")


if temp <= -20:
    print(Back.BLUE)
    print("На улице пиздец, сиди дома")
elif temp <= -10:
    print(Back.CYAN)
    print("На улице холодэо")
elif temp <= 0:
    print(Back.WHITE)
    print("На улице замерзэо")
elif temp <= 10:
    print(Back.GREEN)
    print("Штаны в носки и заебись")
elif temp >= 10:
    print(Back.RED)
    print("Самое то, по району летать")
input()