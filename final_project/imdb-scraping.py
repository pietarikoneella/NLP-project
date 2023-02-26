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
    
    for movie in movies:
        rank = movie.find("td", class_="titleColumn").get_text(strip=True).split(".")[0]

        if int(rank) > 1: # If you want fewer movies you can specify that here
            break
        else:
            name = movie.find("td", class_="titleColumn").a.text
            year = movie.find("td", class_="titleColumn").span.text.strip("()")
            rating = movie.find("td", class_="ratingColumn imdbRating").strong.text

            a_tag = str(movie.find("td", class_="titleColumn").a)
            link = re.search(r'href=\"(\/title\/\w+\/)', a_tag)
            urls.append("https://www.imdb.com" + link.group(1))
            
            print(rank, name, year, rating)
        
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
    synopsisurls = []

    for url in urls:
        url = url + "plotsummary/?ref_=tt_stry_pl#synopsis"
        synopsisurls.append(url)

    for url in synopsisurls:
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        webpage = urlopen(req).read()

        soup = BeautifulSoup(webpage, "html.parser")
        
        summaries = soup.find_all("div", class_="ipc-html-content-inner-div")
        synopsis = str(summaries[10])

        #remove tags
        tags = re.findall(r"<[^<>]+>", synopsis)
        for i in range(len(tags)):
            synopsis = re.sub(r"<[^<>]+>", r"", synopsis)
        
        print(synopsis)

        # extract themes
        extractor.load_document(synopsis, language='en')
        extractor.candidate_selection()
        extractor.candidate_weighting()
        number_of_themes = int(input("How many themes would you like? "))
        keyphrases = extractor.get_n_best(n=number_of_themes)

        """
        print("Extracted themes:")
        print("=================")
        for keyphrase in keyphrases:
            print(f'{keyphrase[1]:.5f}   {keyphrase[0]}')
        """
        
    
except Exception as e:
    print(e)
