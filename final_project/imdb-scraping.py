from bs4 import BeautifulSoup
from urllib import request
from urllib.request import Request, urlopen
import requests
import re
import pke
extractor = pke.unsupervised.TopicRank()

try:

    headers = {'Accept-Language': 'en-Us,en;q=0.5'}

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
        if i > 179: # If you want fewer movies you can specify that here
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
    
    a=1

    for url in urls:
        url = url + "plotsummary/?ref_=tt_stry_pl#synopsis"
        ploturls.append(url)

    url_without_synopsis = ["https://www.imdb.com/title/tt0027977/plotsummary/?ref_=tt_stry_pl#synopsis",
                            "https://www.imdb.com/title/tt0057565/plotsummary/?ref_=tt_stry_pl#synopsis",
                            "https://www.imdb.com/title/tt8267604/plotsummary/?ref_=tt_stry_pl#synopsis",
                            "https://www.imdb.com/title/tt0091251/plotsummary/?ref_=tt_stry_pl#synopsis",
                            "https://www.imdb.com/title/tt0012349/plotsummary/?ref_=tt_stry_pl#synopsis"]  #47,86,88,93,128,196,199,228,229,235 

    url_not_decode = ["https://www.imdb.com/title/tt1375666/plotsummary/?ref_=tt_stry_pl#synopsis",
                      "https://www.imdb.com/title/tt0038650/plotsummary/?ref_=tt_stry_pl#synopsis",
                      "https://www.imdb.com/title/tt0245429/plotsummary/?ref_=tt_stry_pl#synopsis",                                                                               
                      "https://www.imdb.com/title/tt0021749/plotsummary/?ref_=tt_stry_pl#synopsis",
                      "https://www.imdb.com/title/tt0044741/plotsummary/?ref_=tt_stry_pl#synopsis",                                                                                 
                      "https://www.imdb.com/title/tt0052357/plotsummary/?ref_=tt_stry_pl#synopsis",
                      "https://www.imdb.com/title/tt8503618/plotsummary/?ref_=tt_stry_pl#synopsis",
                      "https://www.imdb.com/title/tt1255953/plotsummary/?ref_=tt_stry_pl#synopsis",
                      "https://www.imdb.com/title/tt0017136/plotsummary/?ref_=tt_stry_pl#synopsis",
                      "https://www.imdb.com/title/tt0095016/plotsummary/?ref_=tt_stry_pl#synopsis",
                      "https://www.imdb.com/title/tt0097576/plotsummary/?ref_=tt_stry_pl#synopsis",
                      "https://www.imdb.com/title/tt0363163/plotsummary/?ref_=tt_stry_pl#synopsis"] #14,21,31, 52,99 (fails), 100,107, 109, 115, 118, 120, 124

    url_fails= ["https://www.imdb.com/title/tt0027977/plotsummary/?ref_=tt_stry_pl#synopsis",
                "https://www.imdb.com/title/tt0057565/plotsummary/?ref_=tt_stry_pl#synopsis",
                "https://www.imdb.com/title/tt8267604/plotsummary/?ref_=tt_stry_pl#synopsis",
                "https://www.imdb.com/title/tt0091251/plotsummary/?ref_=tt_stry_pl#synopsis",
                "https://www.imdb.com/title/tt0012349/plotsummary/?ref_=tt_stry_pl#synopsis"]  #47,86,88,93,128,196,199,228,229,235, 
    
                      
                      
                             

    file = open("synopses.txt", "w")
    for url in ploturls:
    
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        if url not in url_not_decode:
            webpage = urlopen(req).read().decode('utf-8')
            webpage = str(webpage)

            if url not in url_fails:
                synopsis_text = re.findall(r'<h3 class="ipc-title__text"><span id="synopsis">Synopsis.+', webpage) 
                synopsis_text = str(synopsis_text)
                summaries = re.findall(r'<div class=\"ipc-html-content-inner-div\"><div class=\"ipc-html-content ipc-html-content--base" role="presentation"><div class="ipc-html-content-inner-div">(.+)</div></div></div></div></div></li></ul></div></section>',synopsis_text)
        #print(summaries)
    
                try:
                    synopsis = str(summaries[0])
            
                except Exception as e:
                    print(e)
                
            elif url in url_fails:
                #synopsis = "aaaaa"
                soup = BeautifulSoup(webpage, "html.parser")
                
                summaries = soup.find_all("div", class_="ipc-html-content")
                #summaries = re.findall('<div class="ipc-html-content ipc-html-content--base" role="presentation"><div class="ipc-html-content-inner-div">(.+)<span style="display:block" data-reactroot="">', webpage) 
                #synopsis_text = str(synopsis_text)
                #summaries = re.findall(r'<div class=\"ipc-html-content-inner-div\"><div class=\"ipc-html-content ipc-html-content--base" role="presentation"><div class="ipc-html-content-inner-div">(.+)</div></div></div></div></div></li></ul></div></section>',synopsis_text)
        #print(summaries)
    
                try:
                    synopsis = str(summaries[2])
            
                except Exception as e:
                    print(e)

        elif url in url_not_decode:
            webpage = urlopen(req).read()
            webpage = str(webpage)

            if url not in url_fails:
                synopsis_text = re.findall(r'<h3 class="ipc-title__text"><span id="synopsis">Synopsis.+', webpage) 
                synopsis_text = str(synopsis_text)
                summaries = re.findall(r'<div class=\"ipc-html-content-inner-div\"><div class=\"ipc-html-content ipc-html-content--base" role="presentation"><div class="ipc-html-content-inner-div">(.+)</div></div></div></div></div></li></ul></div></section>',synopsis_text)
        #print(summaries)
    
                try:
                    synopsis = str(summaries[0])
            
                except Exception as e:
                    print(e)
                
            elif url in url_fails:
                #synopsis = "aaaaa"
                soup = BeautifulSoup(webpage, "html.parser")
                
                summaries = soup.find_all("div", class_="ipc-html-content") # ipc-html-content--base" role="presentation"><div class="ipc-html-content-inner-div">(.+)<span style="display:block" data-reactroot="">', webpage) 
                #synopsis_text = str(synopsis_text)
                #summaries = re.findall(r'<div class=\"ipc-html-content-inner-div\"><div class=\"ipc-html-content ipc-html-content--base" role="presentation"><div class="ipc-html-content-inner-div">(.+)</div></div></div></div></div></li></ul></div></section>',synopsis_text)
        #print(summaries)
    
                try:
                    synopsis = str(summaries[2])
            
                except Exception as e:
                    print(e)
                
        #remove tags
        tags = re.findall(r"<[^<>]+>", synopsis)
        for i in range(len(tags)):
            synopsis = re.sub(r"<[^<>]+>", r"", synopsis)
        synopsis = re.sub(r'&quot;', r'"', synopsis)
        synopsis = re.sub(r'&#39;', r"'", synopsis) 
        synopsis = re.sub(r'&amp;', r"&", synopsis) 
        synopsis = re.sub(r'&#12302;&#28779;&#22402;&#12427;&#12398;&#22675;&#12303;', r"", synopsis)
        synopsis = re.sub(r'&#12302;&#21531;&#12398;&#21517;&#12399;&#12290;&#12303;', r"", synopsis)
        synopsis = re.sub(r'\\xc3\\xbc', r"u", synopsis)
        synopsis = re.sub(r'\\xc3\\xb6', r"o", synopsis)
        synopsis = re.sub(r'&mdash;', r"", synopsis)
        
        file.write("<synopsis>" + synopsis + "</synopsis>\n\n")
        
        print("done", a)
        a = a + 1

    file.close()
 
    
    
except Exception as e:
    print(e)
