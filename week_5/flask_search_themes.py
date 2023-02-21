from flask import Flask, render_template, request
import re
import os
import pke
import numpy as np
import matplotlib.pyplot as plt

import search_engine_week4 as se


#Initialize Flask instance
app = Flask(__name__)

def make_plot(keyph, title):
    if len(keyph) > 0:
        themes = []
        values = []

        if f"./static/article_{title}_plot.png":
            print(f"The plot for \"{title}\" is already in static!")
        
        for p in keyph[0]:
            themes.append(p[0])
            values.append(round(p[1], 2))
        fig = plt.figure()
        plt.title(f"Themes for article \"{title}\"")
        colors = plt.cm.rainbow(np.linspace(0, 1, 5))
        bar = plt.bar(themes, values, color = colors)
        plt.xticks(rotation=20)
        plt.subplots_adjust(bottom=0.15)
        labels = plt.bar_label(bar, values)
        plt.savefig(f'static/article_{title}_plot.png')

print("Loading articles")
documents = se.index_documents_from_text_file("articles_long.txt")
if len(documents) == 100:
    print("Successfully loaded articles")
print("Stemming articles")
stemmed_documents = se.stemming_documents(documents)
if len(stemmed_documents) == 100:
    print("Successfully stemmed articles")

@app.route('/')
def index():
   return render_template("welcome_page.html")

@app.route('/options')
def optionts():
    return render_template("options.html")
#Function search() is associated with the address base URL + "/search"

@app.route('/boolean')
def search_b():

    os.system('rm -f static/*.png')

    #Get query from URL variable
    query = request.args.get('query')

    #Initialize list of matches
    matches_titles = []
    matches_texts = []
    ids = []
    data = {}
    number_of_docs = 0

    if query:
        # Exact match
        if '"' in query:
            query = re.sub(r"\"", r"", query)
            ids = se.boolean_search(documents, query)
        # Stem search
        elif '"' not in query:                
            stemmed_query = se.stem_query(query)
            ids = se.boolean_search(stemmed_documents, stemmed_query)
            
        matches_titles = se.get_titles(documents, ids)
        matches_texts = se.get_texts(documents, ids)
        #data = zip(matches_titles, matches_texts, matches_themes)
        data = zip(matches_titles, matches_texts)

        number_of_docs = len(ids)
        matches_themes = []
        print("There are", number_of_docs, "matches!")
        
        if len(matches_texts) > 2:
            for i in range(3):
                article = matches_texts[i]
                title = matches_titles[i]
                matches_themes = se.theme_extraction(article)
                #print(matches_themes)
                make_plot(matches_themes, title)
                i += 1
        elif len(matches_texts) < 3:
            for i in range(len(matches_texts)):
                article = matches_texts[i]
                title = matches_titles[i]
                matches_themes = se.theme_extraction(article)
                #print(matches_themes)
                make_plot(matches_themes, title)
                i += 1
        
    return render_template('boolean.html', data=data, query=query, number_of_docs=number_of_docs)

@app.route('/td_idf')
def search_t():

    os.system('rm -f static/*.png')

    #Get query from URL variable
    query = request.args.get('query')

    #Initialize list of matches
    matches_titles = []
    matches_texts = []
    ids = []
    data = {}
    number_of_docs = 0

    if query:
        # Exact match
        if '"' in query:
            query = re.sub(r"\"", r"", query)
            ids = se.tfidf_search(documents, query)
        # Stem search
        elif '"' not in query:                
            stemmed_query = se.stem_query(query)
            ids = se.tfidf_search(stemmed_documents, stemmed_query)

        matches_titles = se.get_titles(documents, ids)
        matches_texts = se.get_texts(documents, ids)

        #data = zip(matches_titles, matches_texts, matches_themes)
        data = zip(matches_titles, matches_texts)

        number_of_docs = len(ids)
        matches_themes = []
        print("There are", number_of_docs, "matches!")
        
        if len(matches_texts) > 2:
            for i in range(3):
                article = matches_texts[i]
                title = matches_titles[i]
                matches_themes = se.theme_extraction(article)
                print(matches_themes)
                make_plot(matches_themes, title)
                i += 1
        elif len(matches_texts) < 3:
            for i in range(len(matches_texts)):
                article = matches_texts[i]
                title = matches_titles[i]
                matches_themes = se.theme_extraction(article)
                print(matches_themes)
                make_plot(matches_themes, title)
                i += 1
    
    return render_template('td_idf.html', data=data, query=query, number_of_docs=number_of_docs) #matches=matches)




