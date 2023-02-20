from flask import Flask, render_template, request
import re
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
        
        for p in keyph[0]:
            themes.append(p[0])
            values.append(round(p[1], 2))
        fig = plt.figure()

        legend_names = []
        for t in themes:
            legend_names.append(t)
        

        plt.title(f"Themes for article \"{title}\"")

        colors = plt.cm.rainbow(np.linspace(0, 1, 5))
        bar = plt.bar(themes, values, color = colors)
        plt.bar_label(bar, values)
        plt.xticks(rotation=20)
        plt.subplots_adjust(bottom=0.15)
        plt.savefig(f'static/article_{title}_plot.png')

print("Loading articles")
documents = se.index_documents_from_text_file("articles_long.txt")
if len(documents) == 1000:
#if len(documents) == 100:
    print("Successfully loaded articles")
print("Stemming articles")
stemmed_documents = se.stemming_documents(documents)
if len(stemmed_documents) == 1000:
#if len(stemmed_documents) == 100:
    print("Successfully stemmed articles")
print("Documents:", len(documents))
print("Stemmed documents:", len(stemmed_documents))

test_ids_0 = [*range(0,100,1)]
test_ids_1 = [*range(100,200,1)]
test_ids_2 = [*range(200,300,1)]
test_ids_3 = [*range(300,400,1)]
test_ids_4 = [*range(400,500,1)]
test_ids_5 = [*range(500,600,1)]
test_ids_6 = [*range(600,700,1)]
test_ids_7 = [*range(700,800,1)]
test_ids_8 = [*range(800,900,1)]
test_ids_9 = [*range(900,1000,1)]

#Getting the article titles for check-up
title_list_0 = se.get_titles(documents, test_ids_0)
title_list_1 = se.get_titles(documents, test_ids_1)
title_list_2 = se.get_titles(documents, test_ids_2)
title_list_3 = se.get_titles(documents, test_ids_3)
title_list_4 = se.get_titles(documents, test_ids_4)
title_list_5 = se.get_titles(documents, test_ids_5)
title_list_6 = se.get_titles(documents, test_ids_6)
title_list_7 = se.get_titles(documents, test_ids_7)
title_list_8 = se.get_titles(documents, test_ids_8)
title_list_9 = se.get_titles(documents, test_ids_9)

#for i in range(100):
#    print(title_list[i])
print("First and last title:")
print("First title on the list:", title_list_0[0])
print("Last title on the list:", title_list_0[-1])
print()
print("First and last title:")
print("First title on the list:", title_list_1[0])
print("Last title on the list:", title_list_1[-1])
print()
print("First and last title:")
print("First title on the list:", title_list_2[0])
print("Last title on the list:", title_list_2[-1])
print()
print("First and last title:")
print("First title on the list:", title_list_3[0])
print("Last title on the list:", title_list_3[-1])
print()
print("First and last title:")
print("First title on the list:", title_list_4[0])
print("Last title on the list:", title_list_4[-1])
print()
print("First and last title:")
print("First title on the list:", title_list_5[0])
print("Last title on the list:", title_list_5[-1])
print()
print("First and last title:")
print("First title on the list:", title_list_6[0])
print("Last title on the list:", title_list_6[-1])
print()
print("First and last title:")
print("First title on the list:", title_list_7[0])
print("Last title on the list:", title_list_7[-1])
print()
print("First and last title:")
print("First title on the list:", title_list_8[0])
print("Last title on the list:", title_list_8[-1])
print()
print("First and last title:")
print("First title on the list:", title_list_9[0])
print("Last title on the list:", title_list_9[-1])
print()


@app.route('/')
def index():
   return render_template("welcome_page.html")

@app.route('/options')
def optionts():
    return render_template("options.html")
#Function search() is associated with the address base URL + "/search"

@app.route('/boolean')
def search_b():

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
        
    return render_template('boolean.html', data=data, query=query, number_of_docs=number_of_docs)

@app.route('/td_idf')
def search_t():

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




