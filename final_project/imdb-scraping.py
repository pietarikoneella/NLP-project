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
        #rank = movie.find("td", class_="titleColumn").get_text(strip=True).split(".")[0]

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
    file.write("\n\n")
    file.write(str(ranks) + "\n\n")
    file.write(str(names) + "\n\n")
    file.write(str(years) + "\n\n")
    file.write(str(ratings) + "\n\n")
    file.close()

    #Extracting stuff from a movie's plot page
    ploturls = []
    
    a=1

    for url in urls:
        url = url + "plotsummary/?ref_=tt_stry_pl#synopsis"
        ploturls.append(url)

    url_1= ["https://www.imdb.com/title/tt1201607/plotsummary/?ref_=tt_stry_pl#synopsis",
            "https://www.imdb.com/title/tt0015324/plotsummary/?ref_=tt_stry_pl#synopsis"]  #180,195
    url_2= ["https://www.imdb.com/title/tt0088763/plotsummary/?ref_=tt_stry_pl#synopsiss",
            "https://www.imdb.com/title/tt2024544/plotsummary/?ref_=tt_stry_pl#synopsis",
            "https://www.imdb.com/title/tt2278388/plotsummary/?ref_=tt_stry_pl#synopsis"] #30, 180, 184
    url_3 = ["https://www.imdb.com/title/tt0107207/plotsummary/?ref_=tt_stry_pl#synopsis"] #189

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
                      "https://www.imdb.com/title/tt0363163/plotsummary/?ref_=tt_stry_pl#synopsis",
                      "https://www.imdb.com/title/tt0088763/plotsummary/?ref_=tt_stry_pl#synopsis",
                      "https://www.imdb.com/title/tt0073195/plotsummary/?ref_=tt_stry_pl#synopsis",
                      "https://www.imdb.com/title/tt0245712/plotsummary/?ref_=tt_stry_pl#synopsis",
                      "https://www.imdb.com/title/tt0032976/plotsummary/?ref_=tt_stry_pl#synopsis",
                      "https://www.imdb.com/title/tt0025316/plotsummary/?ref_=tt_stry_pl#synopsis",
                      "https://www.imdb.com/title/tt0129167/plotsummary/?ref_=tt_stry_pl#synopsis",
                      "https://www.imdb.com/title/tt0103639/plotsummary/?ref_=tt_stry_pl#synopsis"] #14,21,31, 52,99, 100,107, 109, 115, 118, 120, 124, 30, 204, 236, 237, 242, 245

    url_fails= ["https://www.imdb.com/title/tt0027977/plotsummary/?ref_=tt_stry_pl#synopsis",
                "https://www.imdb.com/title/tt0057565/plotsummary/?ref_=tt_stry_pl#synopsis",
                "https://www.imdb.com/title/tt8267604/plotsummary/?ref_=tt_stry_pl#synopsis",
                "https://www.imdb.com/title/tt0091251/plotsummary/?ref_=tt_stry_pl#synopsis",
                "https://www.imdb.com/title/tt0012349/plotsummary/?ref_=tt_stry_pl#synopsis",
                "https://www.imdb.com/title/tt3011894/plotsummary/?ref_=tt_stry_pl#synopsis",
                "https://www.imdb.com/title/tt0050976/plotsummary/?ref_=tt_stry_pl#synopsis",
                "https://www.imdb.com/title/tt0317705/plotsummary/?ref_=tt_stry_pl#synopsis",
                "https://www.imdb.com/title/tt0113247/plotsummary/?ref_=tt_stry_pl#synopsis",
                "https://www.imdb.com/title/tt0476735/plotsummary/?ref_=tt_stry_pl#synopsis",
                "https://www.imdb.com/title/tt0053198/plotsummary/?ref_=tt_stry_pl#synopsis"]  #47,86,88,93,128,196,200,228,229,235, 240 urls without synopsis
    
                      
                      
                             
    #extract synopsis from urls
    file = open("synopses.txt", "w")
    for url in ploturls:
    
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})

        if url in url_1:
            webpage = urlopen(req).read().decode('utf-8')
            webpage = str(webpage)
            soup = BeautifulSoup(webpage, "html.parser")
            summaries = soup.find_all("div", class_="ipc-html-content")
                
            try:
                summary = str(summaries[8])
            
            except Exception as e:
                print(e)
                
        elif url in url_2:
            webpage = urlopen(req).read().decode('utf-8')
            webpage = str(webpage)
            soup = BeautifulSoup(webpage, "html.parser")
            summaries = soup.find_all("div", class_="ipc-html-content")
                
            try:
                summary = str(summaries[11])
            
            except Exception as e:
                print(e)

        elif url in url_3:
            webpage = urlopen(req).read().decode('utf-8')
            webpage = str(webpage)
            soup = BeautifulSoup(webpage, "html.parser")
            summaries = soup.find_all("div", class_="ipc-html-content")
                
            try:
                summary = str(summaries[7])
            
            except Exception as e:
                print(e)

        
        else:
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
                
                    soup = BeautifulSoup(webpage, "html.parser")
                    summaries = soup.find_all("div", class_="ipc-html-content")
                
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
            
                    soup = BeautifulSoup(webpage, "html.parser") 
                    summaries = soup.find_all("div", class_="ipc-html-content")
                
                    try:
                        synopsis = str(summaries[2])
            
                    except Exception as e:
                        print(e)
                
        #remove tags
        synopsis = re.sub(r'<br><br>', r"\n\n", synopsis) #makes paragraphs
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

    a=1
    summaries = []
    #extract summary 
    file = open("movies.txt", "a+")
    
    
    for url in ploturls:
    
        req = Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        
        if url not in url_not_decode:
            webpage = urlopen(req).read().decode('utf-8')
            webpage = str(webpage)
            soup = BeautifulSoup(webpage, "html.parser")
            summaries_text = soup.find_all("div", class_="ipc-html-content")
                
            try:
                summary = str(summaries_text[0])
            
            except Exception as e:
                print(e)

        elif url in url_not_decode:
            webpage = urlopen(req).read()
            webpage = str(webpage)
            soup = BeautifulSoup(webpage, "html.parser")
            summaries_text = soup.find_all("div", class_="ipc-html-content")
                
            try:
                summary = str(summaries_text[0])
            
            except Exception as e:
                print(e)

        #remove tags
        summary = re.sub(r'<br><br>', r"\n", summary) #makes paragraphs
        tags = re.findall(r"<[^<>]+>", summary)
        for i in range(len(tags)):
            summary = re.sub(r"<[^<>]+>", r"", summary)
        summary = re.sub(r'&quot;', r'"', summary)
        summary = re.sub(r'&#39;', r"'", summary) 
        summary = re.sub(r'&amp;', r"&", summary) 
        summary = re.sub(r'&#12302;&#28779;&#22402;&#12427;&#12398;&#22675;&#12303;', r"", summary)
        summary = re.sub(r'&#12302;&#21531;&#12398;&#21517;&#12399;&#12290;&#12303;', r"", summary)
        summary = re.sub(r'\\xc3\\xbc', r"u", summary)
        summary = re.sub(r'\\xc3\\xb6', r"o", summary)
        summary = re.sub(r'&mdash;', r"", summary)

        try:
            file.write(summary + "#")
            summaries.append(summary)
            print("done_sum", a)
            a = a + 1

        except Exception as e:
            print(e)
            
    file.write("\n\n")        
    file.write(str(summaries) + "\n\n")    
    
        
        
    
    file.close()
    
    
except Exception as e:
    print(e)
