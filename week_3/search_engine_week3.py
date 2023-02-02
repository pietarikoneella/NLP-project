import re
import numpy
from sklearn.feature_extraction.text import CountVectorizer
import math

from sklearn.feature_extraction.text import TfidfVectorizer
import numpy as np

def index_documents_from_text_file():
    """ This function first opens a file, reads its contents
        into a string and closes the file. Then it creates and returns a list
        of every item consisiting of an article title and the article text itself
    """
    document_string = ""
    
    # Opening the file, storing the contents of the article into one string, closing the file
    try:
        input_file = open("articles.txt", "r", encoding = 'utf8')    
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

def rewrite_token(t):
    d = {"AND": "&", "OR": "|",
        "NOT": "1 -",
        "(": "(", ")": ")"}  # operator replacements

    #print(d.get(t, 'td_matrix[t2i["{:s}"]]'.format(t))) # N.B. This print statement shows the rewritten query!
    return d.get(t, 'td_matrix[t2i["{:s}"]]'.format(t)) 

def rewrite_query(query): # rewrite every token in the query
        return " ".join(rewrite_token(t) for t in query.split())


def boolean_search(docs, query):
    """This function handles the Boolean search
    """

    cv = CountVectorizer(lowercase=True, binary=True, token_pattern=r"(?u)\b\w\w*\b") # indexing all words containing alphanumeric characters
    
    sparse_matrix = cv.fit_transform(docs)
    dense_matrix = sparse_matrix.todense()
    td_matrix = dense_matrix.T

    # There seems to be variation in these commands between scikit-learn versions - 
    # this block of code helps with that 
    try:
        terms = cv.get_feature_names_out()
    except AttributeError:
        terms = cv.get_feature_names()

    t2i = cv.vocabulary_

    try:
        # This if statement code checks if there is a NOT operator in the query. If the negated word does not 
        # exist in any of the documents, it means that every document matches the query. E.g. NOT kiisseli --> all documents match
        if "NOT" in query:
            not_statements = re.findall("NOT\s(\w+)\s?", query)
            #print(not_statements)
            for word in not_statements:
                if str(docs).find(word) != -1:
                    hits_matrix = eval(rewrite_query(query))
                else: # This is the case where the negated word isn't in any of the documents, which means a 100% match. 
                    hits_matrix = numpy.matrix([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                                                    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                                                    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                                                    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 
                                                    1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]])      
        else:            
            hits_matrix = eval(rewrite_query(query))      

        hits_list = list(hits_matrix.nonzero()[1])
            
        print("Matches for '" + query + "' were found in following " + str(len(hits_list)) + " document(s):")
        print()
                                
        for i, doc_idx in enumerate(hits_list):
        # Using the three stars to find the end of the article title
            if i > 9:
                print("Showing the ten first results.")
                print()
                break
            index = docs[doc_idx].find("***")
            print("Matching doc #{:d}: {:s}".format(i, docs[doc_idx][:index]))
            print(docs[doc_idx][index+3:].strip())

            print()
                                    
            # There was a list index out of range error with search word 'interesting' so I commented this away for now
            """
            for doc_idx in hits_list:
                docs_list = re.findall(r"^.{200,500}\.", docs[doc_idx])
                docs = "".join(docs_list)
               print("Matching doc:", docs)
            """
                    
    except KeyError:
        print("No matches")
    
def tfidf_search(documents, query): # !
    tfv = TfidfVectorizer(lowercase=True, sublinear_tf=True, use_idf=True, norm="l2")
    sparse_matrix = tfv.fit_transform(documents).T.tocsr() # CSR: compressed sparse row format => order by terms

    # The query vector is a horizontal vector, so in order to sort by terms, we need to use CSC
    query_vec = tfv.transform([query]).tocsc() # CSC: compressed sparse column format

    hits = np.dot(query_vec, sparse_matrix)

    try:
        ranked_scores_and_doc_ids = sorted(zip(np.array(hits[hits.nonzero()])[0], hits.nonzero()[1]), reverse=True)

        number_of_matches = 0
        best_doc_ids = []

        for score, i in ranked_scores_and_doc_ids:
            if number_of_matches < 10:
                best_doc_ids.append(i)
            number_of_matches += 1

        print(number_of_matches, "document(s) matched your query.")
        if number_of_matches > 10:
            print("Showing the top 10 matches.\n")

        for i in best_doc_ids:
            print(documents[i])
            print()

    except IndexError: # Entering an unknown word causes IndexError
        print("No matches")

def main():

    #documents = ["This is a silly example",
    #            "A better example",
    #            "Nothing to see here",
    #            "This is a great and long example"]


    documents = index_documents_from_text_file()

    print("SEARCH ENGINE")
    search_method = " "
    while search_method != "":

        search_method = input("Would you like to make a Boolean (B) or an tf-idf search (T)? ").lower().strip()
        if search_method == "b":
            print("You chose Boolean search.")
            break
        elif search_method == "t":
            print("You chose tf-idf search.")
            break

    query ="*"
    while query != "":
        query = input("Type a query: ")
        if query == "":
            print("Goodbye!")
            break
        elif search_method == "b":
            boolean_search(documents, query)
        elif search_method == "t":
            tfidf_search(documents, query)

    
main()
