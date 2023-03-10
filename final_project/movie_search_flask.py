from flask import Flask, render_template, request, redirect, url_for
import re
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import spacy
import pke
import movie_search_functions as ms
from movies import *

app = Flask(__name__)

synopsis_list = ms.index_documents_from_text_file()
synopsis_list_bold = []

file = open("movies.txt", "r")
ranks = file.readline().split("#")
del ranks[-1] # remove "\n"
titles = file.readline().split("#")
del titles[-1]
years = file.readline().split("#")
del years[-1]
ratings = file.readline().split("#")
del ratings[-1]
file.close()

themes = []
summaries = []

# To be replaced with the real ones later!
t = [("a", 0.12), ("b", 0.23), ("c",0.09), ("d",0.2), ("e",0.1)] # To be replaced
s = "This is a movie summary." # To be replaced
for i in range(len(ratings)):
    themes.append(t)
    summaries.append(s)



file = open("synopses.txt", "r", encoding = "ISO-8859-1")

synopses = file.read().split("</synopsis>")
del synopses[-1] # remove newlines
file.close()

data = zip(titles, ratings, years, themes, summaries, synopses)
query = ""
result_list = []
movie_list = []

    

i = 0
for item in data:
    # New movie object Movie(id, title, rating, year, themes, summary, synopsis)
    new_movie = Movie(i, item[0], item[1], item[2], item[3], item[4], item[5])
    movie_list.append(new_movie)
    i+=1

@app.route('/')
def index():
    return redirect('index')


@app.route('/index')
def search():
    """ This function now goes through the data and makes a result list
        out of it if and only if the user has typed in a query.
        Then it uses the query to get relevant search results
    """
    query = request.args.get('query')
    method = request.args.get('search_method')
    
    i = 0
    doc_ids = []
    result_ids = []
    final_result_list = []

    if query:
        
        if method == 'Boolean':
            result_ids = ms.search_b(synopsis_list, query)        
            final_result_list = []
            if len(result_ids) > 0:
                for i in result_ids:
                    final_result_list.append(movie_list[i])

        elif method == 'td-idf':
            result_ids = ms.search_t(synopsis_list, query)
            final_result_list = []
            if len(result_list) > 0:
                for i in result_ids:
                    final_result_list.append(movie_list[i])


        elif method == 'Third option':
            print(ms.search_other())

        for id in result_ids:
            s = movie_list[id].get_synopsis()
            s_new = re.sub(str(query), f"<mark><b>{query}</b></mark>", s)
            movie_list[id].set_synopsis(s_new)

    else:
        if method == 'Boolean' or method == 'td-idf':
            pass
        elif method == 'List all movies':
            final_result_list = movie_list[:]

        else:
            pass

    if query:
        print('The query is "' + query +'".')

    number=len(final_result_list)

    return render_template('index.html',  movie_list=movie_list, final_result_list=final_result_list, number=number, query=query, method=method)


@app.route('/movie/<title>/<id>')

def show_movie(title, id):
    """ This function creates a page for an individual movie object.
        Theme extraction and later on adding a plot is done here - only if
        the user clicks the link for that particular movie.
    """
    #print("Showing movie")
    id = int(id)
    #query = str(request.args.get('query'))
    
    #print("SYNOPSIS")
    #print(synopses[id])
    #synopsis_bold = ms.highlight_query(query, synopses[id])

    movie_ = Movie(id, titles[id], ratings[id], years[id], themes[id], summaries[id], synopses[id])
    title = movie_.get_title()


    


    #This is now extra since we decided to extract themes for all the movies at once
    """
    theme_listing = ["theme 1", "theme 2", "theme 3", "theme 4", "theme 5"]
    nlp = spacy.load('en_core_web_sm')
    text = movie_.get_synopsis()
    text = nlp(text)
    tag = ["PROPN"]
    synopsis_no_names = ""
    for token in text:
        if token.pos_ not in tag:
            print(token)
            t = " " + token.text
            synopsis_no_names += t
    print(synopsis_no_names)
    extractor = pke.unsupervised.TopicRank()
    extractor.load_document(synopsis_no_names, language='en')
    extractor.candidate_selection()
    extractor.candidate_weighting()
    number_of_themes = 10 #int(input("How many themes would you like? "))
    keyphrases = extractor.get_n_best(n=number_of_themes)
    print("The themes are as follows:", keyphrases)
    

    #theme_listing = [] # Later on, here will be the function call for theme extraction
    movie_.set_themes(keyphrases)
    """

    ms.make_plot(movie_.get_themes(), movie_.get_title())

    return render_template('movie.html', result_list=result_list, id=id, query=query, title=title, movie_=movie_)
