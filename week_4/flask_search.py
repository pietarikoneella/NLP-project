from flask import Flask, render_template, request
import re

# With this import we can access the functions from search_engine_week4.py
import search_engine_week4 as se

#Initialize Flask instance
app = Flask(__name__)

print("Loading articles")
documents = se.index_documents_from_text_file("articles.txt")
if len(documents) == 100:
    print("Successfully loaded articles")
print("Stemming articles")
stemmed_documents = se.stemming_documents(documents)
if len(stemmed_documents) == 100:
    print("Successfully stemmed articles")


# The rest of the code is copied from the example

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
        data = zip(matches_titles, matches_texts)
        number_of_docs = len(ids)


    #If query exists (i.e. is not None)
    #if query:
        #Look at each entry in the example data
        #for entry in example_data:
            #If an entry name contains the query, add the entry to matches
            #if query.lower() in entry['name'].lower():
                #matches.append(entry)

    #Render index.html with matches variable
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
        data = zip(matches_titles, matches_texts)
        number_of_docs = len(ids)
    
    return render_template('td_idf.html', data=data, query=query, number_of_docs=number_of_docs) #matches=matches)




