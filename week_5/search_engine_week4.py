import nltk
from nltk.stem import PorterStemmer
from nltk import word_tokenize
#nltk.download('punkt')
import pke
import re
import numpy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np
import matplotlib.pyplot as plt

extractor = pke.unsupervised.TopicRank()

def index_documents_from_text_file(filename):
    """ This function first opens a file, reads its contents
        into a string and closes the file. Then it creates and returns a list
        of every item consisiting of an article title and the article text itself
    """
    document_string = ""
    
    # Opening the file, storing the contents of the article into one string, closing the file
    try:
        input_file = open(filename, "r", encoding = 'utf8')    
        for line in input_file:
            line = line.strip()
            document_string += line + " "
        input_file.close()

    except FileNotFoundError:
        print(f"File was not found.")
    except OSError:
        print(f"Something went wrong reading the file.")
    except:
        print("Something went wrong.")
    
    title_list = re.findall(r"\<article name\=\"([\w\s\d\.\,\(\)\?\!]*)\"\>", document_string)
    article_content_string = re.sub(r"\<article name\=\"[\w\s\d\.\,\(\)\?\!]*\"\>", "",  document_string)
    content_list = article_content_string.strip().split("</article>")
    # Combining the article titles and contents into a list 
    # The three stars are added in between to aid in separating the article title from the body text
    article_and_title_list = []
    for i in range(len(title_list)):
        article_and_title_list.append(title_list[i] + " *** " + content_list[i])
    
    return article_and_title_list

def get_all_titles(filename):
    document_string = ""
    
    # Opening the file, storing the contents of the article into one string, closing the file
    try:
        input_file = open(filename, "r", encoding = 'utf8')    
        for line in input_file:
            line = line.strip()
            document_string += line + " "
        input_file.close()

    except FileNotFoundError:
        print(f"File was not found.")
    except OSError:
        print(f"Something went wrong reading the file.")
    except:
        print("Something went wrong.")
    
    title_list = re.findall(r"\<article name\=\"([\w\s\d\.\,\(\)\?\!]*)\"\>", document_string)
    
    return title_list

def get_all_content(filename):
    document_string = ""
    
    # Opening the file, storing the contents of the article into one string, closing the file
    try:
        input_file = open(filename, "r", encoding = 'utf8')    
        for line in input_file:
            line = line.strip()
            document_string += line + " "
        input_file.close()

    except FileNotFoundError:
        print(f"File was not found.")
    except OSError:
        print(f"Something went wrong reading the file.")
    except:
        print("Something went wrong.")
    
    title_list = re.findall(r"\<article name\=\"([\w\s\d\.\,\(\)\?\!]*)\"\>", document_string)
    article_content_string = re.sub(r"\<article name\=\"[\w\s\d\.\,\(\)\?\!]*\"\>", "",  document_string)
    content_list = article_content_string.strip().split("</article>")
    
    return content_list

    

def rewrite_token(t):
    d = {"and": "&", "or": "|",
        "not": "1 -",
        "(": "(", ")": ")"}  # operator replacements 
    #print(d.get(t, 'td_matrix[t2i["{:s}"]]'.format(t))) # N.B. This print statement shows the rewritten query!
    
    return d.get(t, 'td_matrix[t2i["{:s}"]]'.format(t)) 


def rewrite_query(query): # rewrite every token in the query
        return " ".join(rewrite_token(t) for t in query.split())

def theme_extraction(doc):
    
    # theme extraction
    keyphrases = [] # list of lists of theme/score tuples
    keyphrases_dictionary = {}
    extractor.load_document(doc, language='en')
    extractor.candidate_selection()
    extractor.candidate_weighting()
    number_of_themes = 5
    keyphrases.append(extractor.get_n_best(n=number_of_themes))
    
    return keyphrases


# TO DO BOOLEAN: "not apple and not pineapple"
def boolean_search(docs, query):
    """This function handles the Boolean search
    """
    hits_list = []
    cv = CountVectorizer(lowercase=True, binary=True, token_pattern=r"(?u)\b\w\w*\b") # indexing all words containing alphanumeric characters
    
    sparse_matrix = cv.fit_transform(docs)
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
    
def tfidf_search(documents, query):
    tfv = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2")
    sparse_matrix = tfv.fit_transform(documents).T.tocsr() # CSR: compressed sparse row format => order by terms

    # The query vector is a horizontal vector, so in order to sort by terms, we need to use CSC
    query_vec = tfv.transform([query]).tocsc() # CSC: compressed sparse column format

    hits = np.dot(query_vec, sparse_matrix)
    best_doc_ids = []

    try:
        ranked_scores_and_doc_ids = sorted(zip(np.array(hits[hits.nonzero()])[0], hits.nonzero()[1]), reverse=True)

        #number_of_matches = 0
        

        # Here appending all the results to the list in order to make the function output_results work
        # Most of the original print statement code can be found in def output_results!
        for score, i in ranked_scores_and_doc_ids:
                best_doc_ids.append(i)
                #number_of_matches += 1
        

    except IndexError: # Entering an unknown word causes IndexError
        print("No matches")
    return best_doc_ids
    

def stemming_documents(docs):

    ps = PorterStemmer()
    docs_tokens = [word_tokenize(i) for i in docs]
    docs = [[]]
    docs = [[ps.stem(token) for token in docs_tokens[i]] for i in range(0, len(docs_tokens))]
                         
    for i in range(0, len(docs)):
        docs[i] = " ".join(docs[i])
    return(docs)


def stem_query(q):
    ps = PorterStemmer()
    query_split = q.split(" ")
    
    for i in range(0, len(query_split)):
        if i == 0:
            q = "".join(q)
            q = ps.stem(q)

        elif i > 0:
            query_list_stem = []
            query_list_stem = [ps.stem(token) for token in query_split] 
            q = " ".join(query_list_stem)

    return q

# Commented this away as is it not needed with flask
"""
def output_results(docs: list, match_ids: list):
    print()
    print(len(match_ids), "document(s) matched your query.")
    print()
    if len(match_ids) > 10:
        print("Showing the top 10 matches.\n")

    count = 0
    for i in match_ids:
        if count < 10:
            index = docs[i].find("***")
            print("Matching document: #{:d}: {:s}" .format(i, docs[i][:index]))
            print(docs[i][index+3:].strip())
            count += 1
            print()
"""

# These functions return match article titles and texts in separate lists

def get_titles(docs, match_ids):
    title_list = []
    if len(match_ids) > 0: 
        for i in match_ids:
            index = docs[i].find("***")
            title_list.append(docs[i][:index])
    return title_list

def get_texts(docs, match_ids):
    text_list = []
    if len(match_ids) > 0:
        for i in match_ids:
            index = docs[i].find("***")
            text_list.append(docs[i][index+3:].strip())
    return text_list



def main():

#    documents = index_documents_from_text_file("articles.txt")
#    stemmed_documents = stemming_documents(documents)
    """
    documents = ["One two three and four interest.",
                 "Two three four or five interesting?",
                 "Three four five six yes left interests.",
                 "Four five six all right and left interested!"
                ]
    
    stemmed_documents = stemming_documents(documents)
    
    print("Documents:")
    for item in documents:
        print(item)
    print()
    print("Stemmed documents:")
    for item in stemmed_documents:
        print(item)
    print()
    """

    """
    print("WELCOME TO SEARCH ENGINE")
    print("-"*24)
    print("Instructions:")
    print("For Boolean search write 'B'")
    print("For td-idf search write 'T'")
    print("In order to find an article by its number, write the number from 0 to 99.")
    print("--------------------------------------------------------------------------")
    search_method = " "
    while search_method != "":

        search_method = input("Please, choose your search method (T, B or article index number): ").lower().strip()
        if search_method == "b":
            print("You chose Boolean search.")

        elif search_method == "t":
            print("You chose tf-idf search.")

        # Search with article number    
        elif re.findall(r"\d+?", search_method) != False:
            try:
                search_method = int(search_method)
                try:
                    for i in documents:
                        i = search_method
                        index = documents[i].find("***")
                    print(f"Article #{i}: {documents[i][:index]}")
                    print(documents[i][index+3:].strip())
                    print()

                except IndexError:
                    print("No articles with number", search_method)
            except ValueError:
                print("Write 'B', 'T' or number from 0 to 99")
            continue # After a search with a document number, the loop continues from the start

        query ="*"
        while query != "":
            query = input("Type a query: ").lower()

            if query == "":
                break
            # Exact match
            elif '"' in query:
                query = re.sub(r"\"", r"", query)
                if search_method == "b":
                    index_list_hits = boolean_search(documents, query)
                elif search_method == "t":
                    index_list_hits = tfidf_search(documents, query)
            # Stem search
            elif '"' not in query:                
                stemmed_query = stem_query(query)
                try:
                    if search_method == "b":
                        index_list_hits = boolean_search(stemmed_documents, stemmed_query)

                    elif search_method == "t":
                        index_list_hits = tfidf_search(stemmed_documents, stemmed_query)
                except UnboundLocalError:
                    continue

            # Printing out the results
            try:
                if len(index_list_hits) > 0:

                    #titles = get_titles(documents, index_list_hits)
                    print("Number of hits:", len(index_list_hits))
                    #for i in index_list_hits:
                    #    print(f"#{i}: {documents[i]}")
                    print()
                    print()
                    #print(titles)
                else:
                    print("No matches.")
            except:
                continue
            
            print("Press ENTER to switch search method or") # There is a continuation to this print statement at the beginning of this loop!       
    """                        
    
main()
