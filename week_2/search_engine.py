import re
from sklearn.feature_extraction.text import CountVectorizer


def main():

    #document = open("articles.txt", "r", encoding="utf-8")
    #document.read()
    #article_title_list = re.findall(r"<article name=\"(\w+\S?

    documents = ["This is a silly example",
                "A better example",
                "Nothing to see here",
                "This is a great and long example"]

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
                #print(hits_list)
                
                for doc_idx in hits_list:
                    docs_list = re.findall(r".{7,10}\b", documents[doc_idx])
                    docs_part = docs_list[0]
                    docs = "".join(docs_part)
                    #print("Matching doc:", docs)

                print("Matches for '" + query + "' were found in following document(s):")
                for i, doc_idx in enumerate(hits_list):
                    print("Matching doc #{:d}: {:s}".format(i, documents[doc_idx]))
        
            except KeyError:
                print("No matches")
    
    
main()
