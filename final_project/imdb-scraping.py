from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
import requests
import re
import pke
extractor = pke.unsupervised.TopicRank()

try:
    headers = {'Accept-Language': 'en-US,en;q=0.5'}
    source = requests.get("https://www.imdb.com/chart/top/", headers=headers)
    source.raise_for_status()
    soup = BeautifulSoup(source.text, "html.parser")
    movies = soup.find("tbody", class_="lister-list").find_all("tr")

    urls = []
    ranks = []
    names = []
    years = []
    ratings = []

    i = 1
    for movie in movies:
        if i > 250: # If you want fewer movies you can specify that here
            break
        else:
            rank = movie.find("td", class_="titleColumn").get_text(strip=True).split(".")[0]
            ranks.append(rank)
            name = movie.find("td", class_="titleColumn").a.text
            names.append(name)
            year = movie.find("td", class_="titleColumn").span.text.strip("()")
            years.append(year)
            rating = movie.find("td", class_="ratingColumn imdbRating").strong.text
            ratings.append(rating)

            a_tag = str(movie.find("td", class_="titleColumn").a)
            link = re.search(r'href=\"(\/title\/\w+\/)', a_tag)
            urls.append("https://www.imdb.com" + link.group(1))
            
            print(rank, name, year, rating)
        i += 1

    file = open("movies.txt", "w")
    for i in ranks:
        file.write(str(i) + "#")
    file.write("\n")
    for i in names:
        file.write(str(i) + "#")
    file.write("\n")
    for i in years:
        file.write(str(i) + "#")
    file.write("\n")
    for i in ratings:
        file.write(str(i) + "#")
    file.write(str(ranks) + "\n\n")
    file.write(str(names) + "\n\n")
    file.write(str(years) + "\n\n")
    file.write(str(ratings) + "\n\n")
    file.close()
        
    #print(urls)

    #url = "https://www.imdb.com/title/tt0111161/"
    #req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    #webpage = urlopen(req).read()
    #print("Beginning of webpage:", webpage[:1000])

    """
    #Extracting stuff from a movie's main page
    for url in urls:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()
        #print("Excerpt of webpage:", webpage[400:800])
        print()

        soup = BeautifulSoup(webpage, "html.parser")

        storyline = soup.find("div", class_="ipc-html-content-inner-div")
        synopsis = soup.find("a", class_="ipc-link ipc-link--base ipc-link--inline")

        #source = requests.get(url) # "403 Client Error: Forbidden"
        #source.raise_for_status()
        #soup = BeautifulSoup(source.text, "html.parser")
        #storyline = soup.find("div", class_="ipc-html-content-inner-div")
    """

    #Extracting stuff from a movie's plot page
    ploturls = []

    for url in urls:
        url = url + "plotsummary/?ref_=tt_stry_pl#synopsis"
        ploturls.append(url)

    file = open("synopses.txt", "w")
    for url in ploturls:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()

        soup = BeautifulSoup(webpage, "html.parser")
        
        summaries = soup.find_all("div", class_="ipc-html-content-inner-div")
        try:
            synopsis = str(summaries[10])
        except Exception as e:
            print(e)

        #remove tags
        tags = re.findall(r"<[^<>]+>", synopsis)
        for i in range(len(tags)):
            synopsis = re.sub(r"<[^<>]+>", r"", synopsis)

        file.write("<synopsis>" + synopsis + "</synopsis>\n\n")
    file.close()
    
except Exception as e:
    print(e)
