import re
import numpy
from sklearn.feature_extraction.text import CountVectorizer
import math

def index_documents_from_text_file():
    """ This function first opens a file, reads its contents
        into a string and closes the file. Then it creates and returns a list
        of every item consisiting of an article title and the article text itself
    """
    document_string = ""
    
    # Opening the file, storing the contents of the article into one string, closing the file
    try:
        #with open("articles.txt") as input_file:
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
    
    # Finding the article titles, storing them in a list
    title_list = re.findall(r"\<article name\=\"([\w\s\d\.\,\(\)\?\!]*)\"\>", document_string)
    # Making a new content string without the article name tags and article names
    article_content_string = re.sub(r"\<article name\=\"[\w\s\d\.\,\(\)\?\!]*\"\>", "",  document_string)
    # Splitting the contents into a new list with the help of the still remaining endtags 
    content_list = article_content_string.strip().split("</article>")
    # Removint the last, empty list item
    #content_list.remove("")

    # Combining the article titles and contents into a list 
    # The three stars are added in between to aid in separating the article title from the body text
    article_and_title_list = []
    for i in range(len(title_list)):
        article_and_title_list.append(title_list[i] + " *** " + content_list[i])
    
    return article_and_title_list


def main():

    documents = index_documents_from_text_file()

    
    #documents = ["This is a silly example",
    #            "A better example",
    #            "Nothing to see here",
    #            "This is a great and long example"]

    cv = CountVectorizer(lowercase=True, binary=True, token_pattern=r"(?u)\b\w\w*\b") # indexing all words containing alphanumeric characters
    
    sparse_matrix = cv.fit_transform(documents)
    dense_matrix = sparse_matrix.todense()
    td_matrix = dense_matrix.T

    # There seems to be variation in these commands between scikit-learn versions - 
    # this block of code helps with that 
    try:
        terms = cv.get_feature_names_out()
    except AttributeError:
        terms = cv.get_feature_names()

    t2i = cv.vocabulary_

    d = {"AND": "&", "OR": "|",
        "NOT": "1 -",
        "(": "(", ")": ")"}          # operator replacements

    def rewrite_token(t):
        print(d.get(t, 'td_matrix[t2i["{:s}"]]'.format(t))) # N.B. This print statement shows the rewritten query!
        return d.get(t, 'td_matrix[t2i["{:s}"]]'.format(t)) 

    def rewrite_query(query): # rewrite every token in the query
        return " ".join(rewrite_token(t) for t in query.split())

    query ="*"
    while query != "":
            
        query = input("Type a query: ")

        if query == "":
            print("Goodbye!")
            break
        else:
            try:
                
                # This if statement code checks if there is a NOT operator in the query. If the negated word does not 
                # exist in any of the documents, it means that every document matches the query. E.g. NOT kiisseli --> all documents match
                if "NOT" in query:
                    not_statements = re.findall("NOT\s(\w+)\s?", query)
                    #print(not_statements)
                    for word in not_statements:
                        if str(documents).find(word) != -1:
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
                
                # Maria's code for task 5 (covering also task 2)- Maria commented this away since task 2 was issued to Sofia
                # This is a slightly different solution utilizing the stars that were used in my function to separate the article title
                # from the article text
                """
                    for i, doc_idx in enumerate(hits_list):
                    # Using the three stars to find the end of the article title
                    index = documents[doc_idx].find("***")
                    print("Matching doc #{:d}: {:s}".format(i, documents[doc_idx][:index]))
                    print(documents[doc_idx][index+3:].strip())
                    print()
                """
                    
                # Sofia's code for task 2
                for doc_idx in hits_list:
                    docs_list = re.findall(r"^.{200,500}\.", documents[doc_idx])
                    docs = "".join(docs_list)
                    print("Matching doc:", docs)
                    
            except KeyError:
                print("No matches")
    
    
main()
