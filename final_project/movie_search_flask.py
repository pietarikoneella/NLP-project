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

def make_plot(keyph, title):
    if len(keyph) > 0:
        themes = []
        values = []

        if f"./static/article_{title}_plot.png":
            print(f"The plot for \"{title}\" is already in static!")
        
        for p in keyph:
            print(p[0])
            print(p[1])
        
        for p in keyph:
            themes.append(p[0])
            values.append(round(p[1], 2))
        fig = plt.figure()
        plt.title(f"Themes for movie \"{title}\"")
        colors = plt.cm.rainbow(np.linspace(0, 1, 5))
        bar = plt.bar(themes, values, color = colors)
        plt.xticks(rotation=20)
        plt.subplots_adjust(bottom=0.15)
        labels = plt.bar_label(bar, values)
        plt.savefig(f'static/movie_{title}_plot.png')


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

file = open("synopses.txt", "r", encoding = "ISO-8859-1")

synopses = file.read().split("</synopsis>")
del synopses[-1] # remove newlines
file.close()

data = zip(titles, ratings, years, synopses)
query = ""
result_list = []
movie_list = []
i = 0
for item in data:
    new_movie = Movie(i, item[0], item[1], item[2], item[3])
    movie_list.append(new_movie)
    i+=1

@app.route('/')
def index():
    return redirect('index')


@app.route('/index')
def search():
    """ This function now goes through the data and makes a result list
        out of it if and only if the user has typed in a query.
        Later on we will use the query to get relevant search results
    """
    query = request.args.get('query')
    method = request.args.get('search_method')
    i = 0
    doc_ids = []
    result_list = []
    final_result_list = []

    if method == 'Boolean':
        result_list = ms.search_b(synopsis_list, query)        
        final_result_list = []
        for i in result_list:
            final_result_list.append(movie_list[i])

    elif method == 'td-idf':
        result_list = ms.search_t(synopsis_list, query)
        final_result_list = []
        for i in result_list:
            final_result_list.append(movie_list[i])

    elif method == 'Third option':
        print(ms.search_other())
    else:
        pass

    if query:
        print('The query is "' + query +'".')

    return render_template('index.html',  movie_list=movie_list, final_result_list=final_result_list, query=query, method=method)


@app.route('/movie/<id>')

def show_movie(id):
    """ This function creates a page for an individual movie object.
        Theme extraction and later on adding a plot is done here - only if
        the user clicks the link for that particular movie.
    """
    print("Showing movie")
    id = int(id)
    movie_ = Movie(id, titles[id], ratings[id], years[id], synopses[id])

    

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

    make_plot(keyphrases, movie_.get_title())

    return render_template('movie.html', result_list=result_list, id=id, movie_=movie_)
