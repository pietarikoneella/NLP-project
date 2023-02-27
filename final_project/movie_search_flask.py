from flask import Flask, render_template, request, redirect, url_for
import re
import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pke
import movie_search_functions as ms
from movies import *

app = Flask(__name__)

# This is how we access the functions in movie_search_functions.py
message = ms.this_is_movie_search()
print(message)

#Simple example lists
titles = ["Movie 1", "Movie 2", "Movie 3", "Movie 4"] 
ratings = [2, 3, 4, 5]
years = [2001, 2002, 2003, 2004]
synopses = ["Synopsis 1", "Synopsis 2", "Synopsis 3", "Synopsis 4"]

#titles = []
#ratings = []
#years = []
#synopses = []

data = zip(titles, ratings, years, synopses)
query = ""
result_list = []


@app.route('/')
def index():
    return redirect('index')


@app.route('/index')
def search():
    """ This function now goes through the toy data and makes a result list
        out of it if and only if the user has typed in a query.
        Later on we will use the query to get relevant search results
    """
    query = request.args.get('query')
    method = request.args.get('search_method')
    i = 0

    if method == 'Boolean':
        print(ms.search_b())
    elif method == 'td-idf':
        print(ms.search_t())
    elif method == 'Third option':
        print(ms.search_other())
    else:
        pass 

    # N.B. So far this only lists all of the movies. When we have search working,
    # this will show the search results
    for item in data:
        # Using the Movie class to create a movie object
        new_movie = Movie(i, item[0], item[1], item[2], item[3])
        result_list.append(new_movie)
        i+=1

    #for item in result_list:
    #    print(item.get_id())
    #    print(item.get_title())
    #    print(item.get_rating())
    #    print(item.get_synopsis())

    if query:
        print('The query is "' + query +'".')

    return render_template('index.html', result_list=result_list, query=query, method=method)


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
    #theme_listing = [] # Later on, here will be the function call for theme extraction
    movie_.set_themes(theme_listing)

    return render_template('movie.html', result_list=result_list, id=id, movie_=movie_)
