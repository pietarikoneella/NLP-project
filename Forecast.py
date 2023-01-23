from urllib import request
from bs4 import BeautifulSoup
import re
import requests
def main():
    
    url = "https://weather.com/weather/today/l/6e297205c5199a0a119875bde5cb0f506e57e4ab869091b945e1f6f94b494bf1"
    html = request.urlopen(url).read().decode('utf8')
    soup = BeautifulSoup(html, 'html.parser')
    print("Weather in Helsinki, Finland")
    print()
    
    now_list = re.findall(r"<a class=\"Column--innerWrapper--3ocxD  Button--default--2gfm1\" href=\"/weather/hourbyhour/l/6e297205c5199a0a119875bde5cb0f506e57e4ab869091b945e1f6f94b494bf1\" target=\"_self\"><h3 class=\"Column--label--2s30x Column--default--2-Kpw\"><span class=\"Ellipsis--ellipsis--3ADai\" style=\"-webkit-line-clamp:2\">Now</span></h3><div data-testid=\"SegmentHighTemp\" class=\"Column--temp--1sO_J\"><span data-testid=\"TemperatureValue\">-?\d*°",html)
    now = " ".join(now_list)
    now_t = re.findall(r"-?\d*°", now)

    morning_list =  re.findall(r"<a class=\"Column--innerWrapper--3ocxD  Button--default--2gfm1\" href=\"/weather/hourbyhour/l/6e297205c5199a0a119875bde5cb0f506e57e4ab869091b945e1f6f94b494bf1\" target=\"_self\"><h3 class=\"Column--label--2s30x Column--default--2-Kpw\"><span class=\"Ellipsis--ellipsis--3ADai\" style=\"-webkit-line-clamp:2\">Morning</span></h3><div data-testid=\"SegmentHighTemp\" class=\"Column--temp--1sO_J\"><span data-testid=\"TemperatureValue\">-?\d*°",html)
    morning = " ".join(morning_list)
    morning_t = re.findall(r"-?\d*°", morning)
    
    afternoon_list = re.findall(r"<a class=\"Column--innerWrapper--3ocxD  Button--default--2gfm1\" href=\"/weather/hourbyhour/l/6e297205c5199a0a119875bde5cb0f506e57e4ab869091b945e1f6f94b494bf1\" target=\"_self\"><h3 class=\"Column--label--2s30x Column--default--2-Kpw\"><span class=\"Ellipsis--ellipsis--3ADai\" style=\"-webkit-line-clamp:2\">Afternoon</span></h3><div data-testid=\"SegmentHighTemp\" class=\"Column--temp--1sO_J\"><span data-testid=\"TemperatureValue\">?\d*°", html)
    afternoon = " ".join(afternoon_list)
    afternoon_t = re.findall(r"-?\d*°", afternoon)
    
    evening_list = re.findall(r"<a class=\"Column--innerWrapper--3ocxD  Button--default--2gfm1\" href=\"/weather/hourbyhour/l/6e297205c5199a0a119875bde5cb0f506e57e4ab869091b945e1f6f94b494bf1\" target=\"_self\"><h3 class=\"Column--label--2s30x Column--default--2-Kpw\"><span class=\"Ellipsis--ellipsis--3ADai\" style=\"-webkit-line-clamp:2\">Evening</span></h3><div data-testid=\"SegmentHighTemp\" class=\"Column--temp--1sO_J\"><span data-testid=\"TemperatureValue\">-?\d*°",html)
    evening = " ".join(evening_list)
    evening_t = re.findall(r"-?\d*°", evening)
    
    overnigt_list =  re.findall(r"<a class=\"Column--innerWrapper--3ocxD  Button--default--2gfm1\" href=\"/weather/hourbyhour/l/6e297205c5199a0a119875bde5cb0f506e57e4ab869091b945e1f6f94b494bf1\" target=\"_self\"><h3 class=\"Column--label--2s30x Column--default--2-Kpw\"><span class=\"Ellipsis--ellipsis--3ADai\" style=\"-webkit-line-clamp:2\">Overnight</span></h3><div data-testid=\"SegmentHighTemp\" class=\"Column--temp--1sO_J\"><span data-testid=\"TemperatureValue\">-?\d*°",html)
    overnigt = " ".join(overnigt_list)
    overnigt_t = re.findall(r"-?\d*°", overnigt)
    
    print("1. Weather now")
    print("2. Weather for today")
    
    task = "*"
    while task != "":
        print()
        task = input("What do you want to know? (Write a number): ")

        if task == "1":
            print()
            print("Temperature now: "+ " ".join(now_t))

        elif task == "2":
            print()
            print("Temperature for today.")
            print("----------------------")
            print("Morning: "+ " ".join(morning_t))
            print("Afternoon: "+ " ".join(afternoon_t))
            print("Evening: "+ " ".join(evening_t))
            print("Overnigt: "+ " ".join(overnigt_t))

        elif task == "":
            print("Bye!")
            break

        else:
            print ()
            print("Please, write 1 or 2.")
            

        
main()

    
    
