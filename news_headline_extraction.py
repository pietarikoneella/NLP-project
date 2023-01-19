
from urllib import request
from bs4 import BeautifulSoup
import re

def main():

    url = "https://yle.fi/uutiset"


    html = request.urlopen(url).read().decode('utf8')
    #raw = BeautifulSoup(html, 'html.parser').get_text()


    # The news page displays ten short news in a feed. They can be "caught" as h3. 
    # However, there are other feeds on the page as well and their content also seems to be h3
    # so to skip scraping them as well, the auxiliary variable i helps catch the ones wanted.

    list_of_headlines = []
    i = 0
    for tags in BeautifulSoup(html, "html.parser").find_all("h3"):
        if i == 10:
            break
        list_of_headlines.append(tags.text.strip())

        i += 1

    #########################
    # This is another, (pretty messy) regular expression, way to get the headlines

    #list_of_headlines = []

        #for item in re.findall(r'\"type\":\"h1\",\"text\":\"([a-öA-Ö0-9\s.,:\-\–\"!?]*)\"},{\"type\":\"paragraph\"', html):
            #list_of_headlines.append(item.strip())
    #########################

    print()

    print("Then short news stories from Yle Uutiset")

    # This finds the time the piece of news was first created

    list_of_creation_time_tuples = []

    for item in re.findall(r'\"settings\":{},\"createdAt\":"(\d\d\d\d\-\d\d\-\d\d)T(\d\d:\d\d:\d\d)', html):
        
        list_of_creation_time_tuples.append(item)

    print()

    # This finds the time the piece of news was last updated

    list_of_update_time_tuples = []

    for item in re.findall(r'hideAuthor":[truefals]+,\"updatedAt\":"(\d\d\d\d\-\d\d\-\d\d)T(\d\d\:\d\d\:\d\d)', html):
        list_of_update_time_tuples.append(item)

    # Printing out the headlines and creation times

    for i in range(10):
        print(i+1, "Headline:",   list_of_headlines[i])
        print("  Created:", list_of_creation_time_tuples[i][0], "at", list_of_creation_time_tuples[i][1])
        print("  Latest update:", list_of_update_time_tuples[i][0], "at", list_of_update_time_tuples[i][1])
        print()


main()


