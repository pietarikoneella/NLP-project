import re
from sklearn.feature_extraction.text import CountVectorizer

def index_documents_from_text_file():
    """ This function first opens a file, reads its contents
        into a string and closes the file. Then it creates and returns a list
        of every item consisiting of an article title and the article text itself
    """
    document_string = ""
    
    # Opening the file, storing the contents of the article into one string, closing the file
    try:
        with open("articles.txt") as input_file:
            
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
    content_list.remove("")

    # Combining the article titles and contents into a list 
    # The three stars are added in between to aid in separating the article title from the body text
    article_and_title_list = []
    for i in range(len(title_list)):
        article_and_title_list.append(title_list[i] + "***" + content_list[i])
    
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
                hits_matrix = eval(rewrite_query(query))
                #print("Matching documents as vector (it is actually a matrix with one single row):", hits_matrix)
                #print("The coordinates of the non-zero elements:", hits_matrix.nonzero())    
                hits_list = list(hits_matrix.nonzero()[1])
                
                for doc_idx in hits_list:
                    docs_list = re.findall(r".{7,10}\b", documents[doc_idx])
                    docs_part = docs_list[0]
                    docs = "".join(docs_part)
                    #print("Matching doc:", docs)

                print("Matches for '" + query + "' were found in following document(s):")
                for i, doc_idx in enumerate(hits_list):
                    # Using the three stars to find the end of the article title
                    index = documents[doc_idx].find("***")
                    print("Matching doc #{:d}: {:s}".format(i, documents[doc_idx][:index]))
        
            except KeyError:
                print("No matches")
    
    
main()
