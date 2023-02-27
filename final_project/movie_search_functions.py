import nltk
from nltk.stem import PorterStemmer
from nltk import word_tokenize
#nltk.download('punkt')
import pke
import numpy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import matplotlib.pyplot as plt

import re

def index_documents_from_text_file():
    """ This function first opens a file, reads its contents
        into a string and closes the file. Then it creates and returns a list
        of every item consisiting of an article title and the article text itself
    """
    document_string = ""
    
    # Opening the file, storing the contents of the article into one string, closing the file
    try:
        input_file = open("synopses.txt", "r", encoding = 'utf8')    
        #for line in input_file:
        #    line = line.strip()
        #    document_string += line + " "
        document_string = input_file.read()
        input_file.close()

    except FileNotFoundError:
        print(f"File was not found.")
    except OSError:
        print(f"Something went wrong reading the file.")
    except:
        print("Something went wrong.")

    article_content_string = re.sub(r"<synopsis>", "",  document_string)
    synopsis_list = article_content_string.strip().split("</synopsis>")
    
    return synopsis_list

def this_is_movie_search():
    message = "NLP is great!"
    return message

def search_b(synopsis_list, query): #boolean search
    """This function handles the Boolean search
    """
    hits_list = []
    cv = CountVectorizer(lowercase=True, binary=True, token_pattern=r"(?u)\b\w\w*\b") # indexing all words containing alphanumeric characters
    
    sparse_matrix = cv.fit_transform(synopsis_list)
    dense_matrix = sparse_matrix.todense()
    td_matrix = dense_matrix.T
    # There seems to be variation in these commands between scikit-learn versions - 
    # this block of code helps with that 
    try:
        terms = cv.get_feature_names_out()
        #print("Terms:", terms)
    except AttributeError:
        terms = cv.get_feature_names()
    
    t2i = cv.vocabulary_
    parts = query.split()
    parts_without = parts[:]

    all_one = False

    for i, p in enumerate(parts_without):
        if p == "not" or p == "and" or p == "or":
            continue
        elif p not in terms:
            if i > 0 and parts_without[i-1] == "not":
                if i-1 == 0:
                    parts = parts[i+1:]
                elif i-1 > 0:
                    parts = parts[:i-1]
                all_one = True
            elif i != len(parts_without)-1 and parts_without[i+1] == "or":
                parts = parts[i+1:]
                all_one = False
            elif i == len(parts_without)-1 and parts_without[i-1] == "or":
                parts = parts[:i-1]
                all_one = False
            else:
                continue
            
    operator = ""
    if len(parts) > 0:
        if parts[0] == "or" or parts[0] == "and":
            operator = parts[0]
            parts = parts[1:]
            #print("And tai or alussa",parts)
        
        elif parts[-1] == "or" or parts[-1] == "and":
            operator = parts[-1]
            parts = parts[:len(parts)-1]
            #print("And tai or lopussa",parts)
    
        if operator == "or" and all_one == True:
            shape = 1, len(docs)
            hits_matrix = numpy.ones(shape, dtype=int)
            print(hits_matrix)
    
        elif operator == "and":
            if len(parts) > 0:
                parts_into_string = " ".join(parts)
                hits_matrix = eval(rewrite_query(parts_into_string))

        else:
            parts_into_string = " ".join(parts)
            try:
                hits_matrix = eval(rewrite_query(parts_into_string))
            except KeyError:
                shape = 1, len(docs)
                hits_matrix = numpy.zeros(shape, dtype=int)
        hits_list = list(hits_matrix.nonzero()[1])
    else:
        shape = 1, len(docs)
        hits_matrix = numpy.ones(shape, dtype=int)
        hits_list = list(hits_matrix.nonzero()[1])
        
    return hits_list
    

def search_t(synopsis_list, query): #tf-idf search
    tfv = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2")
    sparse_matrix = tfv.fit_transform(synopsis_list).T.tocsr() # CSR: compressed sparse row format => order by terms

    # The query vector is a horizontal vector, so in order to sort by terms, we need to use CSC
    query_vec = tfv.transform([query]).tocsc() # CSC: compressed sparse column format

    hits = np.dot(query_vec, sparse_matrix)
    best_doc_ids = []

    try:
        ranked_scores_and_doc_ids = sorted(zip(np.array(hits[hits.nonzero()])[0], hits.nonzero()[1]), reverse=True)

        for score, i in ranked_scores_and_doc_ids:
                best_doc_ids.append(i)

    except IndexError: # Entering an unknown word causes IndexError
        print("No matches")
    return best_doc_ids

def search_other():
    return "This is some other search"
