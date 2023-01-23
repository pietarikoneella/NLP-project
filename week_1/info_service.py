from urllib import request
from bs4 import BeautifulSoup
import re
import requests


def main():

    # The news part

    url_news = "https://yle.fi/uutiset"
    html_news = request.urlopen(url_news).read().decode('utf8')
    

    # The news page displays ten short news in a feed. They can be "caught" as h3. 
    # However, there are other feeds on the page as well and their content also seems to be h3
    # so to skip scraping them as well, the auxiliary variable i helps catch the ones wanted.

    list_of_headlines = []
    i = 0
    for tags in BeautifulSoup(html_news, "html.parser").find_all("h3"):
        if i == 10:
            break
        list_of_headlines.append(tags.text.strip())
        i += 1


    # This finds the time the piece of news was first created

    list_of_creation_time_tuples = []

    for item in re.findall(r'\"settings\":{},\"createdAt\":"(\d\d\d\d\-\d\d\-\d\d)T(\d\d:\d\d:\d\d)', html_news):   
        list_of_creation_time_tuples.append(item)


    # This finds the time the piece of news was last updated

    list_of_update_time_tuples = []

    for item in re.findall(r'hideAuthor":[truefals]+,\"updatedAt\":"(\d\d\d\d\-\d\d\-\d\d)T(\d\d\:\d\d\:\d\d)', html_news):
        list_of_update_time_tuples.append(item)

    
    # The weather part
    
    url_temps = "https://weather.com/fi-FI/weather/today/l/60.18,24.93"
    html_temps = request.urlopen(url_temps).read().decode('utf8')
    soup = BeautifulSoup(html_temps, 'html.parser')

    now_list = re.findall(r"CurrentConditions--tempValue--MHmYY\">(-?\+?\d+°)</span>", html_temps)
    now_t = now_list[0]

    morning_list =  re.findall(r"Aamuna</span></h3><div data-testid=\"SegmentHighTemp\" class=\"Column--temp--1sO_J\"><span data-testid=\"TemperatureValue\">(-?\d+°)", html_temps)
    morning_t = morning_list[0]
    
    afternoon_list = re.findall(r"Iltapäivä</span></h3><div data-testid=\"SegmentHighTemp\" class=\"Column--temp--1sO_J\"><span data-testid=\"TemperatureValue\">(-?\d+°)", html_temps)
    afternoon_t = afternoon_list[0]
    
    evening_list = re.findall(r"Ilta</span></h3><div data-testid=\"SegmentHighTemp\" class=\"Column--temp--1sO_J\"><span data-testid=\"TemperatureValue\">(-?\d+°)", html_temps)
    evening_t = evening_list[0]
    
    overnight_list =  re.findall(r"Yö</span></h3><div data-testid=\"SegmentHighTemp\" class=\"Column--temp--1sO_J\"><span data-testid=\"TemperatureValue\">(-?\d+°)", html_temps)
    overnight_t = overnight_list[0]


    # The user interface

    print()
    print("*** Weather and news update service ***")
    
    task = "*"

    while task != "":
        print()
        print("Pleace choose the information you need!")
        print("1 - Weather now in Helsinki")
        print("2 - Today's weather in Helsinki")
        print("3 - 10 latest short news headlines on yle.fi/uutiset")
        print()
        task = input("Choose the info you need! (Write a number): ")

        if task == "1":
            print()
            print("  Current temperature in Helsinki:")
            print("  "+ "-"*32)
            print(" ", now_t)
    
        elif task == "2":
            print()
            print("  Helsinki: today's temperature estimates:")
            print("  " + "-"*39)
            print("  Morning:", morning_t)
            print("  Afternoon:", afternoon_t)
            print("  Evening:", evening_t)
            print("  Overnigt:", overnight_t)

        elif task == "3":
            # Printing out the headlines and creation times
            print()
            print("  Ten latest short news headlines on yle.fi/uutiset")
            print(" ", "-"*50)
            for i in range(10):
                print(" ", list_of_headlines[i])
                print("      Created:", list_of_creation_time_tuples[i][0], "at", list_of_creation_time_tuples[i][1], end="")
                print(", latest update:", list_of_update_time_tuples[i][0], "at", list_of_update_time_tuples[i][1])
                print()


        elif task == "":
            print()
            print("Goodbye! Thank you for using our service!")
            print()

        else:
            print ()
            print("Please, write 1, 2 or 3.")
            
        
main()
