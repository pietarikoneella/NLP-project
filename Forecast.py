from urllib import request
from bs4 import BeautifulSoup
import re
import requests
def main():
    
    url = "https://weather.com/fi-FI/weather/today/l/60.18,24.93"
    html = request.urlopen(url).read().decode('utf8')
    soup = BeautifulSoup(html, 'html.parser')
    print("Weather in Helsinki, Finland")
    print()

    now_list = re.findall(r"CurrentConditions--tempValue--MHmYY\">(-?\+?\d+°)</span>", html)
    now_t = now_list[0]

    morning_list =  re.findall(r"Aamuna</span></h3><div data-testid=\"SegmentHighTemp\" class=\"Column--temp--1sO_J\"><span data-testid=\"TemperatureValue\">(-?\d+°)", html)
    morning_t = morning_list[0]
    
    afternoon_list = re.findall(r"Iltapäivä</span></h3><div data-testid=\"SegmentHighTemp\" class=\"Column--temp--1sO_J\"><span data-testid=\"TemperatureValue\">(-?\d+°)", html)
    afternoon_t = afternoon_list[0]
    
    evening_list = re.findall(r"Ilta</span></h3><div data-testid=\"SegmentHighTemp\" class=\"Column--temp--1sO_J\"><span data-testid=\"TemperatureValue\">(-?\d+°)", html)
    evening_t = evening_list[0]
    
    overnight_list =  re.findall(r"Yö</span></h3><div data-testid=\"SegmentHighTemp\" class=\"Column--temp--1sO_J\"><span data-testid=\"TemperatureValue\">(-?\d+°)", html)
    overnight_t = overnight_list[0]
    

    print()
    print("1. Weather now")
    print("2. Weather for today")
    
    task = "*"
    while task != "":
        print()
        task = input("What do you want to know? (Write a number): ")

        if task == "1":
            print()
            print("Temperature now:",  now_t)
    
        elif task == "2":
            print()
            print("Temperature for today.")
            print("----------------------")
            print("Morning:", morning_t)
            print("Afternoon:", afternoon_t)
            print("Evening:", evening_t)
            print("Overnigt:", overnight_t)

        elif task == "":
            print("Bye!")
            break

        else:
            print ()
            print("Please, write 1 or 2.")
            
        
main()

    
    
